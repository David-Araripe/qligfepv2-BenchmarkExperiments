#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-24:00:00
#SBATCH -p rome
#SBATCH -J prep-tyk2
python -c "from QligFEP.chemIO import MoleculeIO;molio = MoleculeIO('ligands.sdf');molio.write_sdf_separate('.')"
micromamba run -n qligfep_new setupFEP -FF AMBER14sb -c SNELLIUS -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
