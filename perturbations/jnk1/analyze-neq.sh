#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1024
#              d-hh:mm:ss
#SBATCH --time=0-1:00:00
#SBATCH -J resneq-jnk1
# BAR analysis of the NEQ2 switching work from prepare-neq.sh (see ../commands.md for the protocol).
# No partition is set; add "#SBATCH -p <partition>" above if your cluster needs one.
micromamba run -n qligfep_new qligfep_neq_analyze -p 2.protein -w 1.water -T 300 -u kcal -j mapping.json -exp ddg_value -t jnk1 -o jnk1_neq_results.csv -log debug && mkdir -p results_jnk1_neq && mv jnk1_neq* results_jnk1_neq && cp mapping.json results_jnk1_neq
