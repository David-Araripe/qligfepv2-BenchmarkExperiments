# Contents

- [JACS dataset](#jacs-dataset)
    - [bace](#bace)
    - [cdk2](#cdk2)
    - [jnk1](#jnk1)
    - [mcl1](#mcl1)
    - [p38](#p38)
    - [ptp1b](#ptp1b)
    - [thrombin](#thrombin)
    - [tyk2](#tyk2)
- [Merck dataset](#merck-dataset)
    - [cdk8](#cdk8)
    - [cmet](#cmet)
    - [eg5](#eg5)
    - [hif2a](#hif2a)
    - [shp2](#shp2)
    - [syk](#syk)
    - [pfkfb3](#pfkfb3)
    - [tnks2](#tnks2)

# JACS dataset

## bace

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t bace -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_bace && mv bace*  results_bace && cp mapping_ddG.json results_bace
```

## cdk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c SNELLIUS -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42 -wath 1.7
```

Analyze the results
```bash
qligfep_analyze -t cdk2 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_cdk2 && mv cdk2*  results_cdk2 && cp mapping_ddG.json results_cdk2
```

## jnk1

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t jnk1 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_jnk1 && mv jnk1*  results_jnk1 && cp mapping_ddG.json results_jnk1
```

## mcl1

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t mcl1 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_mcl1 && mv mcl1*  results_mcl1 && cp mapping_ddG.json results_mcl1
```

## p38

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t p38 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_p38 && mv p38*  results_p38 && cp mapping_ddG.json results_p38
```

## ptp1b

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c SNELLIUS -r 30 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -drf 1.5 -rs 42
```

Analyze the results
```bash
qligfep_analyze -t ptp1b -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose -v && mkdir -p results_ptp1b && mv ptp1b*  results_ptp1b && cp mapping_ddG.json results_ptp1b
```

## thrombin

<!-- Here we used our internally prepared structure. The overlap with the IndustryBenchmarks structures was very high, so we used the same ligands as in the dataset -->
```bash
setupFEP -FF AMBER14sb -c SNELLIUS -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t thrombin -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_thrombin && mv thrombin*  results_thrombin && cp mapping_ddG.json results_thrombin
```

## tyk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t tyk2 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_tyk2 && mv tyk2*  results_tyk2 && cp mapping_ddG.json results_tyk2
```

# Merck dataset

## cdk8

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c SNELLIUS -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t cdk8 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_cdk8 && mv cdk8*  results_cdk8 && cp mapping_ddG.json results_cdk8
```

## cmet

<!-- This target contains some perturbations that are quite challenging. Ring structure v.s. linear decoration
causes the restraints to be absent for a big part of the molecule. However, the space overlap is somewhat reasonable.
I expect some crashes... -->

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_ls -rs 42
```

Analyze the results
```bash
qligfep_analyze -t cmet -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_cmet && mv cmet*  results_cmet && cp mapping_ddG.json results_cmet
```

## eg5

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t eg5 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_eg5 && mv eg5*  results_eg5 && cp mapping_ddG.json results_eg5
```

## hif2a

<!-- These compounds have a common core ring in the series, but it's broken in one of the ligands. This results in very few atoms being mapped. I'll try heavyatom_p and if not, should do `kartograf` (update, the results seem ok) -->

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t hif2a -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_hif2a && mv hif2a*  results_hif2a && cp mapping_ddG.json results_hif2a
```

## shp2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p_1.2 -rs 42
```

Analyze the results
```bash
qligfep_analyze -t shp2 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_shp2 && mv shp2*  results_shp2 && cp mapping_ddG.json results_shp2
```

## syk

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t syk -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_syk && mv syk*  results_syk && cp mapping_ddG.json results_syk
```

## pfkfb3

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

## tnks2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c DARDEL -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest heavyatom_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t tnks2 -j mapping.json -log debug -exp ddg_value -m ddGbar -lamb 101 --save-verbose && mkdir -p results_tnks2 && mv tnks2*  results_tnks2 && cp mapping_ddG.json results_tnks2
```