#!/bin/bash

export PATH=${PATH}:$HOME/edirect

input=$1

cat $input | xtract -pattern DocumentSummary \
-def "NA" -pfx "AssemblyAccession:" -element AssemblyAccession \
-def "NA" -pfx "AssemblyName:" -element AssemblyName \
-def "NA" -pfx "Organism:" -element Organism \
-def "NA" -pfx "Taxid:" -element Taxid \
-def "NA" -pfx "assembly-status:" -element assembly-status \
-def "NA" -pfx "representative-status:" -element representative-status \
-def "NA" -pfx "SubmitterOrganization:" -element SubmitterOrganization \
-block GB_BioProjects \
    -pfx "BioprojectAccn:" \
    -element BioprojectAccn \
     -pfx "BioprojectId:" \
    -element BioprojectId \
-block Stat \
    -if Stat@category -equals scaffold_n50 \
    -or Stat@category -equals contig_n50 \
    -or Stat@category -equals  total_length \
    -if Stat@sequence_tag -equals all \
    -sep ":" -def "NA" -element Stat@category,Stat | awk  -F $'\t' '{ if ( $5 != "Contig" && $6 != "alternate-pseudohaplotype"  && $6 != "haploid-with-alt-loci") {print } }'
