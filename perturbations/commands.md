# cdk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest aromaticity_ls -rs 42
```

Analyze the results
```bash
qligfep_analyze -t cdk2 -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cdk2 && mv cdk2*  results_cdk2 && cp mapping_ddG.json results_cdk2
```

# cdk8

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t cdk8 -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cdk8 && mv cdk8*  results_cdk8 && cp mapping_ddG.json results_cdk8
```

# cmet

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# p38

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t p38 -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_p38 && mv p38*  results_p38 && cp mapping_ddG.json results_p38
```

# pfkfb3

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# syk

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# thrombin

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_ls -rs 42
```

Analyze the results
```bash
qligfep_analyze -t thrombin -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_thrombin && mv thrombin*  results_thrombin && cp mapping_ddG.json results_thrombin
```

# tyk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t tyk2 -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_tyk2 && mv tyk2*  results_tyk2 && cp mapping_ddG.json results_tyk2
```

# cdk8

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# eg5

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# hif2a

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# mcl1

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest hybridization_ls -rs 42
```

Analyze the results
```bash
qligfep_analyze -t mcl1 -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_mcl1 && mv mcl1*  results_mcl1 && cp mapping_ddG.json results_mcl1
```

# pde2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# ptp1b

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest aromaticity_p -rs 42
```

Analyze the results
```bash
qligfep_analyze -t ptp1b -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_ptp1b && mv ptp1b*  results_ptp1b && cp mapping_ddG.json results_ptp1b
```

# shp2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```

# tnks2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd inp -j mapping.json -log info -rest DEFINE -rs 42
```

Analyze the results
```bash
qligfep_analyze -t TARGET -j mapping.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_TARGET && mv TARGET*  results_TARGET && cp mapping_ddG.json results_TARGET
```