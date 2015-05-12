import codecs
from lxml import etree
import os
from flask import Flask, request
import json
from Logic import SettingsManager
from Logic import Parser
from Logic import Helper

__author__ = 'Till'


class FlaskWebServer:
    def __init__(self):
        self.PORT = 5000
        self.__print_urls()

        self.app = Flask(__name__, static_folder=SettingsManager.project_dir)
        self.app.add_url_rule('/', 'list_all_htmls', self.__list_all_htmls)
        self.app.add_url_rule('/<path:path>', 'serve_static_content', self.__serve_static_content)
        self.app.add_url_rule('/uploadajax', 'upload', self.__trigger_file_creation, methods=['POST'])
        self.app.run(port=self.PORT)

    # displays all available pretty printed htmls as links
    def __list_all_htmls(self):
        urls = self.__get_all_urls(self.__get_all_html_files())
        return_string = ""
        for url in urls:
            return_string += "<a href=" + url + ">" + url + "</a>" + "<br/>"

        return return_string

    # required to serve static files
    def __serve_static_content(self, path):
        # send_static_file will guess the correct MIME type
        return self.app.send_static_file(path)

    def __trigger_file_creation(self):
        filename, data = self.__read_input()
        self.__write_into_file(filename, data)
        return json.dumps({filename: data})

    def __get_all_urls(self, htmls):
        urls = []
        for html in htmls:
            filename = os.path.basename(html)
            urls.append(SettingsManager.webserver_prettyprint_path + filename)

        return urls

    def __print_urls(self):
        htmls = self.__get_all_html_files()
        print "\nThe links for all available HTML files:"
        urls = self.__get_all_urls(htmls)
        for url in urls:
            print url
        print "\n"

    def __get_all_html_files(self):
        pretty_path = SettingsManager.prettyprinter_output_dir
        htmls = Helper.get_files_in_directory(pretty_path, "*.html")
        return htmls

    def __read_input(self):
        raw_data = json.loads(request.get_data())
        filename = raw_data.keys()[0]
        xml_data = raw_data.values()[0]
        return filename, xml_data

    # TODO: I couldn't find a more concise way to output the xml as pretty print
    def __write_into_file(self, fname, xml_data):
        file_w_path = os.path.join(SettingsManager.headings_input_dir, fname)
        with codecs.open(file_w_path, "w", "utf-8") as the_file:
            the_file.write(xml_data)

        xml_data2 = Parser.parse_dtd(file_w_path)

        with codecs.open(file_w_path, "w", "utf-8") as the_file:
            the_file.write(etree.tostring(xml_data2, pretty_print=True, encoding="utf-8"))


if __name__ == '__main__':
    FlaskWebServer()