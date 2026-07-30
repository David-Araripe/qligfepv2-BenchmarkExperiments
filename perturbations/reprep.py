#!/usr/bin/env python
"""Create benchmark variants with a different sphere radius or replicate count.

The committed directories under ``perturbations/`` are the 25 A baselines.  A
variant is copied from the selected baseline, while its protein and water sphere
are rebuilt from the fully charged protein under ``startFiles/``.  Starting from
the charged protein is important when making a sphere larger: qprep cannot
restore charges to a protein that was already neutralized for a smaller sphere.

Usage (normally through the Makefile):
    python reprep.py <radius> [jacs | merck | all | <target> ...] [--reps N]

Existing variant directories are never replaced unless ``--force`` is passed.
Pass ``--reparameterize`` to regenerate ligand and cofactor parameters with
qparams; the default deliberately reuses the committed benchmark parameters.
"""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PERT = REPO_ROOT / "perturbations"
STARTFILES = REPO_ROOT / "startFiles"

JACS = ["bace", "cdk2", "jnk1", "mcl1", "p38", "ptp1b", "thrombin", "tyk2"]
MERCK = ["cdk8", "cmet", "eg5", "hif2a", "pfkfb3", "shp2", "syk", "tnks2"]
TARGETS = JACS + MERCK

# PFKFB3 needs its three cofactors during qprep.  The default path uses the
# checked-in PDB and combined force field because qparams output can change
# between releases.  The explicit reparameterization path instead regenerates
# and retains the PDB and combined force field as one consistent set.
COFACTOR_TARGETS = {
    "pfkfb3": {
        "pdb": STARTFILES / "pfkfb3" / "protein" / "cofactors.pdb",
        "sdf": STARTFILES / "pfkfb3" / "protein" / "cofactors.sdf",
        "ff": "AMBER14sb_plus_cofactor",
    },
}

COG_RE = re.compile(
    r"COG\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)"
)
RADIUS_RE = re.compile(r"\d+(?:\.\d+)?")
SETUP_RADIUS_RE = re.compile(r"(?<!\S)-r\s+\d+(?:\.\d+)?")
SETUP_REPS_RE = re.compile(r"(?<!\S)-R\s+\d+")


def radius_label(radius: float) -> str:
    """Return a stable directory/script label such as ``20`` or ``20.5``."""
    return f"{radius:g}"


def parse_args(argv):
    """Parse radius, selectors and optional preparation settings."""
    radius = None
    reps = 10
    selectors = []
    force = False
    reparameterize = False
    qparams_args = []
    tokens = list(argv)
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ("--reps", "-R"):
            i += 1
            if i >= len(tokens):
                sys.exit("error: --reps needs a value")
            try:
                reps = int(tokens[i])
            except ValueError:
                sys.exit(f"error: replicate count must be an integer, got {tokens[i]!r}")
        elif tok == "--force":
            force = True
        elif tok in ("--reparameterize", "--reparametrize"):
            reparameterize = True
        elif tok == "--qparams-args":
            i += 1
            if i >= len(tokens):
                sys.exit("error: --qparams-args needs a quoted argument string")
            try:
                qparams_args = shlex.split(tokens[i])
            except ValueError as exc:
                sys.exit(f"error: invalid --qparams-args value: {exc}")
        elif RADIUS_RE.fullmatch(tok):
            if radius is not None:
                sys.exit(f"error: more than one radius given ({radius_label(radius)} and {tok})")
            radius = float(tok)
        else:
            selectors.append(tok.lower())
        i += 1

    if radius is None:
        sys.exit("error: no radius given. Usage: make <radius> [jacs|merck|<target>...]")
    if radius <= 0:
        sys.exit("error: radius must be greater than zero")
    if reps <= 0:
        sys.exit("error: replicate count must be greater than zero")
    if qparams_args and not reparameterize:
        sys.exit("error: --qparams-args requires --reparameterize")
    reserved = {
        "-i",
        "--input",
        "-pcof",
        "--parametrize-cofactors",
        "-pff",
        "--protein-forcefield",
    }
    conflicts = sorted(reserved.intersection(qparams_args))
    if conflicts:
        sys.exit(
            "error: qparams input/cofactor options are managed by reprep.py and cannot be "
            f"passed through --qparams-args: {', '.join(conflicts)}"
        )
    return radius, reps, selectors, force, reparameterize, qparams_args


