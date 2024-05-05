rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i JNK1_protein_mini_renamed.pdb -cog 22.607 7.337 31.361 -log debug
qprep_prot -i JNK1_protein_mini_renamed.pdb -lig ../JNK1_ligands_aligned.sdf -t protein -sp 2.5 -cog 22.607 7.337 31.361 -log debug
