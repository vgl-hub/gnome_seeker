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

python3 ${script_path}/format.py tsv/${taxon}.tsv > filtered/${taxon}_filtered.tsv
echo "\t\t# of assemblies with VGP contiguity standards: "$(cat filtered/${taxon}_filtered.tsv | wc -l)

done

cat filtered/*_filtered.tsv > final.tsv

echo "tag vgp assemblies"
sh ${script_path}/flag_vgp.sh final.tsv > vgp_matches
python3 ${script_path}/tag_asm.py final.tsv vgp_matches > final_tagged.tsv

python3 ${script_path}/summary.py final_tagged.tsv