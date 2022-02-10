#! /usr/bin/env python3.9

import sys,os

contigN50_min=1000000
scaffoldN50_min=10000000

def translate(taxon):
	t={"Actinopteri":"Bony fishes","Amphibia":"Amphibians","Aves":"Birds","Chondrichthyes":"Cartilaginous fishes","Cladistia":"Bony fishes","Coelacanthimorpha":"Bony fishes","Cyclostomata":"Jawless","Dipnoi":"Bony fishes","Mammalia":"Mammals","Reptilia":"Reptiles"}
	if taxon in t.keys(): return t[taxon]
	return taxon

def collapse(table):
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
	return filtered2

fileName=sys.argv[1]

f=open(fileName)
data=f.read().splitlines()
f.close()

#filter for N50 and format NCBI output into a table of dictionary
table=[]
for line in data:
	items=line.split("\t")
	res={}
	for item in items:
		res[item.split(":")[0]]=item.split(":")[1]
	for x in ["AssemblyAccession","AssemblyName","Organism","Taxid","assembly-status","SubmitterOrganization","representative-status","BioprojectAccn","BioprojectId","contig_n50","scaffold_n50","total_length"]:
		if x not in res.keys(): res[x]=""
	taxon_temp=os.path.basename(fileName).split(".")[0]
	res["Taxon"]=translate(taxon_temp)
	if float(res["contig_n50"])>=contigN50_min and float(res["scaffold_n50"])>=scaffoldN50_min:
		res["quality"]="high"
	else:
		res["quality"]="low"
	table.append(res)

# collapse
filtered=collapse(table)

#print(filtered)
cols=["AssemblyAccession","AssemblyName","Organism","Taxid","assembly-status","SubmitterOrganization","representative-status","BioprojectAccn","BioprojectId","contig_n50","scaffold_n50","total_length","Taxon","quality"]
for i in filtered:
	print("\t".join([i[x] for x in cols]))