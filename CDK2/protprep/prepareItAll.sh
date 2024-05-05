rm *_withLigands.pdb complexnotexcluded.pdb qprep_* dualtop.top top_p.pdb  water.pdb

qprep_prot -i CDK2_protein_mini_renamed.pdb -cog 0.893 26.52 8.756 -log debug
qprep_prot -i CDK2_protein_mini_renamed.pdb -lig ../CDK2_ligands.sdf -t protein -sp 2.5 -cog 0.893 26.52 8.756 -log debug