def resolve_targets(selectors):
    """Expand subset keywords and reject unknown target names before doing work."""
    chosen = []
    for selector in (selectors or ["all"]):
        if selector == "jacs":
            chosen.extend(JACS)
        elif selector == "merck":
            chosen.extend(MERCK)
        elif selector == "all":
            chosen.extend(TARGETS)
        elif selector in TARGETS:
            chosen.append(selector)
        else:
            valid = ", ".join(TARGETS)
            raise ValueError(
                f"unknown target {selector!r}; choose jacs, merck, all, or one of: {valid}"
            )
    return list(dict.fromkeys(chosen))


def read_cog(water_pdb: Path) -> list[str]:
    """Parse the sphere centre from the baseline water PDB TITLE record."""
    with water_pdb.open() as handle:
        header = handle.readline()
    match = COG_RE.search(header)
    if not match:
        raise ValueError(f"could not parse COG from {water_pdb}: {header!r}")
    return list(match.groups())


def mapped_ligands(mapping_file: Path) -> list[str]:
    """Return the unique ligand names referenced by a mapping JSON file."""
    try:
        edges = json.loads(mapping_file.read_text())["edges"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError(f"invalid mapping file: {mapping_file}") from exc

    ligands = []
    for edge in edges:
        for ligand in (edge.get("from"), edge.get("to")):
            if not isinstance(ligand, str):
                raise ValueError(f"invalid edge in {mapping_file}: {edge!r}")
            ligands.append(ligand)
    return list(dict.fromkeys(ligands))


def validate_ligand_parameters(directory: Path, ligands: list[str]) -> None:
    """Ensure every mapped ligand has the three files consumed by setupFEP."""
    missing = []
    for ligand in ligands:
        for suffix in (".pdb", ".lib", ".prm"):
            path = directory / f"{ligand}{suffix}"
            if not path.is_file():
                missing.append(path)
    if missing:
        names = "\n  - ".join(str(path) for path in dict.fromkeys(missing))
        raise FileNotFoundError(f"mapping references missing ligand files:\n  - {names}")


def validate_baseline(target: str) -> None:
    """Check the source files needed to create and submit a target variant."""
    base = PERT / target
    charged = STARTFILES / target / "protein" / "protein_reindexed_renamed.pdb"
    required = [
        base / "protein.pdb",
        base / "water.pdb",
        base / "ligands.sdf",
        base / "mapping.json",
        base / "prepare.sh",
        base / "analyze.sh",
        charged,
    ]
    missing = [path for path in required if not path.is_file()]

    neq_scripts = [base / "prepare-neq.sh", base / "analyze-neq.sh"]
    has_any_neq_script = any(path.exists() for path in neq_scripts)
    if has_any_neq_script and not all(path.is_file() for path in neq_scripts):
        missing.extend(path for path in neq_scripts if not path.is_file())

    if target in COFACTOR_TARGETS:
        cfg = COFACTOR_TARGETS[target]
        required_cofactor = [
            cfg["pdb"],
            cfg["sdf"],
            base / f"{cfg['ff']}.lib",
            base / f"{cfg['ff']}.prm",
        ]
        missing.extend(path for path in required_cofactor if not path.is_file())

    if missing:
        names = "\n  - ".join(str(path) for path in dict.fromkeys(missing))
        raise FileNotFoundError(f"missing required files for {target}:\n  - {names}")

    ligands = mapped_ligands(base / "mapping.json")
    validate_ligand_parameters(base, ligands)
    read_cog(base / "water.pdb")


def run_qparams(
    source_sdf: Path,
    workdir: Path,
    qparams_args: list[str],
    protein_forcefield: str | None = None,
) -> list[str]:
    """Run qparams on one SDF and return the exact argument vector used."""
    local_sdf = workdir / source_sdf.name
    if source_sdf.resolve() != local_sdf.resolve():
        shutil.copy2(source_sdf, local_sdf)
    cmd = ["qparams", "-i", local_sdf.name, *qparams_args]
    if protein_forcefield is not None:
        cmd.extend(["-pcof", "-pff", protein_forcefield])
    subprocess.run(cmd, cwd=workdir, check=True)
    return cmd


def prepare_cofactors(
    target: str,
    cfg: dict,
    workdir: Path,
    reparameterize: bool,
    qparams_args: list[str],
) -> tuple[str, list[str], list[list[str]]]:
    """Prepare canonical or newly parameterized cofactor inputs for qprep."""
    commands = []
    if reparameterize:
        commands.append(run_qparams(cfg["sdf"], workdir, qparams_args, "AMBER14sb"))
        cofactor_name = "all_cofactors.pdb"
    else:
        cofactor_name = cfg["pdb"].name
        shutil.copy2(cfg["pdb"], workdir / cofactor_name)
        for suffix in (".lib", ".prm"):
            source = PERT / target / f"{cfg['ff']}{suffix}"
            shutil.copy2(source, workdir / source.name)

    required = [workdir / cofactor_name]
    required.extend(workdir / f"{cfg['ff']}{suffix}" for suffix in (".lib", ".prm"))
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"cofactor parameterization did not generate: {missing}")
    return cfg["ff"], ["-cof", cofactor_name], commands


