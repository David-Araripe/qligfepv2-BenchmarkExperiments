import string
from typing import Union
import numpy as np
import pandas as pd
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
from QligFEP.pdb_utils import read_pdb_to_dataframe, write_dataframe_to_pdb


def create_pdb_ligand_files(root_path: Path, overwrite: bool = False) -> None:
    """finds all .sdf filed, and writes a pdb file for each one.

    Args:
        root_path: root with the sdf files
        overwrite: if you want... Defaults to False.
    """
    for sdf_file in root_path.glob("*.sdf"):
        if sdf_file.stem.endswith("_ligands"):
            continue
        pdb_file = root_path / (sdf_file.stem + ".pdb")
        if pdb_file.exists() and not overwrite:
            continue
        sdf_to_pdb(sdf_file, pdb_file)


def sdf_to_pdb(in_sdf_file, out_pdb_file):
    """Converts an SDF file to a PDB file.

    Args:
        in_sdf_file: std_in; path with the sdf file
        out_pdb_file: std_out; path for the pdb file
    """
    suppl = Chem.SDMolSupplier(in_sdf_file)
    for mol in suppl:
        if mol is not None:
            # Generate 3D coordinates if not present
            mol_with_h = Chem.AddHs(mol, addCoords=True)
            AllChem.MMFFOptimizeMolecule(mol_with_h, maxIters=200)
            for atom in mol_with_h.GetAtoms():
                pass
            with open(out_pdb_file, "w") as f:
                print("overwriting")
                f.write(Chem.MolToPDBBlock(mol_with_h))
            break  # there's only one per sdf anyways...


def merge_protein_lig(
    protein_pdb: Union[Path, pd.DataFrame, str],
    lig_pdb: Union[Path, pd.DataFrame, str],
    save_pdb: Path,
    new_ligname="LIG",
):
    prot_df = read_pdb_to_dataframe(protein_pdb) if isinstance(protein_pdb, Path) else protein_pdb
    lig_df = read_pdb_to_dataframe(lig_pdb) if isinstance(lig_pdb, Path) else lig_pdb

    # Determine the new chain ID for the ligand
    existing_chain_ids = set(prot_df["chain_id"].replace({"": np.nan}).dropna().unique())
    if not existing_chain_ids:
        prot_df["chain_id"] = "A"  # Default the protein to chain A if no chain_id is present
        new_chain_id = "B"
    else:
        new_chain_id = next_chain_id(existing_chain_ids)

    last_prot_atom = prot_df["atom_serial_number"].astype(int).max()
    last_prot_resn = prot_df["residue_seq_number"].astype(int).max()

    lig_df = lig_df.assign(
        atom_serial_number=(lig_df["atom_serial_number"].astype(int) + last_prot_atom).astype(str),
        residue_seq_number=(lig_df["residue_seq_number"].astype(int) + last_prot_resn).astype(str),
        residue_name=new_ligname,
        chain_id=new_chain_id,
    )

    merged_df = pd.concat([prot_df, lig_df], ignore_index=True)
    write_dataframe_to_pdb(merged_df, save_pdb)
    return merged_df


def next_chain_id(existing_ids):
    """
    Calculate the next chain ID based on existing IDs.
    Wrap around to 'A' after 'Z', and ensure uniqueness.
    """
    alphabet = list(string.ascii_uppercase)
    if not existing_ids:
        return "A"
    # Find the highest current chain_id and increment
    highest_id = max([alphabet.index(cid) for cid in existing_ids if cid in alphabet], default=-1)
    next_id_index = (highest_id + 1) % len(alphabet)
    return alphabet[next_id_index]
