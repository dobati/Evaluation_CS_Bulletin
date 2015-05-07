__author__ = 'Till'

""" Datastructure which holds data for font abbreviation/font-size, e.g. "ACaslonPro 32" """
class FontAbbrvSize:
    def __init__(self, font_abbrv, size):
        self.font_abbrv = font_abbrv
        self.font_size = size

    def __eq__(self, other):
        if self.font_abbrv == other.font_abbrv:
            if self.font_size == other.font_size:
                return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)