def run_qprep(
    target: str,
    radius: float,
    cog: list[str],
    workdir: Path,
    reparameterize: bool = False,
    qparams_args: list[str] | None = None,
):
    """Run qprep and return its prepared files and parameterization commands."""
    charged = STARTFILES / target / "protein" / "protein_reindexed_renamed.pdb"
    shutil.copy2(charged, workdir / "protein.pdb")

    ff = "AMBER14sb"
    cofactor_args = []
    parameterization_commands = []
    if target in COFACTOR_TARGETS:
        ff, cofactor_args, parameterization_commands = prepare_cofactors(
            target,
            COFACTOR_TARGETS[target],
            workdir,
            reparameterize,
            qparams_args or [],
        )

    # -nbo 0 reproduces the committed baselines' neutralization boundary.  Keep
    # all molecular fragments so changing the water radius does not silently
    # change the protein/cofactor composition as well.
    cmd = [
        "qprep_prot",
        "-i",
        "protein.pdb",
        "-FF",
        ff,
        "-cog",
        *cog,
        "-r",
        radius_label(radius),
        "-b",
        "auto",
        "-sp",
        "3.0",
        "-nbo",
        "0",
        "-skip-ff",
        *cofactor_args,
        "-log",
        "info",
    ]
    subprocess.run(cmd, cwd=workdir, check=True)

    # QligFEP <=2.2 named this output *neutralized.pdb; current versions use
    # protein_processed.pdb.  Accept either without accidentally selecting the
    # fully charged input protein.
    protein_candidates = [workdir / "protein_processed.pdb", *workdir.glob("*neutralized.pdb")]
    prepared = [path for path in protein_candidates if path.is_file()]
    if len(prepared) != 1:
        raise RuntimeError(f"expected one prepared protein in {workdir}, found {prepared}")

    water = workdir / "water.pdb"
    if not water.is_file():
        raise RuntimeError(f"water.pdb was not generated in {workdir}")
    metadata = workdir / "prep.json"
    return prepared[0], water, metadata if metadata.is_file() else None, parameterization_commands


