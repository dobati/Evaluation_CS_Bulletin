import codecs
import re
from lxml import etree
__author__ = 'Till'

""" Contains the most used XML tags and all parser functionality """

# TET tags
TET_div_tag = "Para"
TET_word_tag = "Word"
TET_pages_tag = "Pages"
TET_page_tag = "Page"
TET_placedimage_tag = "PlacedImage"
TET_glyph_tag = "Glyph"
TET_box_tag = "Box"
TET_font_tag = "Font"


# Our tags
book_tag = "book"
div_tag = "div"
word_tag = "w"
text_tag = "Text"
graphic_tag = "graphic"
pb_tag = "pb"

heading_attr = "heading"
article_heading = "article"  # defines the heading-tag from the headings xml that will be wrapped into a "<article>" tag: <div heading=[article_heading]> --> <article><div...></article>

check_all = ".//"

# removes the namespace and parses the file
def parse(filename):
    no_namespace = __remove_namespace(filename)
    parser = etree.XMLParser(encoding="utf-8")
    xml = etree.fromstring(no_namespace, parser)
    return xml


def __remove_namespace(filename):
    with codecs.open(filename, "r") as the_file:
        orig_string = the_file.read()
        string_nonamespace = re.sub('<TET (.*\n)* version="4.2">', "<TET>", orig_string)

    return string_nonamespace


def __find(elem, target, all=""):
    item = elem.find(all + target)
    assert item is not None
    return item


def find_all(elem, target):
    return __find(elem, target, all=check_all)


def __findall(elem, target, all=""):
    targets = elem.findall(all + target)
    assert len(targets) > 0
    return targets


def findall(elem, target):
    return __findall(elem, target)


def findall_all(elem, target):
    return __findall(elem, target, all=check_all)


def xpath_all(elem, target):
    targets = elem.xpath(check_all + target)
    assert len(targets) > 0
    return targets