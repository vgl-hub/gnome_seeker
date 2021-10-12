#! /usr/bin/env python

import sys,glob

contigN50_min=1000000
scaffoldN50_min=10000000


vgplist=[]
f=open("VGP.list")
data=f.read().splitlines()
f.close()
for line in data: vgplist.append(line.split(" ")[0])


fileName=sys.argv[1]

f=open(fileName)
data=f.read().splitlines()
f.close()

#filter for N50 and format NCBI output into a table of dictionary
table=[]
for line in data:
	items=line.split("\t")
	res={}
	#print(items)
	for item in items:
		#print(item)
		res[item.split(":")[0]]=item.split(":")[1]
		#res["species"]=items[2].split(" (")[0]
		#res["common"]=items[2].split(" (")[1].rstrip(")")
	if float(res["contig_n50"])>=contigN50_min and float(res["scaffold_n50"])>=scaffoldN50_min:
		table.append(res)

#print(table)

# collapse
filtered={}
filtered2=[]
for entry in table: filtered.setdefault(entry["Taxid"],[]).append(entry)
for taxId in filtered.keys():
	if len(filtered[taxId])==1:
		j=filtered[taxId][0]
	else:
		jj=0
		for i in range(len(filtered[taxId])):
			if filtered[taxId][i]["representative-status"]=="representative genome": jj=i
		j=filtered[taxId][jj]
	filtered2.append(j)

cols=["AssemblyAccession","AssemblyName","Organism","Taxid","assembly-status","SubmitterOrganization","representative-status","BioprojectAccn","contig_n50","scaffold_n50"]
#print("\t".join(cols))
for i in filtered2:
	flag="non-VGP"
	if i["AssemblyAccession"] in vgplist: flag="VGP"
	print("\t".join([i[x] for x in cols]+[flag]))