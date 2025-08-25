
#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-1:00:00
#SBATCH -p rome
#SBATCH -J res-ptp1b
micromamba run -n qligfep_analyze -t ptp1b -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose -v && mkdir -p results_ptp1b && mv ptp1b*  results_ptp1b && cp mapping_ddG.json results_ptp1b
