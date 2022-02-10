#!/bin/bash

export PATH=${PATH}:$HOME/edirect

input=$1

if [ ! -f vgp.asm ]
then
esearch -db bioproject -query 489243  | elink -target bioproject \
| efilter -query "NOT PRJNA516733, NOT PRJNA688938, NOT PRJNA533106" | elink -target bioproject \
| elink -target assembly | esummary \
| xtract -pattern DocumentSummary -element AssemblyAccession,SpeciesTaxid,SpeciesName,AssemblyType \
> vgp.asm
fi

while IFS=$'\t' read -r AssemblyAccession SpeciesTaxid SpeciesName AssemblyType; do 
	if [[ $AssemblyType != "alternate-pseudohaplotype" ]]; then
		grep $AssemblyAccession $input | cut -f1 -d$'\t'
	fi
done < vgp.asm