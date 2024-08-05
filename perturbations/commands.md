# bace

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_ls
```

Analyze the results
```bash
qligfep_analyze -t bace -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_bace && mv bace*  results_bace && cp lomap_ddG.json results_bace
```

# bace_hunt

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_ls
```

Analyze the results
```bash
qligfep_analyze -t bace_hunt -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_bace_hunt && mv bace_hunt*  results_bace_hunt && cp lomap_ddG.json results_bace_hunt
```

# bace_p2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_ls
```

Analyze the results
```bash
qligfep_analyze -t bace_p2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_bace_p2 && mv bace_p2*  results_bace_p2 && cp lomap_ddG.json results_bace_p2
```

# cdk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_ls
```

Analyze the results
```bash
qligfep_analyze -t cdk2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cdk2 && mv cdk2*  results_cdk2 && cp lomap_ddG.json results_cdk2
```

# cdk8

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_p
```

Analyze the results
```bash
qligfep_analyze -t cdk8 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cdk8 && mv cdk8*  results_cdk8 && cp lomap_ddG.json results_cdk8
```
# galectin

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t galectin -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_galectin && mv galectin*  results_galectin && cp lomap_ddG.json results_galectin
```
# jnk1

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t jnk1 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_jnk1 && mv jnk1*  results_jnk1 && cp lomap_ddG.json results_jnk1
```
# p38

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t p38 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_p38 && mv p38*  results_p38 && cp lomap_ddG.json results_p38
```
# pde2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t pde2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_pde2 && mv pde2*  results_pde2 && cp lomap_ddG.json results_pde2
```
# ptp1b

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t ptp1b -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_ptp1b && mv ptp1b*  results_ptp1b && cp lomap_ddG.json results_ptp1b
```
# syk

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t syk -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_syk && mv syk*  results_syk && cp lomap_ddG.json results_syk
```
# tnks2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t tnks2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_tnks2 && mv tnks2*  results_tnks2 && cp lomap_ddG.json results_tnks2
```
# bace_hunt

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t bace_hunt -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_bace_hunt && mv bace_hunt*  results_bace_hunt && cp lomap_ddG.json results_bace_hunt
```
# cdk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t cdk2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cdk2 && mv cdk2*  results_cdk2 && cp lomap_ddG.json results_cdk2
```
# cmet

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t cmet -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_cmet && mv cmet*  results_cmet && cp lomap_ddG.json results_cmet
```
# eg5

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t eg5 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_eg5 && mv eg5*  results_eg5 && cp lomap_ddG.json results_eg5
```
# hif2a

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t hif2a -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_hif2a && mv hif2a*  results_hif2a && cp lomap_ddG.json results_hif2a
```
# mcl1

Setup FEP's for target ✅
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest hybridization_ls
```

Analyze the results
```bash
qligfep_analyze -t mcl1 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_mcl1 && mv mcl1*  results_mcl1 && cp lomap_ddG.json results_mcl1
```
# pde10

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t pde10 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_pde10 && mv pde10*  results_pde10 && cp lomap_ddG.json results_pde10
```
# pfkfb3

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t pfkfb3 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_pfkfb3 && mv pfkfb3*  results_pfkfb3 && cp lomap_ddG.json results_pfkfb3
```
# shp2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t shp2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_shp2 && mv shp2*  results_shp2 && cp lomap_ddG.json results_shp2
```
# thrombin

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t thrombin -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_thrombin && mv thrombin*  results_thrombin && cp lomap_ddG.json results_thrombin
```
# tyk2

Setup FEP's for target
```bash
setupFEP -FF AMBER14sb -c TETRA -r 25 -b auto --start 0.5 -R 10 -S sigmoidal -ts 2fs -clean dcd -j lomap.json -log info -rest 
```

Analyze the results
```bash
qligfep_analyze -t tyk2 -j lomap.json -l debug -exp ddg_value -m ddGbar && mkdir -p results_tyk2 && mv tyk2*  results_tyk2 && cp lomap_ddG.json results_tyk2
```