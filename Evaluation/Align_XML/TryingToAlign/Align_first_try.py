__author__ = 'Dolores'

import lxml
from lxml import etree
import os
import Helper
from lxml import etree
import SettingsManager
from collections import defaultdict

"""Align the Articles & Sentences in Parallel XML Files"""
class ParallelXML2AlignedXML():
    def __init__(self):
        self.__parallel_xml_path = SettingsManager.parallel_xml_dir
        self.__aligned_xml_output_path = SettingsManager.aligned_xml_dir


    def start(self):
        files = Helper.get_files_in_directory(self.__parallel_xml_path, "*.xml")
        print "Align.py is processing files from:\n" + self.__parallel_xml_path
        jahrgang_ausgabe_dict = defaultdict(list)
        jahrgang_ausgabe_filename_dict = defaultdict(None)

        for xmlfile in files:
            #Example bulletin_1998_5_Kleider_de.xml
            #print "\t" + os.path.basename(xmlfile)
            bulletin = os.path.basename(xmlfile)[:8]
            jahrgang = os.path.basename(xmlfile)[9:13]
            ausgabe = os.path.basename(xmlfile)[14]
            name = os.path.basename(xmlfile)[16:-7]
            Language = os.path.basename(xmlfile)[-6: os.path.basename(xmlfile).index('.')]

            # If you want only filenames without full path
            #jahrgang_ausgabe_dict[(jahrgang,ausgabe,name)] +=[os.path.basename(xmlfile)]
            jahrgang_ausgabe_dict[(jahrgang,ausgabe,name)] +=[xmlfile]

            for jahrgang_ausgabe_name in jahrgang_ausgabe_dict:

                aligned_xml_filename = bulletin+'_'+jahrgang_ausgabe_name[0]+'_'+jahrgang_ausgabe_name[1]+"_"+jahrgang_ausgabe_name[2]+"-Aligned.xml"
                jahrgang_ausgabe_filename_dict[aligned_xml_filename] = jahrgang_ausgabe_dict[jahrgang_ausgabe_name]
                self.open_files_to_write(jahrgang_ausgabe_filename_dict)

        print "Align.py is done.\n"
       # print jahrgang_ausgabe_filename_dict

    def open_files_to_write(self, dict_with_filenames):

        for myfilename in dict_with_filenames:
            myfilename = Helper.replace_path_file(myfilename,self.__aligned_xml_output_path)
            aligned_content = self.align_articles(dict_with_filenames)

            # Pay attention to possible encoding errors here!
            with open(myfilename, 'wb') as my_aligned_file_name:
                my_aligned_file_name.write(aligned_content)
                return my_aligned_file_name


    def align_articles(self, dict_with_filenames):

        #for key, value in d.iteritems()
        all_article_nr = []
        for ausgaben_all_langs, each_lang_xml in dict_with_filenames.iteritems():
            for my_xmlinput in each_lang_xml:
                my_xml = open(my_xmlinput, 'r')
                tree = etree.parse(my_xml)
                article = tree.findall('//article')
        for each_article in article:
            article_nr = each_article.get('n')
            all_article_nr.append(article_nr)

        print all_article_nr, len(all_article_nr)

        # Return the 1 file with aligned articles with linkGrp targType="yearbook" for each Jahrgang_Ausgabe
        return '\n'.join(all_article_nr)

        # SAVE lang Attribute (<book lang="it">)
        # Save prallel file names for each Ausgabe
        #

            ### Parse with lxml
            ### Ausgabe soll so aussehen:

            # <?xml version='1.0' encoding='UTF-8'?>
            # <TEI>
            # <teiHeader>
            # JahrgangX_AusgabeY
            # </teiHeader>
            # <linkGrp targType="yearbook" xtargets="JahrgangX_AusgabeY_de.xml;JahrgangX_AusgabeY_fr.xml" lang="de;fr">
            #     <linkGrp targType="article" xtargets="a1;a1">
            #     </linkGrp>
            # </linkGrp>
            # </TEI>

       # return ' '.join(dict_with_filenames[ausgaben_all_langs])

    def align_sentences(self):
        return 'not yet'



if __name__ == "__main__":
   ParallelXML2AlignedXML().start()

# <book lang="de">
#   <article n="0">
#     <div> DE </div>
#     <div> DE </div>
#   # </article>
#   <article n="1">
#     <div heading="article">DE TITEL 1</div>
#     <div> DE </div>
#   </article>
#   <article n="2">
#     <div heading="article"> DE TITEL 2</div>
#     <div> DE </div>
#     <div> DE </div>
#   </article>
# </book>
#
#
# Output:
#
# <?xml version='1.0' encoding='UTF-8'?>
# <TEI>
# <teiHeader>
# JahrgangX_AusgabeY
# </teiHeader>
# <linkGrp targType="yearbook" xtargets="JahrgangX_AusgabeY_de.xml;JahrgangX_AusgabeY_fr.xml" lang="de;fr">
# 	<linkGrp targType="article" xtargets="a1;a1">
# 	</linkGrp>
# </linkGrp>
# </TEI>
