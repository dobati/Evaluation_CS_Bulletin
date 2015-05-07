import Logic.Parser as Parser
from lxml import etree
import os
__author__ = 'Till'

class TagHandler:
    def __init__(self):
        pass

    def rename_tags(self, xml):
        self.__rename_tag(xml, Parser.TET_pages_tag, Parser.book_tag)
        self.__rename_tag(xml, Parser.TET_div_tag, Parser.div_tag)
        self.__rename_tag(xml, Parser.TET_word_tag, Parser.word_tag)
        self.__rename_tag(xml, Parser.TET_placedimage_tag, Parser.graphic_tag)

    def __rename_tag(self, xml, tag, new_tag):
        all_tags = Parser.findall_all(xml, tag)
        for tag in all_tags:
            tag.tag = new_tag

    # strip_tags deletes the parent while preserving the children tags
    def strip_tags(self, xml):
        etree.strip_tags(xml, "Document")
        etree.strip_tags(xml, "Content")
        etree.strip_tags(xml, "Table")
        etree.strip_tags(xml, "Row")
        etree.strip_tags(xml, "Cell")

    # strip_elements removes children and tail text
    def strip_elements(self, xml):
        etree.strip_elements(xml, "Creation")
        etree.strip_elements(xml, "DocInfo")
        etree.strip_elements(xml, "Metadata")
        etree.strip_elements(xml, "Options")
        etree.strip_elements(xml, "Resources")
        etree.strip_elements(xml, Parser.TET_box_tag)  # removes <Box> and <Glyphs>

    # converts pb to empty tag: <pb></pb> to </pb>
    def convert_pbtags_to_emptytag(self, xml):
        all_pbs = Parser.findall_all(xml, Parser.TET_page_tag)
        for pb in all_pbs:
            pb.tag = Parser.pb_tag
            del pb.attrib["width"]
            del pb.attrib["height"]
            pb.tail = None
            pb.text = None

            for child in reversed(pb):
                pb.addnext(child)  # promote child to sibling

    def remove_tet_tag(self, xml):
        book_tag = Parser.find_all(xml, Parser.book_tag)
        xml._setroot(book_tag)

    # The Text & Berg pipeline expects a "lang" attribute in the <book> tag
    def book_set_lang_attribute(self, xml, absolute_filename):
        filename = os.path.splitext(os.path.basename(absolute_filename))[0]  # extract filename without extension
        token = filename.split("_")[-1]  # split by "_" and pick last token
        book_language = None

        if token == "de":
            book_language = "de"
        elif token == "en":
            book_language = "en"
        elif token == "fr":
            book_language = "fr"
        elif token == "it":
            book_language = "it"
        assert book_language is not None, "Couldn't derive language from filename.\n Filename must end on '_de', '_en', '_fr' or '_it'"

        book_tag = xml.getroot()
        book_tag.set("lang", book_language)

    def remove_empty_lines(self, xml):
        parser = etree.XMLParser(encoding="UTF8", remove_blank_text=True)
        xml_no_empty_lines = etree.fromstring(etree.tostring(xml, encoding="UTF8"), parser=parser)
        root_tree = xml_no_empty_lines.getroottree()

        return root_tree