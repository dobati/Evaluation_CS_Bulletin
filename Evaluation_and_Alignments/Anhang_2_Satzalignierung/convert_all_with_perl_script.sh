# Dolores Batinic
# Preparation for sentences alignment with T&B Scripts Graen/Weibel/Leuenberger

# Bash script for applying the per Skript Convert_old_to_new_id_format.pl to all the files in directory



# in oldxml/ are stored tokenized.tagged.xmls which we need to convert to t&b format and rename
# change the path for oldxml/ to the path where the xml files in the old id format are stored

# eliminate files if they are already there

rm -f oldxml/*{en,fr,it,de}.xml
rm -f sentence_alignment/*{en,fr,it,de}.xml


for old_xml in $(ls oldxml/*xml)
do
    
perl Convert_old_to_new_id_format.pl $old_xml  > "${oldxml}${old_xml%/}_converted_to_tb_format.xml"

done

mv oldxml/*.tokenized.tagged.xml_converted_to_tb_format.xml sentence_alignment/


rename 's/.tokenized.tagged.xml_converted_to_tb_format.xml/.xml/' sentence_alignment/*.tokenized.tagged.xml_converted_to_tb_format.xml 
