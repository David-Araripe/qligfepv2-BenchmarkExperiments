#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-24:00:00
#SBATCH -J prepneq-bace
# NEQ2 FEP setup, run in place of prepare.sh (see ../commands.md for the protocol).
# No partition is set; add "#SBATCH -p <partition>" above if your cluster needs one.
micromamba run -n qligfep_new python -c "from QligFEP.chemIO import MoleculeIO;molio = MoleculeIO('ligands.sdf');molio.write_sdf_separate('.')"
micromamba run -n qligfep_new setupFEP -FF AMBER14sb -c SNELLIUS -r 25 -b auto --start 0.5 -R 10 -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42 -T 300 --neq --neq-reps 5 --neq-steps 50000 --neq-eq-steps 1000 --neq-relax-steps 5000 -L 8.0 --neq-schedule sigmoidal
