from Logic.PDF2TET import TET
from Logic import SettingsManager

__author__ = 'Till'

""" PDF to TETML by TET commandline tool.
    Is used by start.py. """
class StartPDF2TETML():

    def __init__(self):
        self.__pdf_input_path = SettingsManager.pdf_input_dir
        self.__tetml_path = SettingsManager.tetml_output_dir

    def start(self):
        tet = TET(self.__pdf_input_path, self.__tetml_path)
        tet.convert()

        print "StartPDF2XML.py is done.\n"

if __name__ == "__main__":
    StartPDF2TETML().start()