import sys
sys.path.append('..')

import codecs
import unittest
from lxml import etree
from Logic.Headings.ArticleInjector import ArticleInjector
from Logic.TagHandler import TagHandler
import Logic.Parser as Parser
from Logic.DivHandling.DivHandler import DivHandler
import TestHelper
from Logic.DivHandling.TokenizerAdapter import TokenizerAdapter


__author__ = 'Till'

""" Succeeds if all text is preserved and order of text is correct """
class ArticleInjectorTest(unittest.TestCase):

    def setUp(self):

        self.div_tag = Parser.TET_div_tag
        self.word_tag = Parser.TET_word_tag
        self.xml = Parser.parse(r"Input/referenzCS_de.tetml")
        self.headings_file = r"Input/referenzCS_de-Heading.xml"
        self.tagHandler = TagHandler()
        self.__run_divhandler()
        self.__run_tokenizeradapter()
        self.__run_taghandler()

    def test_article_injector(self):
        injector = ArticleInjector(self.div_tag, "Pages")
        injector.add_article_tags(self.xml)

        with codecs.open("Output/articleinjector.xml", "w", "utf-8") as the_file:
            the_file.write(etree.tostring(self.xml, pretty_print=True))

        generated = TestHelper.get_file_content("Output/articleinjector.xml")
        orig = TestHelper.get_file_content("Input/articleinjector.xml")
        self.assertEqual(generated, orig)

    def __run_divhandler(self):
        divhandler = DivHandler(self.headings_file, self.word_tag, self.div_tag)
        divhandler.handle_divs(self.xml)

    def __run_tokenizeradapter(self):
        self.tokenizerAdapter = TokenizerAdapter(self.div_tag, self.word_tag)
        self.tokenizerAdapter.start(self.xml)

    def __run_taghandler(self):
        self.tagHandler.strip_tags(self.xml)
        self.tagHandler.strip_elements(self.xml)
        self.tagHandler.convert_pbtags_to_emptytag(self.xml)

if __name__ == '__main__':
    unittest.main()