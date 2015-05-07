from Logic.Headings.HeadingsParser import HeadingsParser
from Logic import Parser


__author__ = 'Till'
""" Sets headings for divs """
class HeadingsInjector:

    def __init__(self, headings_file, div_tag, word_tag, FontManager):
        self.__headingsDB = HeadingsParser().parse(headings_file)
        self.__div_tag = div_tag
        self.__word_tag = word_tag
        self.__FontManager = FontManager

    # for each div, lookup its fontabbrv and set heading if one matches
    def set_headings(self, xml):
        all_divs = Parser.findall_all(xml, self.__div_tag)
        for div in all_divs:
            words = Parser.findall_all(div, self.__word_tag)
            first_word = words[0]
            self.__set_heading(first_word)

    def __set_heading(self, word):
        fontabbrvsize = self.__FontManager.get_fontabbrvsize(word)
        heading = self.__headingsDB.get_heading_by_font(fontabbrvsize)
        if heading:  # set heading attribute
            div = word.getparent()
            div.set(Parser.heading_attr, heading)
