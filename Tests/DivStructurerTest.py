import sys
sys.path.append('..')

import codecs
import unittest
from Logic.Headings import FontManager
from Logic.DivHandling.DivStructurer import DivStructurer
from Logic import Parser
import os
from lxml import etree
import TestHelper

__author__ = 'Till'

class DivStructurerTest(unittest.TestCase):
    def test_return_value(self):
        self.filename = "DivStructurerTest.xml"
        input_generated_xml = os.path.abspath(os.path.join("Input", "referenzCS_de.tetml"))
        input_original_xml = os.path.abspath(os.path.join("Input", self.filename))
        generated_file = self.__generate_temp_file(input_generated_xml)

        computed_string = TestHelper.get_file_content(generated_file)
        orig_file_string = TestHelper.get_file_content(input_original_xml)

        self.assertItemsEqual(orig_file_string, computed_string)

    def __generate_temp_file(self, input_generated_xml):
        xml = Parser.parse(input_generated_xml)
        computed_string = ""
        FontManager.create_font_to_abbrv_mapping(xml)
        DivStructurer(Parser.TET_div_tag, Parser.TET_word_tag, FontManager).unravel_divs(xml)
        all_divs = Parser.findall_all(xml, Parser.TET_div_tag)
        for div in all_divs:
            for word in div:
                computed_string += etree.tostring(word)

        generated_file = os.path.abspath(os.path.join("Output", self.filename))
        with codecs.open(generated_file, "w", "utf-8") as the_file:
            the_file.write(computed_string)
        return generated_file





