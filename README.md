# QligFEPv2 Benchmarking Experiments

This repository contains the benchmarking experiments for the QligFEPv2 software for relative binding free energy (RBFE) calculations.

In this repostory you can find:
- The starting structures used as inputs to run the RBFE calculations;
- Scripts for preparing the systems and the RBFE network for each target;
- A dash app to interactively visualize the results of the benchmarking experiments, including starting poses of protein structures, ligands, and the calculated RBFE values.

# FEPviz

The FEPviz is a dash app that allows the interactive visualization of the results of the benchmarking experiments. The app is available on `app.py` and requires the following packages to be installed:

```bash
python -m pip install git+https://github.com/David-Araripe/SFC_FreeEnergyCorrection.git git+https://github.com/David-Araripe/Weighted_cc.git git+https://github.com/David-Araripe/chemFilters.git dash cinnabar dash-molstar dash-bootstrap-components statannotations statsmodels fastparquet tabulate
```

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

**Ligand Changes**

An additional change was introduced to the input ligand structures. We noticed poorer correlation with the experimental data when using the ligands from the `IndustryBenchmarks2024` repository. Ligand `17` in the series contains a halogen meta-substituted phenyl ring, pointing towards the solvent. The protein structure `6GUK`, though different from the ligand in question, displays a different rotamer pointing towards the cyclohexyl group, less solvent-exposed. The space where the chlorine group is positioned in this deposited structure has an [overlap](https://www.ebi.ac.uk/pdbe/entry/view3D/6guk/?view=entry_index&viewer=litemol&assembly=1) of both 2Fo-Fc $\sigma$ and Fo-Fc(-ve) $\sigma$ maps, indicating an uncertainty in the positioning of the halogen atom. However, we assumed the rotamer conformation to have contributed for the poor correlation between QligFEP results with the experimental data and decided to use poses with the halogen pointing towards the cyclohexyl group.

<!-- For a quick visualization of the deposited protein structure illustrating this binding pose, see:

```python
import py3Dmol

viewer = py3Dmol.view(query="pdb:6GUK")
viewer.setStyle({"model": 0, "not resn": "FC8"}, {"cartoon": {"color": "gray"}})
viewer.setStyle(
    {"model": 0, "resn": "FC8"},
    {"stick": {"colorscheme": "greenCarbon", "radius": 0.3}},
)
viewer.addSurface(
    py3Dmol.VDW, {"opacity": 0.5, "color": "white"}, {"not": {"resn": "FC8"}}
)
viewer.zoomTo({"resn": "FC8"})
viewer.show()
``` -->

### jnk1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```GLY35, VAL40, LEU110, MET111, ALA113```

### mcl1

All ligands and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```VAL253, MET231, LEU246, LEU290, ILE294, LEU267, MET250, VAL274, LEU235, PHE270, GLY271```

### p38

No manual minimization performed. Bad clashes were only observed against water molecules, which are automatically removed before QligFEP RBFE simulations.

### ptp1b

Prepared protein from the source repository displayed poor correlation with the experimental data. Therefore, we proceeded to use an internally prepared structure by us, generated before this study was conducted and known to work well with QligFEP RBFE calculations.

Upon checking the ligands, we noticed a need for optimization of the ligand poses. Despite the good MCS alignment for the scaffold shared by the ligands, other parts of the ligand weren't so well aligned. Therefore, we decided to perform a few additional alignments on top of the ligand preparation on IndustryBenchmarks2024 repository. The changes can be found in our [ligand alignment notebook](startFiles/ligand_alignment.ipynb).

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

Ligands `20`, `41`, and `42` and respective protein structure were loaded in `Maestro`. A minimization step was applied to the following residues by manually selecting them and minimizing with the `Ctrl + m` command:
```val214```

Following that, ligands `44`, `47`, `52`, `53` were loaded. A second minimization step was applied to the folliwng residues by manually selecting them and minimizing with the `Ctrl + m` command:
```leu238, ile241, his242```

The following water molecules were removed: `905, 914, 944, 993, 998, 1022`, as they were clashing with other HOH `O` atoms and not the closest to the protein residues.

Removed the atoms:
```txt
ATOM      1  CH3 ACE A   0      87.427  98.432 260.536  1.00  0.00           C  
ATOM      2  C   ACE A   0      86.302  98.808 261.499  1.00  0.00           C  
ATOM      3  O   ACE A   0      85.472  97.963 261.827  1.00  0.00           O  
ATOM      4 1H   ACE A   0      87.325  97.362 260.246  1.00  0.00           H  
ATOM      5 2H   ACE A   0      87.370  99.072 259.627  1.00  0.00           H  
ATOM      6 3H   ACE A   0      88.411  98.593 261.030  1.00  0.00           H  
...
ATOM    284  N   NME A  16A     79.441  97.537 254.883  1.00  0.00           N  
ATOM    285  CA  NME A  16A     80.445  98.441 254.341  1.00  0.00           C  
ATOM    286  H   NME A  16A     78.820  97.041 254.262  1.00  0.00           H  
ATOM    287 1HA  NME A  16A     81.022  98.883 255.184  1.00  0.00           H  
ATOM    288 2HA  NME A  16A     81.132  97.880 253.668  1.00  0.00           H  
ATOM    289 3HA  NME A  16A     79.949  99.249 253.759  1.00  0.00           H  
```

**Ligand Changes**

An additional change was introduced to the input ligand structures. We noticed poorer correlation with the experimental data for the edges including ligand `43` from the `IndustryBenchmarks2024` repository. This ligand in the series contains a halogen (`Br`) meta-substituted phenyl ring, pointing towards the solvent. The protein structure `6HVI` [with the co-crystalized ligand](https://www.ebi.ac.uk/pdbe/entry/view3D/6hvi/?view=entry_index&viewer=litemol&assembly=1) `38` of the congeneric series also contains a meta-substitution of the phenyl ring, but on the opposite orientation than ligand 43. Therefore, we decided to flip the cyclohexyl group in ligand 43 to match the observed orientation in the protein structure. Doing so, we observed a better correlation between the calculated and experimental data, supporting the decision to use this pose.

<!-- ```python
import py3Dmol

viewer = py3Dmol.view(query="pdb:6HVI")
viewer.setStyle(
    {"model": 0, "not resn": "GV5"},
    {"cartoon": {"colorscheme": "gray"}},
)
viewer.setStyle(
    {"model": 0, "resn": "GV5"},
    {"stick": {"colorscheme": "greenCarbon", "radius": 0.3}},
)
viewer.addSurface(
    py3Dmol.VDW, {"opacity": 0.5, "color": "white"}, {"not": {"resn": "GV5"}}
)
viewer.zoomTo({"resn": "GV5"})
viewer.show()
``` -->

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

No manual minimization performed.
