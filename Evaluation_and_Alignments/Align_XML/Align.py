#-*-coding:utf-8-*-

__author__ = 'Dolores Batinic'

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

            jahrgang_ausgabe_name = jahrgang_ausgabe_name[0:-7]
            jahrgang_ausgabe_dict[(jahrgang_ausgabe_name)] +=[xmlfile]


        ## get ready for aligning the articles for each edition
        self.align_articles(jahrgang_ausgabe_dict)

        print "Align.py is done.\n"


    def align_articles(self, dict_with_filenames):

        ## open the root element TEI
        #********************
        tei = etree.Element("TEI")
         #********************

        #################################################################################

         ## iterate through the dict which has a list with every xml edition as value:
        for ausgaben_all_langs, each_lang_xml in dict_with_filenames.iteritems():
            xtarget_file_name_list, languagelist = [], []

            ## for each edition (filename without language information) write the name in the teiHeader, which should be child of <TEI>
            #teiHeader = etree.Element("teiHeader")
            #teiHeader.text = str(ausgaben_all_langs)

            #********************
            #tei.append(teiHeader)
            #********************

            #################################################################################

            ## open dict for storing article number for each page number of each language
            pb_lang_holds_artnr = defaultdict(list)
            ## open dict for storing article number for each page number
            pb_holds_artnr = defaultdict(list)
            a_art_nr_lang = defaultdict(int)

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
                    article_nr = each_article.get('n')
                    # the language information is temporary stored along with the article number to verify alignments and add None when there is no corresponding alignment
                    
                    articlenr =  "a"+article_nr+"_"+lang

                    for each_pb in each_article:
                        if each_pb.tag == "pb":
                            pbnumber = each_pb.get("number")
                            pb_lang_holds_artnr[(pbnumber,lang)] +=[articlenr]


            if len(languagelist) > 1:

                teiHeader = etree.Element("teiHeader")
                teiHeader.text = str(ausgaben_all_langs)

                #********************
                tei.append(teiHeader)
                #********************

                ## append to <tei> child element <linkGrp> which stores full filename and language info

                #********************
                linkGrp1 = etree.Element("linkGrp",targType="yearbook",xtargets=';'.join(xtarget_file_name_list), lang=';'.join(languagelist))
                tei.append(linkGrp1)
                #********************

                #################################################################################

                # for each language in our editions and for each <pb> tag in the respective edition
                # and add a ";" separator between the article numbers which belong to editions in two different languages

                for language in languagelist:

                    for key_pb, key_lang in pb_lang_holds_artnr:
                        # order the article numbers to correspond to the order of languages in lang attribute
                        if key_lang == language:
                            if key_pb not in pb_holds_artnr:
                                pb_holds_artnr[key_pb] = pb_lang_holds_artnr[key_pb, key_lang]+[";"]
                            else:
                                pb_holds_artnr[key_pb] += pb_lang_holds_artnr[key_pb, key_lang]+[";"]

                ## Invert the dict, so you have article combinations as keys
                for key in sorted(pb_holds_artnr):
                    a_art_nr_lang[tuple(pb_holds_artnr[key])] +=1

                for art_key in sorted(a_art_nr_lang):
                    string_in_art_key = [str(x) for x in art_key]
                    art_key_string = "".join(string_in_art_key)

                    ## get rid of ";" separator at the end of the string get rid of whitespaces
                    art_key_stripped_last_punct = art_key_string[:-1]
                    #art_key_stripped_last_punct = art_key_stripped_last_punct.replace(' ', '')
                    art_key_stripped_last_punct_list = art_key_stripped_last_punct.split(';')


                    #################################################################################
                    ### Add dummy value "None" für fehlende Artikel
                    ### Add "None" if they is no corresponding alignment (e.g.: languages: de, en, fr, it -> alignments: en, fr)


                    if len(languagelist) != len(art_key_stripped_last_punct_list):

                        if len(languagelist)==4 and len(art_key_stripped_last_punct_list)==3:

                            if languagelist[0] != art_key_stripped_last_punct_list[0][-2:]:
                                art_key_stripped_last_punct_list.insert(0,"None")
                            elif languagelist[1] != art_key_stripped_last_punct_list[1][-2:]:
                                art_key_stripped_last_punct_list.insert(1,"None")
                            elif languagelist[2] != art_key_stripped_last_punct_list[2][-2:]:
                                art_key_stripped_last_punct_list.insert(2,"None")
                            else:
                                art_key_stripped_last_punct_list.append("None")


                        if len(languagelist)==4 and len(art_key_stripped_last_punct_list)==2:

                            if languagelist[0] != art_key_stripped_last_punct_list[0][-2:]:
                                art_key_stripped_last_punct_list.insert(0,"None")
                            else:
                                if languagelist[1] != art_key_stripped_last_punct_list[1][-2:]:
                                    art_key_stripped_last_punct_list.insert(1,"None")
                                else:
                                    art_key_stripped_last_punct_list.append("None")

                            if languagelist[1] != art_key_stripped_last_punct_list[1][-2:]:
                                art_key_stripped_last_punct_list.insert(1,"None")
                            else:
                                art_key_stripped_last_punct_list.append("None")


                        if len(languagelist)==3 and len(art_key_stripped_last_punct_list)==2:
                            if languagelist[0] != art_key_stripped_last_punct_list[0][-2:]:
                                art_key_stripped_last_punct_list.insert(0,"None")
                            elif languagelist[1] != art_key_stripped_last_punct_list[1][-2:]:
                                art_key_stripped_last_punct_list.insert(1,"None")
                            elif languagelist[2] != art_key_stripped_last_punct_list[2][-2:]:
                                art_key_stripped_last_punct_list.insert(2,"None")

                        # Ignore Alignments where there is only one article
                        #if len(art_key_stripped_last_punct_list)==1:
                         #   pass

                    #################################################################################

                    # if you want to be 100% TEI conform, add second child <linkGrp> to parent <linkGrp>
                    # linkGrp2 = etree.Element("linkGrp",targType="article", xtargets=art_key_stripped_last_punct)
                    # Ignore empty alignments alignments
                    if len(art_key_stripped_last_punct_list) !=0:
                        #if len(art_key_stripped_last_punct_list)!=1:
                        linkGrp2 = etree.Element("link",targType="article", xtargets=";".join(art_key_stripped_last_punct_list).replace("_de", "").replace("_en", "").replace("_fr", "").replace("_it", ""))

                    #********************
                    linkGrp1.append(linkGrp2)
                    #********************

            #et = etree.ElementTree(tei)
            #print(etree.tostring(tei, pretty_print=True))

            aligned = etree.tostring(tei, pretty_print=True)
            with open(self.__aligned_xml_output_path, "w") as output:
                output.write(aligned)


if __name__ == "__main__":
   ParallelXML2AlignedXML().start()


