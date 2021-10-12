#!/bin/bash

export PATH=${PATH}:$HOME/edirect

taxa=$1


script_path=$(dirname "$0")

mkdir -p xml
mkdir -p tsv
mkdir -p filtered

for taxon in ${taxa//,/ }
do
echo ">>> "$taxon
if [ ! -f "xml/${taxon}.xml" ]
then
echo "\t\tRetrieving ${taxon} genomes information from NCBI"
query=${taxon}'[Organism]'
esearch -db assembly -query $query | esummary > xml/${taxon}.xml
fi

sh ${script_path}/filter.sh xml/${taxon}.xml > tsv/${taxon}.tsv
echo "\t\t# of chromosome-scaffold scale assemblies: "$(cat tsv/${taxon}.tsv | wc -l)

python ${script_path}/format.py tsv/${taxon}.tsv > filtered/${taxon}_filtered.tsv
echo "\t\t# of assemblies with VGP contiguity standards: "$(cat filtered/${taxon}_filtered.tsv | wc -l)

done

cat filtered/*_filtered.tsv > final.tsv