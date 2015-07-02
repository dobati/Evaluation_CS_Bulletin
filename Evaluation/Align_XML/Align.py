#-*-coding:utf-8-*-

__author__ = 'Dolores'

import os
import os.path as path
import glob
from lxml import etree
import SettingsManager # in SettingsManager we define the paths of our input and output directories
from collections import defaultdict



"""Align the Articles & Sentences in Parallel XML Files"""
class ParallelXML2AlignedXML():

    def __init__(self):
        self.__parallel_xml_path = SettingsManager.parallel_xml_dir
        self.__aligned_xml_output_path = SettingsManager.aligned_xml_files

    def get_files_in_directory(self, abs_sourcedir, file_extension="*.xml"):
        sourcedir_glob = path.join(abs_sourcedir, file_extension)
        files = sorted(glob.glob(sourcedir_glob))
        return files

    def start(self):

        ##  Use the Helper srcipt to get all the files in the Input directory
        files = self.get_files_in_directory(self.__parallel_xml_path, "*.xml")
        print "Align.py is processing files from:\n" + self.__parallel_xml_path
        jahrgang_ausgabe_dict = defaultdict(list)

        ## First we are grouping the editions in all languages under the same name
        ## Example of filenames:  bulletin_1998_5_Kleider_de.xml, bulletin_1998_5_Kleider_fr.xml
        ## These filenames will get grouped as {bulletin_1998_5_Kleider: [bulletin_1998_5_Kleider_de.xml, bulletin_1998_5_Kleider_fr.xml]}

        for xmlfile in files:

            ### If tokenized.tagged in file name, eliminate it!
            if "tokenized.tagged." in os.path.basename(xmlfile):
                jahrgang_ausgabe_name = os.path.basename(xmlfile).replace("tokenized.tagged.", "")
            else:
                jahrgang_ausgabe_name = os.path.basename(xmlfile)

            #jahrgang_ausgabe_name = os.path.basename(xmlfile)[0:-7]
            jahrgang_ausgabe_name = jahrgang_ausgabe_name[0:-7]
            jahrgang_ausgabe_dict[(jahrgang_ausgabe_name)] +=[xmlfile]


        ## get ready for aligning the articles for each edition
        self.align_articles(jahrgang_ausgabe_dict)
        print "Align.py is done.\n"
        #print len(jahrgang_ausgabe_dict)
        # 79


    def align_articles(self, dict_with_filenames):

        ## open the root element TEI
        tei = etree.Element("TEI")

        ## iterate through the dict which has a list with every xml edition as value:
        for ausgaben_all_langs, each_lang_xml in dict_with_filenames.iteritems():
            xtarget_file_name_list, languagelist = [], []

            ## for each edition (filename without language information) write the name in the teiHeader, which should be child of <TEI>
            teiHeader = etree.Element("teiHeader")
            teiHeader.text = str(ausgaben_all_langs)
            tei.append(teiHeader)

            ## open dict for storing article number for each page number of each language
            pb_lang_holds_artnr = defaultdict(list)
            ## open dict for storing article number for each page number
            pb_holds_artnr = defaultdict(list)

            only_art_nr = defaultdict(int)

            for my_xmlinput_filename in each_lang_xml:

                ## get the basename information for each edition and store it in a list
                xtarget_file_name =  str(os.path.basename(my_xmlinput_filename))
                xtarget_file_name_list.append(xtarget_file_name)

                ## open each edition for reading and parsing with lxml
                my_xml = open(my_xmlinput_filename, 'r')
                tree = etree.parse(my_xml)
                root = tree.getroot()

                ## get the language information for each edition and store it in a list
                lang = root.get('lang')
                languagelist.append(lang)

                article = tree.findall('//article')
                for each_article in article:
                    #print each_article.tag
                    article_nr = each_article.get('n')

                    #if you want to see which articles is from ehich language

                    #articlenr =  "a"+article_nr+"_"+lang
                    #otherwise
                    #articlenr =  "a"+article_nr
                    articlenr =  int(article_nr)

                  #  print article_nr
                    for each_pb in each_article:
                        #print each_pb
                        if each_pb.tag == "pb":
                        #    #print each_pb.tag
                            pbnumber = each_pb.get("number")
                            pb_lang_holds_artnr[(pbnumber,lang)] +=[articlenr]

            #print pb_lang_holds_artnr
            # iterate according to the order in language_list
            # for each language in our editions and for each <pb> tag in the respective edition
            # and add a ";" separator between the article numbers which belong to editions in two different languages

            for language in languagelist:
                for key_pb, key_lang in pb_lang_holds_artnr:
                    if key_lang == language:
                        if key_pb not in pb_holds_artnr:
                            pb_holds_artnr[key_pb] = pb_lang_holds_artnr[key_pb, key_lang]+[";"]
                        else:
                            pb_holds_artnr[key_pb] += pb_lang_holds_artnr[key_pb, key_lang]+[";"]

            ## append to <tei> child element <linkGrp> which stores filename and language info
            #tei.append(etree.Element("linkGrp"))
            linkGrp1 = etree.Element("linkGrp",targType="yearbook",xtargets=';'.join(xtarget_file_name_list), lang=';'.join(languagelist))
            tei.append(linkGrp1)

            ## invert the dict, so you have article combinations as keys and you can take unique elements
            for key in sorted(pb_holds_artnr): #, reverse=False):
                only_art_nr[tuple(pb_holds_artnr[key])] +=1

            ## append to <linkGrp> another <linkGrp> child element which stores article alignments

            # make sure article number is still integer so you can sort from a1 to a20 and avoid sorting per string (to avoid: a1, a11, a2)
            for art_key in sorted(only_art_nr):# , reverse=False):

                string_in_art_key = [str(x) for x in art_key]

                # add "a" label to art. number to be conform to the new text&berg format
                a_string_in_art_key = []
                for x in string_in_art_key:
                    if x.isdigit():
                        art_nr_with_a_label = "a"+x
                        a_string_in_art_key.append(art_nr_with_a_label)
                    else:
                        a_string_in_art_key.append(x)

                art_key_string = " ".join(a_string_in_art_key)

                ## get rid of ";" separator at the end of the string
                art_key_stripped_last_punct = art_key_string[:-1]
                ## get rid of whitespaces
                art_key_stripped_last_punct = art_key_stripped_last_punct.replace(' ', '')

                linkGrp2 = etree.Element("linkGrp",targType="article", xtargets=art_key_stripped_last_punct)
                linkGrp1.append(linkGrp2)


        et = etree.ElementTree(tei)
        print(etree.tostring(tei, pretty_print=True))
        aligned = etree.tostring(tei, pretty_print=True)
        #self.__aligned_xml_output_path
        with open(self.__aligned_xml_output_path, "w") as output:
            output.write(aligned)

        #et.write(sys.stdout)
        #print et

