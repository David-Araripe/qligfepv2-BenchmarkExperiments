# QligFEPv2 Benchmarking Experiments

This repository contains the benchmarking experiments for the QligFEPv2 software for relative binding free energy (RBFE) calculations.

In this repostory you can find:
- The starting structures used as inputs to run the caluculations;
- Scripts for preparing the systems and the RBFE network for each target;
- Obtained results;

- Details;
... Add structure of the repository here;

## JACS Benchmark set;

The JACS benchamrk set is a set of 8 protein-ligand systems used to benchmark the QligFEPv2 software. The prepared ligands/structures used for our calculations are the same reported in the [IndustryBenchmark2024](https://github.com/OpenFreeEnergy/IndustryBenchmarks2024/) repository.

Here you can find the modifications applied to each of the targets obtained from the original repository:

### BACE

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```ILE171, SER96, SER71, PHE169, GLY291```

### CDK2

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```LYS89, ASP86, LEU138```

### JNK1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```GLY35, VAL40, LEU110, MET111, ALA113```

### MCL1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```VAL253, MET231, LEU246, LEU290, ILE294, LEU267, MET250, VAL274, LEU235, PHE270, GLY271```

### p38

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### PTP1B

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### Thrombin

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### Tyk2

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```LEU903, TYR980, GLY984, PRO982```
