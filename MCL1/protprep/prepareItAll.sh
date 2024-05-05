rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i MCL1_modif_renamed.pdb -cog -2.059 -47.508 6.828 -log debug
qprep_prot -i MCL1_modif_renamed.pdb -lig ../MCL1_aligned_ligands_modif.sdf -t protein -sp 2.5 -cog -2.059 -47.508 6.828 -log debug
