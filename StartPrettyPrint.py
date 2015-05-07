import os
from Logic.PrettyPrinter.PrettyHTMLPrinter import PrettyHTMLPrinter
from Logic import Helper
from Logic import SettingsManager

__author__ = 'Till'

""" TETML to pretty printed HTML.
    Is used by start.py. """
class StartPrettyPrint:

    def __init__(self):
        pass

    def start(self):
        tetml_path = SettingsManager.tetml_output_dir
        prettyprint_output_path = SettingsManager.prettyprinter_output_dir

        files = Helper.get_files_in_directory(tetml_path, "*.tetml")
        print "StartPrettyPrint.py is processing files.\n" \
              + tetml_path + " --> " + prettyprint_output_path
        for tetml_file in files:
            print "\t" + os.path.basename(tetml_file)
            pprinter = PrettyHTMLPrinter()

            pprinter.start(tetml_file, prettyprint_output_path)

        print "startPrettyPrint.py is done.\n"

if __name__ == "__main__":
    StartPrettyPrint().start()