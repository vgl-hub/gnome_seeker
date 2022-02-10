# gnome_seeker
 
Collects genome asssemblies from NCBI that meet VGP contig and scaffold N50 minimum standards (1Mb and 10Mb).

To run it:

vertebrates="Cladistia,Aves,Mammalia,Reptilia,Amphibia,Coelacanthimorpha,Dipnoi,Actinopteri,Chondrichthyes,Cyclostomata"

sh _fetch_NCBI.sh $vertebrates

requirements:
python3
NCBI edirect (https://www.ncbi.nlm.nih.gov/books/NBK179288/)

final output: final.tsv
columns= "AssemblyAccession","AssemblyName","Organism","Taxid","assembly-status","SubmitterOrganization","representative-status","BioprojectAccn","BioprojectId","contig_n50","scaffold_n50","VGP tag"

Also now includes a small script to gather tsxonomic information from https://goat.genomehubs.org.

Takes a tab delimited file with header with two columns: scientific_name, common_name.

python goat.py input_file
