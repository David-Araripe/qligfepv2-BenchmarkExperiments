"""Script to separate sdf files into individual files containing the ligands."""

from pathlib import Path
from QligFEP.chemIO import MoleculeIO

directories = [d for d in Path().glob("*/") if d.is_dir()]
for _dir in directories:
    ligand_path = _dir / "ligands.sdf"
    try:
        ligsIO = MoleculeIO(ligand_path)  # save mols in separate sfd files
        ligsIO.write_sdf_separate(_dir)
    except ValueError:
        print(f'no ligands for {ligand_path}. Continuing...')
