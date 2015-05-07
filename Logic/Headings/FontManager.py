__author__ = 'Till'
from Logic import Parser
from Logic.Headings.FontAbbrvSize import FontAbbrvSize
import re

""" This module holds the dictionary to map between TET font ID 'F0' and our simplified fontnames 'AkzidenzGrotesk'
    It also contains methods to get/set that dictionary """
font_abbrv_to_name = dict()  # maps TET font id ("F0") to our simplified fontnames ("AkzidenzGrotesk")

""" Returns the fontabrvsize of a given word.
    Note that the last character of the word is used.
    This helps to prevent that a word is being written in huge letters because the first character was an initial. """
def get_fontabbrvsize(word):
    boxes = Parser.findall_all(word, Parser.TET_box_tag)  # there can be more than 1 box per word
    glyph = Parser.find_all(boxes[-1], Parser.TET_glyph_tag)  # boxes[-1] avoids that whole word is written in huge letters if first char is an initial
    font_abbrv = glyph.get("font")
    font_name = font_abbrv_to_name[font_abbrv]
    font_size = glyph.get("size")
    return FontAbbrvSize(font_name, font_size)

# builds the dictionary
def create_font_to_abbrv_mapping(xml):
    fonts = Parser.findall_all(xml, Parser.TET_font_tag)
    for font in fonts:
        abbrv = font.get("id")
        name = font.get("name")

        simplified_fontname = __simplify_fontname(name)
        if simplified_fontname:     # there might have been no "-" in the fontname
            name = simplified_fontname.group(1)
        font_abbrv_to_name[abbrv] = name


""" This method defines how the font names are simplified
    We keep the string left to the "-":
    'AkzidenzGrotesk-Light' --> 'AkzidenzGrotesk'
"""
def __simplify_fontname(name):
    name_without_details = re.search("(\w*)-\w*", name)
    return name_without_details