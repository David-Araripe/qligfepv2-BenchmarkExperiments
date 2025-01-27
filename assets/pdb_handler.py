import string
import numpy as np
import pandas as pd
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem


def read_pdb_to_dataframe(pdb_file):
    columns = [
        "record_type",
        "atom_serial_number",
        "atom_name",
        "alt_loc",
        "residue_name",
        "chain_id",
        "residue_seq_number",
        "insertion_code",
        "x",
        "y",
        "z",
        "occupancy",
        "temp_factor",
        "segment_id",
        "element_symbol",
        "charge",
    ]
    data = []
    with open(pdb_file, "r") as file:
        for line in file:
            if line.startswith(("ATOM", "HETATM")):
                parsed_line = [
                    line[0:6].strip(),  # record_type
                    int(line[6:11].strip()),  # atom_serial_number
                    line[12:16].strip(),  # atom_name
                    line[16].strip(),  # alt_loc
                    line[17:20].strip(),  # residue_name
                    line[21].strip(),  # chain_id
                    int(line[22:26].strip()),  # residue_seq_number
                    line[26].strip(),  # insertion_code
                    float(line[30:38].strip()),  # x
                    float(line[38:46].strip()),  # y
                    float(line[46:54].strip()),  # z
                    float(line[54:60].strip()),  # occupancy
                    float(line[60:66].strip()),  # temp_factor
                    line[72:76].strip(),  # segment_id
                    line[76:78].strip(),  # element_symbol
                    line[78:80].strip(),  # charge
                ]
                data.append(parsed_line)
    df = pd.DataFrame(data, columns=columns)
    return df


def write_dataframe_to_pdb(df, output_file):
    with open(output_file, "w") as file:
        for index, row in df.iterrows():
            pdb_line = (
                f"{row['record_type']:<6}{row['atom_serial_number']:>5} "
                f"{row['atom_name']:<4}{row['alt_loc']:<1}{row['residue_name']:>3} "
                f"{row['chain_id']:>1}{row['residue_seq_number']:>4}{row['insertion_code']:>1}   "
                f"{row['x']:>8.3f}{row['y']:>8.3f}{row['z']:>8.3f}{row['occupancy']:>6.2f}"
                f"{row['temp_factor']:>6.2f}          {row['element_symbol']:>2}{row['charge']:>2}\n"
            )
            file.write(pdb_line)


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


def merge_protein_lig(protein_pdb, lig_pdb, save_pdb, new_ligname="LIG"):
    prot_df = read_pdb_to_dataframe(protein_pdb)
    lig_df = read_pdb_to_dataframe(lig_pdb)

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
