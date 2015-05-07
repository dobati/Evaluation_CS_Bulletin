from HeadingsInjector import HeadingsInjector
from Logic.DivHandling.DivStructurer import DivStructurer
from Logic.Headings import FontManager
from Logic.DivHandling import FreeWords2Div

__author__ = 'Till'

""" Main class for handling all paragraph related processing """
class DivHandler:
    def __init__(self, headings_file, word_tag, div_tag):
        self.word_tag = word_tag
        self.div_tag = div_tag
        self.headings_injector = HeadingsInjector(headings_file, self.div_tag, self.word_tag, FontManager)

    def handle_divs(self, xml):
        FontManager.create_font_to_abbrv_mapping(xml)
        FreeWords2Div.put_free_words_into_div(xml, self.word_tag, self.div_tag)
        DivStructurer(self.div_tag, self.word_tag, FontManager).unravel_divs(xml)
        self.headings_injector.set_headings(xml)
        return xml
