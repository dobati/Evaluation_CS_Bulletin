# -*- coding: utf-8 -*-

__author__ = 'Till'
from Logic import Parser
from lxml import etree
import re

""" This class merges the text of the words into the divs by adding spaces inbetween words
    Moreover special modifications such as URL detection are done here
    This is required as the T&B Pipeline expects this input"""
class TokenizerAdapter:
    def __init__(self, div_tag, word_tag):
        self.div_tag = div_tag
        self.word_tag = word_tag

    def start(self, xml):
        self.__put_text_to_wordtag(xml)
        self.__merge_into_divs(xml)
        xml_ord = self.__fix_ordinal_numbers(xml)
        xml_guill = self.__fix_guillemets(xml_ord)
        xml_url = self.fix_urls(xml_guill)

        return xml_url

    # also removes <Text> tags
    def __put_text_to_wordtag(self, xml):
        all_words = Parser.findall_all(xml, self.word_tag)
        for word in all_words:
            text = Parser.find_all(word, Parser.text_tag)
            word.text = text.text
            word.remove(text)

    """ Puts the content of <w> into it's parent <div> and removes <w>.
        Required for Text & Berg tokenizer """
    def __merge_into_divs(self, xml):
        all_divs = Parser.findall_all(xml, self.div_tag)
        for div in all_divs:
            all_words = Parser.findall(div, self.word_tag)
            tail_text = ""

            for word in all_words:
                if word.text is not None: # some TETML files contain words without text (bulletin_2007_3_Adrenalin_fr.tetml)
                    tail_text += " " + word.text

            if div.tail is None:
                div.tail = str()
            div.text = tail_text

            etree.strip_elements(div, self.word_tag)

    # "17 ." --> "17."
    def __fix_ordinal_numbers(self, xml):
        string = etree.tostring(xml, encoding="UTF8")
        matches = re.sub("(\d) (\.)", "\g<1>\g<2>", string)
        return self.__create_roottree_from_string(matches)

    # "« Versicherungen »" --> "«Versicherungen»" to avoid that closing guillemet is considered as part of next sentence
    def __fix_guillemets(self, xml):
        string = etree.tostring(xml, encoding="UTF8")
        left_g_matches = re.sub(r"(«) ", "\g<1>", string)    # remove whitespace
        right_g_matches = re.sub(r" (»)", "\g<1>", left_g_matches)

        return self.__create_roottree_from_string(right_g_matches)

    """Detects website & email addresses:
    Working examples:
    -----------------
    http :// www . website . com / ?key=val#anchor
    http :// www . website . com / test1 / test2 /
    www . subhost . host-name . com
    info @ dummy . com
    firstname . lastname @ host . com

    NOTPART is ignored successfully:
    --------------------------------
    http :// www . test . com / regularpath NOTPART
    www . test . com NOTPART
    info @ youtube . com NOTPART
    """
    def fix_urls(self, xml):
        string = etree.tostring(xml, encoding="UTF8")
        regex = r"(?:https? :// )?www \.(?: \S+ \.)+ [a-z]+(?: / ?\S*)*/?|(?:\S+ \. )*\S+ @ \S+ \. [a-z]+"
        matches = re.findall(regex, string)

        nospace_list = list()
        for match in matches:
            nospace_list.append(match.replace(" ", ""))

        for index, match in enumerate(matches):
            escaped_match = re.escape(match)  # 'www . credit-suisse . ch / directnet /)' would result in crash
            string = re.sub(escaped_match, nospace_list[index], string)

        return self.__create_roottree_from_string(string)

    def __create_roottree_from_string(self, string):
        xml = etree.fromstring(string)
        xmltree = xml.getroottree()
        return xmltree



