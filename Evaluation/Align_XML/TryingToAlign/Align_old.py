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
        jahrgang_ausgabe_filename_dict = defaultdict(list)

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

                aligned_xml_filename = bulletin+'_'+jahrgang_ausgabe_name[0]+'_'+jahrgang_ausgabe_name[1]+"_"+jahrgang_ausgabe_name[2]
                jahrgang_ausgabe_filename_dict[aligned_xml_filename] = jahrgang_ausgabe_dict[jahrgang_ausgabe_name]
                #print jahrgang_ausgabe_filename_dict
        self.align_articles(jahrgang_ausgabe_filename_dict)

        print "Align.py is done.\n"


    def align_articles(self, dict_with_filenames):

        article_info_dict = defaultdict(list)


        print "<TEI>"
        for ausgaben_all_langs, each_lang_xml in dict_with_filenames.iteritems():
            xtarget_file_name_list, languagelist = [], []
            print "<teiHeader>", str(ausgaben_all_langs), "</teiHeader>"
            my_dict = defaultdict(list)
            for my_xmlinput_filename in each_lang_xml:

               # print my_xmlinput_filename
                xtarget_file_name =  str(os.path.basename(my_xmlinput_filename))
                xtarget_file_name_list.append(xtarget_file_name)
                my_xml = open(my_xmlinput_filename, 'r')
                tree = etree.parse(my_xml)
                root = tree.getroot()
                lang = root.get('lang')
                languagelist.append(lang)

                articles = tree.findall('//article')
                for article in articles:
                     article_nr = article.get('n')
                     article_info_dict[(xtarget_file_name,lang)] +=[str("a")+str(article_nr)]

                for element in root.iter("article", "pb"):
                    if element.tag == "article":
                        articlenr = element.get("n")
                        articlenr =  "a"+articlenr+"_"+lang
                    if element.tag == "pb":
                        #pbnumber = "pb"+element.text+"_"+lang
                        pbnumber = element.text
                        my_dict[pbnumber] +=[articlenr]

            print '\n<linkGrp targType="yearbook" xtargets="'+';'.join(xtarget_file_name_list)+'"'+ " lang="+'"'+';'.join(languagelist)+'"'+">"

            for key in sorted(my_dict, reverse=False):
                #print key, my_dict[key]
                print '<linkGrp targType="article" xtargets="'+';'.join(my_dict[key])+'"'+'></linkGrp>'
            print "</linkGrp>"


        print "</TEI>"



if __name__ == "__main__":
   ParallelXML2AlignedXML().start()

# Input:

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
#     <div> DE </div>s
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
