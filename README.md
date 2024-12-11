# QligFEPv2 Benchmarking Experiments

This repository contains the benchmarking experiments for the QligFEPv2 software for relative binding free energy (RBFE) calculations.

In this repostory you can find:
- The starting structures used as inputs to run the caluculations;
- Scripts for preparing the systems and the RBFE network for each target;
- Obtained results;

- Details;
... Add structure of the repository here;

## JACS Benchmark set;

The JACS benchmark set is a set of 8 protein-ligand systems used to benchmark the QligFEPv2 software. The prepared ligands/structures used for our calculations are the same reported in the [IndustryBenchmark2024](https://github.com/OpenFreeEnergy/IndustryBenchmarks2024/) repository, with exception of Thrombin, which was prepared by us.

Here you can find the modifications applied to each of the targets obtained from the original repository:

### bace

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```ILE171, SER96, SER71, PHE169, GLY291```

### cdk2

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```LYS89, ASP86, LEU138```

N-terminal of Chain A was also minimized to remove a clash leading to infinite VDW potentials.

### jnk1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```GLY35, VAL40, LEU110, MET111, ALA113```

### mcl1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```VAL253, MET231, LEU246, LEU290, ILE294, LEU267, MET250, VAL274, LEU235, PHE270, GLY271```

### p38

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### ptp1b

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### thrombin

The protein found in the source repository contained some hydrogen positioning problems, which we attempted to fix using Maestro's `Refine > H-bond-assignment` tool. Further, some amino acids were placed in the sequence in the incorrect order. Those were fixed by manually reordering them.

The resulting structure, however, resulted in crashes during the FEP, which wasn't observed for any of the other targets used in this study. Therefore, we proceeded to use an internally prepared structures by us.

### tyk2

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```LEU903, TYR980, GLY984, PRO982```

## Merck Benchmark set;

### cdk8
All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```val27, gly28, tyr32, lys52, ile79, his102, asp103, asn156, leu158, arg356```

### cmet
All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```ile1084, gly1085, met1160, lys1161```

### eg5
All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```arg119, pro121, leu160, gly217, ala218```

### hif2a
```met289, his293, cys339```

### pfkfb3


### shp2
`phe113, his114, thr219, glu249, asp489, lys492`

### syk
The following residues were minimized to better accommodate the ligands in the binding site:
`glu376, leu377, gly378, val385, asn457, asp512, phe513, lys402, gly454, ser379, lys375, phe382, lys458`

Further, other amino acids were minimized to avoid protein-protein clashes.

Finally, the orientation of the protein's hydrogen atoms were refined using Maestro's `Refine > H-bond-assignment` tool by checking the boxes:

- [x] Sample water orientations
- [x] Use PROPKA pH: 7.0

### tnks2