def tracked_baseline_files(base: Path) -> list[Path]:
    """Return the tracked baseline file set, excluding prior generated debris."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", str(base.relative_to(REPO_ROOT))],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Source archives have no .git directory and should contain only the
        # distributed baseline files.  Benchmark target files are top-level.
        return sorted(path for path in base.iterdir() if path.is_file())

    paths = [REPO_ROOT / raw.decode() for raw in result.stdout.split(b"\0") if raw]
    if not paths:
        raise RuntimeError(f"git did not report any baseline files under {base}")
    return paths


def copy_baseline(base: Path, destination: Path) -> None:
    """Copy only distributed baseline inputs, never run outputs or untracked files."""
    destination.mkdir()
    for source in tracked_baseline_files(base):
        if source.name in {"protein.pdb", "water.pdb"}:
            continue
        relative = source.relative_to(base)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def sdf_molecule_names(sdf_file: Path) -> list[str]:
    """Read molecule titles, which qparams uses as output file stems."""
    names = []
    for record in sdf_file.read_text().split("$$$$"):
        if not record.strip():
            continue
        lines = record.lstrip("\n").splitlines()
        name = lines[0].strip() if lines else ""
        if not name:
            raise ValueError(f"an unnamed molecule was found in {sdf_file}")
        names.append(name)
    if not names:
        raise ValueError(f"no molecules found in {sdf_file}")
    return names


def reparameterize_ligands(
    base: Path, destination: Path, qparams_args: list[str]
) -> list[list[str]]:
    """Regenerate every ligand set distributed with a baseline target."""
    source_sdfs = sorted(
        path
        for path in tracked_baseline_files(base)
        if path.parent == base and path.suffix == ".sdf"
    )
    if not source_sdfs:
        raise FileNotFoundError(f"no tracked ligand SDF files found in {base}")

    expected_names = []
    for source in source_sdfs:
        expected_names.extend(sdf_molecule_names(source))
    expected_names = list(dict.fromkeys(expected_names))

    # Remove copied parameter files first.  This ensures a successful check
    # proves qparams regenerated them instead of leaving baseline files behind.
    for name in expected_names:
        for suffix in (".pdb", ".lib", ".prm"):
            (destination / f"{name}{suffix}").unlink(missing_ok=True)

    commands = []
    for source in source_sdfs:
        commands.append(run_qparams(destination / source.name, destination, qparams_args))

    validate_ligand_parameters(destination, expected_names)
    validate_ligand_parameters(destination, mapped_ligands(destination / "mapping.json"))
    return commands


def copy_reparameterized_cofactors(target: str, qprep_dir: Path, destination: Path) -> None:
    """Keep the mutually consistent cofactor PDB, SDF and force field outputs."""
    if target not in COFACTOR_TARGETS:
        return
    cfg = COFACTOR_TARGETS[target]
    names = [cfg["sdf"].name, "all_cofactors.pdb", f"{cfg['ff']}.lib", f"{cfg['ff']}.prm"]
    for name in names:
        source = qprep_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"missing reparameterized cofactor artifact: {source}")
        shutil.copy2(source, destination / name)


def write_parameterization_manifest(destination: Path, commands: list[list[str]]) -> None:
    """Record the exact qparams argument vectors used to build a variant."""
    try:
        qligfep_version = version("qligfep")
    except PackageNotFoundError:
        qligfep_version = "unknown"
    payload = {
        "tool": "qparams",
        "qligfep_version": qligfep_version,
        "commands": commands,
    }
    (destination / "reparameterization.json").write_text(json.dumps(payload, indent=2) + "\n")


def patch_scripts(out_dir: Path, target: str, radius: float, reps: int) -> None:
    """Patch setup parameters, SLURM job names and target-specific result labels."""
    newname = f"{target}-{radius_label(radius)}A"
    scripts = sorted(out_dir.glob("*.sh"))
    if not scripts:
        raise FileNotFoundError(f"no submission scripts copied to {out_dir}")

    for script in scripts:
        text = script.read_text()
        text, radius_changes = SETUP_RADIUS_RE.subn(f"-r {radius_label(radius)}", text)
        text, reps_changes = SETUP_REPS_RE.subn(f"-R {reps}", text)
        if script.name.startswith("prepare") and (radius_changes == 0 or reps_changes == 0):
            raise ValueError(f"could not patch setupFEP radius and replicate count in {script}")
        script.write_text(text.replace(target, newname))


def copy_prep_metadata(source: Path, destination: Path) -> None:
    """Copy prep.json while pointing it at the variant's renamed protein PDB."""
    payload = json.loads(source.read_text())
    payload["prepared_pdb"] = "protein.pdb"
    destination.write_text(json.dumps(payload, indent=2) + "\n")


