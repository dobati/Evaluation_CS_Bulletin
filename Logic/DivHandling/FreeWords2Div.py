__author__ = 'Till'

from Logic import Parser
from lxml import etree


""" TETML contains <Word>-tags with no parent <Para>. We wrap all <Word>-Tags into parent divs. """
def put_free_words_into_div(tree, word_tag, div_tag):
    all_words = Parser.findall_all(tree, word_tag)
    for word in all_words:
        parent_tag = word.getparent().tag
        if parent_tag != div_tag:
            div_elem = etree.Element(div_tag)
            next_free_word = __insert_and_get_next_node(word, div_elem)

            while next_free_word is not None and next_free_word.tag == word_tag:
                next_free_word = __append_and_get_new_node(div_elem, next_free_word)


def __insert_and_get_next_node(word, div_elem):
    next_free_word = word.getnext()  # without this getnext() would result in none as there aren't any next siblings in the new div
    word.addprevious(div_elem)
    div_elem.insert(0, word)  # <word> is child of <div>
    return next_free_word


def __append_and_get_new_node(div_elem, next_free_word):
    next_word = next_free_word.getnext()  # getnext() needs to be called before appending or it would result in none as there aren't any next siblings in the new div
    div_elem.append(next_free_word)
    return next_word
