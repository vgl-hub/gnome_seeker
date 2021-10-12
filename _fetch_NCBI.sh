#!/bin/bash

export PATH=${PATH}:$HOME/edirect

taxa=$1


script_path=$(dirname "$0")

for taxon in ${taxa//,/ }
do
echo ">>> "$taxon
if [ ! -f "${taxon}.xml" ]
then
echo "\t\tRetrieving ${taxon} genomes information from NCBI"
query=${taxon}'[Organism]'
esearch -db assembly -query $query | esummary > ${taxon}.xml
fi

sh ${script_path}/filter.sh ${taxon}.xml > ${taxon}.tsv
echo "\t\t# of chromosome-scaffold scale assemblies: "$(cat ${taxon}.tsv | wc -l)

python ${script_path}/format.py ${taxon}.tsv > ${taxon}_filtered.tsv
echo "\t\t# of assemblies with VGP contiguity standards: "$(cat ${taxon}_filtered.tsv | wc -l)

done

cat *_filtered.tsv > final.tsv