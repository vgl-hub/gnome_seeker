#! /usr/bin/env python

import sys

fileName=sys.argv[1]

f=open(fileName)
data=f.read().splitlines()
f.close()

submitters={}
for line in data[1:]:
	items=line.split("\t")
	submitters.setdefault(items[12],[]).append(items[0])

counts={}
for name in submitters.keys():
	counts[name]=len(submitters[name])
sorted_list=sorted(counts.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)

total=sum([counts[x] for x in counts.keys()])
t=0
others=0
print("\n")
for record in sorted_list:
	if t<=total*0.5:
		print(record[0],record[1])
		t=t+record[1]
	else:
		others=others+record[1]
print("others",others)

	
