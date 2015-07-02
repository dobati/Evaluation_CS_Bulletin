#!/bin/bash

FILES=/Users/dona/Documents/UNI/Programmierprojekt/XML_Pipeline_3.5/StructureXML/Output/XML/*xml
for f in $FILES
do
  # Count the number of <article> tags for each xml output file and store the output in OutputCountArticleTagsInXML.tsv

  echo "Processing $f file..."
  grep "<article" $f | wc -l > OutputCountArticleTagsInXML.tsv 

done
