#! /usr/bin/env python

import sys

all_asm_file=sys.argv[1]
vgp_asm_file=sys.argv[2]

f=open(vgp_asm_file)
vgp_asm=f.read().splitlines()
f.close()

f=open(all_asm_file)
data=f.read().splitlines()
f.close()
for line in data:
	items=line.split("\t")
	flag=items[5]
	if flag=="SC": flag="WELLCOME TRUST SANGER INSTITUTE"
	if items[0] in vgp_asm: flag="VGP"
	print("\t".join(items+[flag]))
	
