#!/bin/bash

export PATH=${PATH}:$HOME/edirect

input=$1

if [ ! -f vgp.asm ]
then
esearch -db bioproject -query 489243  | elink -target bioproject \
| efilter -query "NOT PRJNA516733, NOT PRJNA688938, NOT PRJNA533106" | elink -target bioproject \
| elink -target assembly | esummary \
xtract -pattern DocumentSummary -element AssemblyAccession,SpeciesTaxid \
> vgp.asm
fi

while read record id; do grep $record $input | cut -f1 -d$'\t'; done < vgp.asm