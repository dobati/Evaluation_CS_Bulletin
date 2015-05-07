import codecs

__author__ = 'Till'

def get_file_content(filename):
    with codecs.open(filename, "r", "utf-8") as the_file:
        lines = the_file.readlines()

    return lines