#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-1:00:00
#SBATCH -p rome
#SBATCH -J res-cdk2
micromamba run -n qligfep_new qligfep_analyze -t cdk2 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_cdk2 && mv cdk2*  results_cdk2 && cp mapping_ddG.json results_cdk2
