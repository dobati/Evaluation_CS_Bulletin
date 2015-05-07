__author__ = 'Till'
from collections import defaultdict

""" Assigns a heading to a font-name & font-size combination """
class HeadingsDB:

    def __init__(self):
        self.__headings = defaultdict(list)  # dictionary with list. Allows to append multiple values per key

    def add(self, font_abrvsize, heading_name):
        self.__headings[heading_name].append(font_abrvsize)

    def get_heading_by_font(self, font_abbrv_size):
        for key, value in self.__headings.items():
            for v in value:
                if v == font_abbrv_size:
                    return key
        return None