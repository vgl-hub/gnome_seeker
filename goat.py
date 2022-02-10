#! /usr/bin/env python

import sys
import urllib3,json
import requests
import edtools

filename=" ".join(sys.argv[1:])
f = open(filename, 'r')
speciesList = f.read().splitlines()
f.close()

outfile = open(filename+".output", 'w')
notfound=[]
nospecies=[]
#print("\t".join(["query","scientific_name","common_name","taxon_id","synonym","class","order","family","genome_size"]))
outfile.write("\t".join(["query","scientific_name","common_name","taxon_id","synonym","class","order","family","genome_size"]))
for line in speciesList[1:]:
	species=line.split("\t")[0]
	items=species.split(" ")
	#print(line)
	if len(items)==1:
		nospecies.append(line+"\tnot found")
		res=[",".join(line.split("\t"))]+["" for i in range(8)]
		#print("\t".join(res))
		outfile.write("\n"+"\t".join(res))
	else:
		subspecies=""
		#species=" ".join(items[0:2])
		#print(species)
		if len(items)>2: subspecies=items[2]
		err=None
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		species_search="+".join(species.split(" ")[0:2])
		results=edtools.list_to_dict([],[])
		baseurl="https://goat.genomehubs.org/api/v0.0.1/lookup?"
		PARAMS={"searchTerm":species_search,"size":"1","taxonomy":"ncbi","maxErrors":"0","result":"multi"}
		response_ = requests.get(url=baseurl,params=PARAMS)
		data_=response_.json()
		output={"taxon_id":"","family":"","order":"","class":"","genome_size":"","scientific_name":"","common_name":[],"VGP_Id":"","synonym":[]}
		if len(data_.keys())>0:
			output["taxon_id"]=data_["results"][0]["result"]["taxon_id"]
			output["scientific_name"]=data_["results"][0]["result"]["scientific_name"]
			goat_id=data_["results"][0]["id"]
			for i in data_['results'][0]['result']['taxon_names']:
				if i["class"]=="synonym": output["synonym"].append(i["name"])
				if i["class"]=="tol_id": output["VGP_Id"]=i["name"]
				if i["class"]=="genbank common name" or  i["class"]=="common_name": output["common_name"].append(i["name"])
			baseurl="https://goat.genomehubs.org/api/v0.0.1/record?"
			PARAMS={"recordId":str(goat_id),"taxonomy":"ncbi","result":"taxon"}
			response_ = requests.get(url=baseurl,params=PARAMS)
			data2_=response_.json()
			#print(data2_)
			output["genome_size"]=str(round(data2_["records"][0]["record"]["attributes"]["genome_size"]["value"]/1000000000,3))
			for lineage in data2_["records"][0]["record"]["lineage"]:
				if lineage["taxon_rank"] in ["class","order","family"]:
					output[lineage["taxon_rank"]]=lineage["scientific_name"]
		res=[",".join(line.split("\t"))]
		for k in ["scientific_name","common_name","taxon_id","synonym","class","order","family","genome_size"]:
			if k=="common_name" or k=="synonym":
				res.append(",".join(output[k]))
			else:
				res.append(output[k])
		print("\t".join(res))
		outfile.write("\n"+"\t".join(res))
outfile.close()