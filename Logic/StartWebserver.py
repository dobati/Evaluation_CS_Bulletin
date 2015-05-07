import os
import sys
sys.path.insert(0, '../')
import Helper
import SettingsManager

__author__ = 'Till'

class StartWebserver:
    def __init__(self):
        self.command = "python -m SimpleHTTPServer"

    def start(self):
        self.__change_dir_to_projectroot()
        self.__print_urls()
        Helper.launch_by_commandline(self.command)

    def __change_dir_to_projectroot(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        # Change to root dir
        os.chdir(module_dir)
        os.chdir("..")
        os.chdir("..")

    def __print_urls(self):
        htmls = self.__get_all_html_files()
        print "\nThe links for all available HTML files:"
        for html in htmls:
            filename = os.path.basename(html)
            print SettingsManager.webserver_prettyprint_path + filename
        print "\n"

    def __get_all_html_files(self):
        pretty_path = SettingsManager.prettyprinter_output_dir
        htmls = Helper.get_files_in_directory(pretty_path, "*.html")
        return htmls

if __name__ == "__main__":
    StartWebserver().start()