if __name__ == "__main__":
   ParallelXML2AlignedXML().start()

   ###
   ### write the output in Aligned_files.xml
   ### test it
   ### make the sentence alignment


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

###  Text & Berg Output:
#
#   <article n="a11">
#     <tocEntry author="Dr. P.-L. Mercanton" authorID="2053" category="Abhandlungen" lang="fr" title="Les Variations périodiques des Glaciers des Alpes Suisses" />
#     <div>
#       <s lang="fr" n="a11-s1">
#         <w lemma="les" n="a11-s1-w1" pos="D_def">Les</w>
#         <w lemma="variation" n="a11-s1-w2" pos="N_C">Variations</w>
#         <w lemma="périodique" n="a11-s1-w3" pos="A_qual">périodiques</w>
#         <w lemma="de" n="a11-s1-w4" pos="P">des</w>
#         <w lemma="glacier" n="a11-s1-w5" pos="N_C">Glaciers</w>
#         <w lemma="de" n="a11-s1-w6" pos="P">des</w>
#         <w lemma="alpe" n="a11-s1-w7" pos="N_C">Alpes</w>
#         <w lemma="suisse" n="a11-s1-w8" pos="N_C">Suisses</w>
#       </s>
#     </div>
#
### CS Output:
#
# <article n="0" content="TOC">
#     <div>
#       <s n="0-1" lang="de">
#         <w n="0-1-1" pos="ADJA" lemma="unk">bulletin1</w>
#       </s>
#     </div>
#     <div>
#       <s n="0-2" lang="de">
#         <w n="0-2-1" pos="ART" lemma="d">Das</w>
#         <w n="0-2-2" pos="NN" lemma="Magazin">Magazin</w>
#         <w n="0-2-3" pos="ART" lemma="d">der</w>
#         <w n="0-2-4" pos="NE" lemma="Credit">Credit</w>
#         <w n="0-2-5" pos="ADJA" lemma="unk">Suisse</w>
#         <w n="0-2-6" pos="NN" lemma="unk">Financial</w>
#         <w n="0-2-7" pos="NN" lemma="Service">Services</w>
#       </s>
#     </div>
