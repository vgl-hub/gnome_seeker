#! /usr/bin/env python3.9

import sys

all_asm_file=sys.argv[1]
vgp_asm_file=sys.argv[2]

f=open(vgp_asm_file)
vgp_asm=f.read().splitlines()
f.close()

f=open(all_asm_file)
data=f.read().splitlines()
f.close()
total=[]
print("\t".join(["AssemblyAccession","AssemblyName","Organism","Taxid","assembly-status","SubmitterOrganization","representative-status","BioprojectAccn","BioprojectId","contig_n50","scaffold_n50","total_length","Taxon","quality","Project","Source"]))
for line in data:
	items=line.split("\t")
	total.append(items[0])
	flag=items[5]
	flag2="Others"
	if flag=="SC": flag="WELLCOME TRUST SANGER INSTITUTE"
	if items[0] in vgp_asm:
		flag="VGP"
		flag2="VGP"
	print("\t".join(items+[flag,flag2]))

for genome in vgp_asm:
	if genome not in total:
		print(genome)
	
