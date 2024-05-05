rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i BACE_modif_renamed.pdb -cog 14.917 -1.542 -0.993 -log debug
qprep_prot -i BACE_modif_renamed.pdb -lig ../BACE_ligands_aligned.sdf -t protein -sp 2.5 -cog 14.917 -1.542 -0.993 -log debug