def build_target(
    target: str,
    radius: float,
    reps: int,
    force: bool = False,
    reparameterize: bool = False,
    qparams_args: list[str] | None = None,
) -> Path:
    """Create ``perturbations/<target>-<radius>A`` atomically from its baseline."""
    validate_baseline(target)
    base = PERT / target
    out_dir = PERT / f"{target}-{radius_label(radius)}A"
    if out_dir.exists() and not force:
        raise FileExistsError(
            f"{out_dir} already exists; move it aside or rerun with OVERWRITE=1/--force"
        )

    cog = read_cog(base / "water.pdb")
    with tempfile.TemporaryDirectory(prefix=f".{out_dir.name}.", dir=PERT) as temp:
        temp_dir = Path(temp)
        qprep_dir = temp_dir / "qprep"
        staging_dir = temp_dir / "output"
        qprep_dir.mkdir()

        prepared, water, metadata, commands = run_qprep(
            target,
            radius,
            cog,
            qprep_dir,
            reparameterize=reparameterize,
            qparams_args=qparams_args,
        )
        copy_baseline(base, staging_dir)
        if reparameterize:
            commands.extend(reparameterize_ligands(base, staging_dir, qparams_args or []))
            copy_reparameterized_cofactors(target, qprep_dir, staging_dir)
            write_parameterization_manifest(staging_dir, commands)
        shutil.copy2(prepared, staging_dir / "protein.pdb")
        shutil.copy2(water, staging_dir / "water.pdb")
        if metadata is not None:
            copy_prep_metadata(metadata, staging_dir / "prep.json")
        patch_scripts(staging_dir, target, radius, reps)

        previous = None
        if force and out_dir.exists():
            previous = temp_dir / "previous"
            out_dir.replace(previous)
        try:
            staging_dir.replace(out_dir)
        except Exception:
            if previous is not None and not out_dir.exists():
                previous.replace(out_dir)
            raise
    return out_dir


def main():
    radius, reps, selectors, force, reparameterize, qparams_args = parse_args(sys.argv[1:])
    try:
        targets = resolve_targets(selectors)
        for target in targets:
            validate_baseline(target)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        sys.exit(f"error: {exc}")
    if shutil.which("qprep_prot") is None:
        sys.exit(
            "error: qprep_prot is not available; activate QligFEP or set ENV to its "
            "micromamba environment"
        )
    if reparameterize and shutil.which("qparams") is None:
        sys.exit(
            "error: qparams is not available; activate QligFEP or set ENV to its "
            "micromamba environment"
        )

    print(
        f"Re-preparing {len(targets)} target(s) at {radius_label(radius)} A, "
        f"{reps} replicate(s): {', '.join(targets)}"
    )
    if reparameterize:
        rendered_args = shlex.join(qparams_args) if qparams_args else "<qparams defaults>"
        print(f"Reparameterizing ligands and cofactors with: {rendered_args}")
    failures = []
    for target in targets:
        try:
            out_dir = build_target(
                target,
                radius,
                reps,
                force=force,
                reparameterize=reparameterize,
                qparams_args=qparams_args,
            )
            print(f"  [ok]   {out_dir.relative_to(REPO_ROOT)}")
        except Exception as exc:  # continue so a batch reports every target failure
            failures.append((target, exc))
            print(f"  [FAIL] {target}: {exc}")

    if failures:
        print(f"\n{len(failures)} target(s) failed:")
        for target, exc in failures:
            print(f"  - {target}: {exc}")
        sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    main()
