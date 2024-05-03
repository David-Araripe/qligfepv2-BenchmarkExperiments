# openff220-startfiles
So I can run my FEP calculations

# JACS Protein System Preparations

Notes on the settings:
- `2fs` calculations are default on the CLI, and this setting is not explicitly mentioned in the commands below.
- Same goes for the `-T 298` setting.

## BACE
``` bash
qligfep -l1 CAT-13o -l2 CAT-24 -FF AMBER14sb -s protein -c TETRA -R 10 -S sigmoidal -r 25 -l 0.5 -w 100 -T 298 -b 2442_5627,3403_5974,4220_5016

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -b 2442_5627,3403_5974,4220_5016 -j lomap.json -S sigmoidal -clean dcd
```
## CDK2
``` bash
qligfep -l1 17 -l2 1oiu -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## JNK1
``` bash
qligfep -l1 17124-1 -l2 18637-1 -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```
Note -> had to remove the final modified residue from the pdb file (`ERROR: Residue number   369 is of unknown type CPHE`)

used `pdb2amber` command to fix the atom naming; used a script to correctly format the `.pdb` file. (atom naming not aligned to the left in the PDB)

## MCL1

``` bash
qligfep -l1 23 -l2 66 -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

Note -> used `pdb2amber` command to fix the atom naming; used a script to correctly format the `.pdb` file. (atom naming not aligned to the left in the PDB)

## PTP1B

``` bash
qligfep -l1 '20667-2qbp' -l2 '23482' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```
Notes: used `pdb2amber` command to fix the atom naming; used a script to correctly format the `.pdb` file. (atom naming not aligned to the left in the PDB)

## Thrombin

``` bash
qligfep -l1 '1a' -l2 '1b' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein -b 1089_1322,3452_3684,3878_4316

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd -b 1089_1322,3452_3684,3878_4316
```
Notes: used `pdb2amber` command to fix the atom naming; used a script to correctly format the `.pdb` file. (atom naming not aligned to the left in the PDB)

## Tyk2

``` bash
qligfep -l1 'ejm_31' -l2 'ejm_45' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## p38

``` bash
qligfep -l1 'p38a_2aa' -l2 'p38a_3flw' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

# Analysis dataset

``` bash
qligfep_analyze -t BACE -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsBACE && mv BACE* resultsBACE
qligfep_analyze -t CDK2 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsCDK2 && mv CDK2* resultsCDK2
qligfep_analyze -t JNK1 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsJNK1 && mv JNK1* resultsJNK1
qligfep_analyze -t MCL1 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsMCL1 && mv MCL1* resultsMCL1
qligfep_analyze -t PTP1B -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsPTP1B && mv PTP1B* resultsPTP1B
qligfep_analyze -t Thrombin -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsThrombin && mv Thrombin* resultsThrombin
qligfep_analyze -t Tyk2 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsTyk2 && mv Tyk2* resultsTyk2
qligfep_analyze -t p38 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsp38 && mv p38* resultsp38
```
# Merk Protein System Preparations

- All the protein files were passed through `fix_indentation.py` to fix the atom type indentation (aligned to the left in the PDB file). Then, the `pdb2amber` command was used to fix the atom naming.

## cdk8
``` bash
qligfep -l1 '13' -l2 '43' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## cmet
``` bash
qligfep -l1 'CHEMBL3402741_400' -l2 'CHEMBL3402742_23' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## eg5
``` bash
qligfep -l1 'CHEMBL1077204' -l2 'CHEMBL1085692' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## hif2a
``` bash
qligfep -l1 '1' -l2 '84' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## pfkfb3
``` bash
qligfep -l1 '19' -l2 '24' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## shp2
``` bash
qligfep -l1 '10' -l2 'Example_30' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## syk
``` bash
qligfep -l1 'CHEMBL3259820' -l2 'CHEMBL3265005' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

## tnks2
``` bash
qligfep -l1 '1a' -l2 '5a' -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -S sigmoidal -clean .dcd -s protein

setupFEP -FF AMBER14sb -c TETRA -r 25 -l 0.5 -R 10 -w 100 -j lomap.json -S sigmoidal -clean .dcd
```

# Analysis dataset

``` bash
qligfep_analyze -t cdk8 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultscdk8 && mv cdk8* resultscdk8
qligfep_analyze -t cmet -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultscmet && mv cmet* resultscmet
qligfep_analyze -t eg5 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultseg5 && mv eg5* resultseg5
qligfep_analyze -t hif2a -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultshif2a && mv hif2a* resultshif2a
qligfep_analyze -t pfkfb3 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultspfkfb3 && mv pfkfb3* resultspfkfb3
qligfep_analyze -t shp2 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultsshp2 && mv shp2* resultsshp2
qligfep_analyze -t syk -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultssyk && mv syk* resultssyk
qligfep_analyze -t tnks2 -j lomap.json -l DEBUG -exp delta_r_user_dG.exp -m ddGbar && mkdir resultstnks2 && mv tnks2* resultstnks2
