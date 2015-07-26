#!/bin/bash
# @ Dolores Batinic
# Skript to count the <article> tags in XML output files

# remove the output file if it exist
rm -f OutputCountArticleTagsInXML.tsv

# adjust the path for your files
FILES=../../Output/XML/*xml

for f in $FILES
do
  # Count the number of <article> tags for each xml output file and store the output in OutputCountArticleTagsInXML.tsv
  echo "Processing $f file..."
  grep -H -c "<article" $f  >> OutputCountArticleTagsInXML_prov.tsv
  awk 'BEGIN { FS=":" }  { print $1,$2 }' OFS='\t' OutputCountArticleTagsInXML_prov.tsv >  OutputCountArticleTagsInXML.tsv
 
done
rm OutputCountArticleTagsInXML_prov.tsv

