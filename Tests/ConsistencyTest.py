import sys
sys.path.append('..')

import codecs
import unittest
import os.path
from lxml import etree
from Logic.TET2XML import TET2XML
from Logic import Helper
import Logic.Parser as Parser
import TestHelper

__author__ = 'Till'

""" Succeeds if all text is preserved and order of text is correct """
class ConsistencyTest(unittest.TestCase):

    def setUp(self):
        self.tetml_file = os.path.abspath(r"Input/referenzCS_de.tetml")
        self.headings_folder = os.path.abspath(r"Input")

    def test_output_unchanged(self):
        gen_file = r"Output/referenzCS_de_consistency.xml"
        orig_file = r"Input/referenzCS_de_consistency.xml"

        xml = self.__start_tet2xml(self.headings_folder, self.tetml_file)

        with codecs.open(gen_file, "w", "utf-8") as the_file:
            the_file.write(etree.tostring(xml, pretty_print=True))

        computed_string = TestHelper.get_file_content(gen_file)
        orig_file_string = TestHelper.get_file_content(orig_file)

        self.assertItemsEqual(orig_file_string, computed_string)

    @unittest.skip("test_text_consistency_and_order() only works if the fix* methods in TokenizerAdapter are commented out")
    def test_text_consistency_and_order(self):
        original_list = self.__get_original_text(self.tetml_file)
        produced_list = self.__get_produced_text(self.headings_folder, self.tetml_file)

        self.assertEqual(len(original_list), len(produced_list), "Text is missing!")
        for f, b in zip(original_list, produced_list):
            self.assertEqual(f, b, "Text is out of order!")

    def __get_original_text(self, tetml_file):
        tree = Parser.parse(tetml_file)
        all_text = Parser.findall_all(tree, "Text")
        text_list = list()
        for text in all_text:
            text_list.append(text.text)
        return text_list

    def __get_produced_text(self, headings_folder, tetml_file):
        xml = self.__start_tet2xml(headings_folder, tetml_file)
        all_divs = Parser.findall_all(xml, Parser.div_tag)
        comparable_list = list()
        for div in all_divs:
            comparable_list.extend(div.text.split())
        return comparable_list

    def __start_tet2xml(self, headings_folder, tetml_file):
        tet2xml = TET2XML()
        headings_file = Helper.replace_extension_and_path(tetml_file, headings_folder, ".tetml", "-Heading.xml")
        xml = tet2xml.start(tetml_file, headings_file)
        return xml

