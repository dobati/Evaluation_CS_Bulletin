__author__ = 'Till'

from Logic import Parser
from lxml import etree
""" A TETML <Para> (Paragraph) can contain several different fontblocks (=font size & font abbrv combinations).
    This class separates those divs so that they only contain one fontblock per div."""
class DivStructurer:
    def __init__(self, div_tag, word_tag, FontManager):
        self.div_tag = div_tag
        self.word_tag = word_tag
        self.FontManager = FontManager

    def unravel_divs(self, xml):
        all_divs = Parser.findall_all(xml, self.div_tag)
        for div in all_divs:
            font_blocks = list()
            font_blocks.append(list())
            words = Parser.findall(div, self.word_tag)
            old_abbrv = self.FontManager.get_fontabbrvsize(words[0])

            for w in words:
                abbrv = self.FontManager.get_fontabbrvsize(w)
                if abbrv != old_abbrv:
                    font_blocks.append(list())
                    old_abbrv = abbrv

                font_blocks[-1].append(w)

            self.__put_into_new_divs(font_blocks, div)

    def __put_into_new_divs(self, font_blocks, div):
        if len(font_blocks) > 1:    # Are there different fontblocks mixed into the div?
            newest_div = div  # always append to the newest div
            for index, key in enumerate(font_blocks):
                if index == 0:  # don't process the first fontblock
                    continue
                new_div = etree.Element(self.div_tag)
                newest_div.addnext(new_div)
                newest_div = new_div

                for word in font_blocks[index]:
                    newest_div.append(word)