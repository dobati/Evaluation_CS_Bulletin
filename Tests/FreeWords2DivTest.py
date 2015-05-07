import sys
sys.path.append('..')

import unittest
import os.path
from Logic.Headings import FontManager
from Logic.DivHandling import FreeWords2Div
from Logic import Parser


__author__ = 'Till'

class FreeWords2DivTest(unittest.TestCase):
    def test_DivHandler(self):
        tetml_file = os.path.abspath("Input/referenzCS_de.tetml")
        xml = Parser.parse(tetml_file)
        FontManager.create_font_to_abbrv_mapping(xml)
        FreeWords2Div.put_free_words_into_div(xml, Parser.TET_word_tag, Parser.TET_div_tag)

        word_tags = Parser.findall_all(xml, Parser.TET_word_tag)

        for tag in word_tags:
            para_tag = tag.getparent().tag
            self.assertTrue(para_tag == Parser.TET_div_tag, "<" + para_tag + ">" + " != " + "<" + Parser.TET_div_tag + ">" + "\nThere are still free floating word-tags")