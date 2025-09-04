#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-1:00:00
#SBATCH -p rome
#SBATCH -J res-cdk8
micromamba run -n qligfep_new qligfep_analyze -t cdk8 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_cdk8 && mv cdk8*  results_cdk8 && cp mapping_ddG.json results_cdk8
