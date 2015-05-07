__author__ = 'Till'
from Logic.Headings.ArticleInjector import ArticleInjector
from Logic.TagHandler import TagHandler
from Logic.DivHandling.TokenizerAdapter import TokenizerAdapter
from DivHandling.DivHandler import DivHandler

import Parser

""" Main class for TETML processing. Output is intermediate XML format for Text & Berg Tokenizer. """
class TET2XML:

    def __init__(self):
        self.__articleInjector = ArticleInjector(Parser.div_tag, Parser.book_tag)
        self.tokenizerAdapter = TokenizerAdapter(Parser.div_tag, Parser.word_tag)
        self.tagHandler = TagHandler()

    def start(self, tetml_file, headings_file):
        xml = Parser.parse(tetml_file)
        self.tagHandler.rename_tags(xml)
        xml = DivHandler(headings_file, Parser.word_tag, Parser.div_tag).handle_divs(xml)
        xml = self.tokenizerAdapter.start(xml)

        self.tagHandler.strip_tags(xml)
        self.tagHandler.strip_elements(xml)
        self.tagHandler.convert_pbtags_to_emptytag(xml)
        self.__articleInjector.add_article_tags(xml)
        self.tagHandler.remove_tet_tag(xml)
        self.tagHandler.book_set_lang_attribute(xml, tetml_file)
        xml = self.tagHandler.remove_empty_lines(xml)

        return xml