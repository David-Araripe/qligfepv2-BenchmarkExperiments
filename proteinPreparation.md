# BACE
```bash
rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i BACE_modif_renamed.pdb -cog 14.917 -2.542 -0.993 -log debug
qprep_prot -i BACE_modif_renamed.pdb -lig ../BACE_ligands_aligned.sdf -t protein -sp 2.5 -cog 14.917 -2.542 -0.993 -log debug
```
# CDK2
```bash
rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i CDK2_protein_mini_renamed.pdb -cog 0.893 26.52 8.756 -log debug
qprep_prot -i CDK2_protein_mini_renamed.pdb -lig ../CDK2_ligands.sdf -t protein -sp 2.5 -cog 0.893 26.52 8.756 -log debug
```
# JNK1
```bash
rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i JNK1_protein_mini_renamed.pdb -cog 22.607 7.337 31.361 -log debug
qprep_prot -i JNK1_protein_mini_renamed.pdb -lig ../JNK1_ligands_aligned.sdf -t protein -sp 2.5 -cog 22.607 7.337 31.361 -log debug
```
# MCL1
```bash
rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i MCL1_modif_renamed.pdb -cog -2.059 -47.508 6.828 -log debug
qprep_prot -i MCL1_modif_renamed.pdb -lig ../MCL1_aligned_ligands_modif.sdf -t protein -sp 2.5 -cog -2.059 -47.508 6.828 -log debug
```


