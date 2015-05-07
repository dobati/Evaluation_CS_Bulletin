import os
from lxml import etree
from Logic.TET2XML import TET2XML
from Logic import Helper
from Logic import SettingsManager

__author__ = 'Till'

""" TETML to intermediate XML for Text & Berg tokenizer.
    Is used by start.py. """
class StartTETML2XML():
    def __init__(self):
        self.__xml_output_path = SettingsManager.xml_output_dir
        self.__headings_folder = SettingsManager.headings_input_dir
        self.__tetml_path = SettingsManager.tetml_output_dir

    def start(self):
        files = Helper.get_files_in_directory(self.__tetml_path, "*.tetml")
        print "StartTETML2XML.py is processing files from:\n" + self.__tetml_path
        for tetml_file in files:
            print "\t" + os.path.basename(tetml_file)
            tet2xml = TET2XML()
            headings_file = Helper.replace_extension_and_path(tetml_file, self.__headings_folder, ".tetml", "-Heading.xml")
            xml = tet2xml.start(tetml_file, headings_file)

            xml_output_file = Helper.replace_extension_and_path(tetml_file, self.__xml_output_path, ".tetml", ".xml")
            with open(xml_output_file, 'wb') as the_file:
                the_file.write(etree.tostring(xml, encoding="UTF8", pretty_print=True))

        print "StartTETML2XML.py is done.\n"

if __name__ == "__main__":
    StartTETML2XML().start()
