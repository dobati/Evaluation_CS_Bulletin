import codecs
from copy import copy
from os import path
import Parser
import Helper
import SettingsManager

__author__ = 'Till'

""" This class parses all headings files in a folder to store all unique headings in a file for the prettyprinter load history button.
    Additionally it outputs how many new fontabrrvsizes were added with every headings file processed"""
class HeadingsHistoryGenerator:

    def __init__(self):
        self.output_dir = SettingsManager.headings_history_generator_output
        self.headings_dir = SettingsManager.headings_input_dir
        assert path.isdir(self.headings_dir), self.headings_dir + " could not be found!"

    def start(self):
        files = Helper.get_files_in_directory(self.headings_dir, file_extension="*.xml")
        name_and_size = set()
        size_only = set()
        for filename in files:
            xml = Parser.parse(filename)
            headings = Parser.findall_all(xml, "HEADING")
            prev_name_and_size = copy(name_and_size)
            prev_size_only = copy(size_only)

            self.__add_fontname_and_size(name_and_size, headings)
            self.__add_size_only(size_only, headings)

            self.__print_diff(filename, name_and_size, prev_name_and_size)
            print "\n"
            self.__print_diff(filename, size_only, prev_size_only)
            print "-------------------------------------------------"

        print "Total number of names & size: " + str(len(name_and_size))
        print "Total number of size: " + str(len(size_only))

        self.__write_to_file(name_and_size, path.join(self.output_dir, "headings_name_and_size.txt"))
        self.__write_to_file(size_only, path.join(self.output_dir, "headings_size.txt"))

    # update headings history files for PrettyPrinter
    def __write_to_file(self, fonts, filename):
        order_list = sorted(list(fonts))
        with codecs.open(filename, "w", "utf-8") as the_file:
            for font in order_list:
                the_file.write(font + "\n")

    def __add_fontname_and_size(self, fonts, headings):
        for heading in headings:
            name = heading.get("fontabbrv")
            size = heading.get("fontsize")
            fonts.add(name + " " + size)

    def __add_size_only(self, fonts, headings):
        for heading in headings:
            size = heading.get("fontsize")
            fonts.add(size)

    def __print_diff(self, filename, name_and_size, prev_fonts):
        diff_list = list(name_and_size - prev_fonts)
        print str(len(diff_list)) + " fonts were added by " + path.basename(filename) + ":"
        print diff_list

HeadingsHistoryGenerator().start()