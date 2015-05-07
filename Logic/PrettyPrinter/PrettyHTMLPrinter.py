# -*- coding: utf-8 -*-
__author__ = 'Till'

from lxml import html
import codecs
from os import path
import re
from lxml import etree
from Logic import Parser
from Logic import Helper
from Logic.DivHandling import FreeWords2Div
from Logic.Headings import FontManager
from Logic.DivHandling.DivStructurer import DivStructurer
from Logic.DivHandling.TokenizerAdapter import TokenizerAdapter
from Logic import SettingsManager

""" This class creates the pretty printed HTML files.
    It uses the "template.html" and dynamically builds a table. """
class PrettyHTMLPrinter:
    def __init__(self):
        self.template_path = SettingsManager.prettyprinter_template_html

        # load the template.html which contains all static data
        self.template_html = html.parse(self.template_path)
        self.body = Parser.find_all(self.template_html, "body")
        # the table is dynamically generated
        self.table = html.Element("table")
        table_div = self.body.get_element_by_id("tableDiv")
        table_div.append(self.table)

    def start(self, tetml_file, output_path):
        self.__put_pdfname_into_div(tetml_file)

        output_file = Helper.replace_extension_and_path(tetml_file, output_path, ".tetml", "_prettyprint.html")
        xml = Parser.parse(tetml_file)
        FreeWords2Div.put_free_words_into_div(xml, Parser.TET_word_tag, Parser.TET_div_tag)
        FontManager.create_font_to_abbrv_mapping(xml)

        with codecs.open(output_file, "w", "utf-8") as html_file:
            DivStructurer(Parser.TET_div_tag, Parser.TET_word_tag, FontManager).unravel_divs(xml)

            for element in xml.iter(Parser.TET_div_tag, Parser.TET_page_tag):
                tr = html.Element("tr")
                self.table.append(tr)

                if element.tag == Parser.TET_page_tag:
                    td = self.__create_td(tr)
                    self.__attach_page_link(td, element.get("number"))

                elif element.tag == Parser.TET_div_tag:
                    fontabbrv = FontManager.get_fontabbrvsize(element[0])
                    first_td = self.__create_td(tr)
                    first_span = self.__append_span(first_td)
                    self.__set_span_style(first_span, 'font-size:' + fontabbrv.font_size + 'pt;')
                    second_td = self.__create_td(tr)
                    second_span = self.__append_span(second_td)

                    # put text into table
                    first_span.text = self.prepare_text_1stdiv(element)
                    second_span.text = fontabbrv.font_abbrv + " " + fontabbrv.font_size

            html_file.write(html.tostring(self.template_html, pretty_print=True))

    def __put_pdfname_into_div(self, tetml_file):
        file_name = path.basename(tetml_file).replace(".tetml", ".pdf")
        pdf_file_url = SettingsManager.webserver_pdf_path + file_name

        filename_div = self.body.get_element_by_id("pdfFileName")
        filename_div.set("name", pdf_file_url)

    def __append_span(self, td):
        span = html.Element("span")
        td.append(span)
        return span

    def __create_td(self, tr):
        td = html.Element("td")
        tr.append(td)
        return td

    def __set_span_style(self, span, span_style):
        span.set("style", span_style)
        span.text = r""  # change type from None to String

    def __attach_page_link(self, td, page_number):
        a = html.Element("a")
        a.set("name", page_number)
        a.text = "Page Number " + page_number
        td.append(a)

    def prepare_text_1stdiv(self, fontblock):
        # In order to reuse the TokenizeAdapter, we need to wrap div into parent tag
        par_div = fontblock[0].getparent()
        new_root = etree.Element("root")
        new_root.append(par_div)

        # run TokenizerAdapter & beautifier to extract nicely formatted text
        tokenizer = TokenizerAdapter(Parser.TET_div_tag, Parser.TET_word_tag)
        return_xml = tokenizer.start(new_root)
        final_div = Parser.find_all(return_xml, Parser.TET_div_tag)
        final_text = self.__beautify_text(final_div.text)
        return final_text

    # beautify the text for better readability
    def __beautify_text(self, text):
        if text is None:
            return ""

        td_text = text.strip()
        # remove any whitespaces [in front of] the following characters:
        td_text = re.sub(" ([\.,:;!\?\)»])", "\g<1>", td_text)

        # remove any whitespaces [after] the following characters:
        td_text = re.sub("([«\(]) ", "\g<1>", td_text)

        # L ' article --> L'article
        td_text = re.sub(" (’) ", "\g<1>", td_text)

        return td_text