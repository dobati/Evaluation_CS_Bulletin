__author__ = 'Till'
from lxml import etree
from Logic import Parser
from itertools import islice

""" The Text & Berg Pipeline requires everything that should be processed to be in <article> tags.
    This class puts everything that comes before the first real <article> into a 'zero article', that is, <article n=0>.
    This class also looks for any heading = article and wraps them into a parent <article> tag. """
class ArticleInjector:
    def __init__(self, div_tag, last_elem):
        self.div_tag = div_tag
        self.last_elem = last_elem

    def add_article_tags(self, tree):
        all_divs = Parser.findall_all(tree, self.div_tag)
        article_divs = self.__get_all_articledivs(tree)
        assert len(article_divs) > 0, 'No articles found. Did you define them as \"' + str(Parser.article_heading) + '\" in the headings file?'

        self.__wrap_content_prior_first_article(tree, all_divs[0], article_divs[0])
        self.__surround_with_article_tag(tree, article_divs)

    def __get_all_articledivs(self, tree):
        # XPath query: ".//Para[@heading='article']"
        article_divs = Parser.xpath_all(tree, self.div_tag + "[@" + Parser.heading_attr + "=\'" + Parser.article_heading + "\']")
        return article_divs

    """ The Text&Berg Pipeline expects everything that should be processed by the treetagger to be wrapped into <article> tags"""
    def __wrap_content_prior_first_article(self, tree, first_div, first_article):
        article_zero = self.__setup_article_zero(first_div)
        it, next_elem = self.__setup_iterator(first_div, tree)

        while next_elem is not first_article:
            article_zero.append(next_elem)
            next_elem = it.next()

    def __setup_article_zero(self, first_div):
        article_zero = self.__create_new_article_elem()
        self.__set_as_parent_node(article_zero, first_div)
        self.__set_article_pagenumber(article_zero, 0)
        return article_zero

    def __setup_iterator(self, first_div, tree):
        it = tree.iter()
        next_elem = it.next()

        while next_elem is not first_div:
            next_elem = it.next()

        return it, next_elem

    def __surround_with_article_tag(self, tree, article_divs):
        articles = list(article_divs)
        last_elem = Parser.find_all(tree, self.last_elem)
        # the last article should span over until the last para
        articles.append(last_elem)
        # we want to loop until 2nd to last element because we always access array until n+1
        length = len(articles) - 1
        for div in islice(articles, length):
            index = articles.index(div)
            article_elem = self.__wrap_into_article_tag(div, index + 1)
            next_article = articles[index + 1]
            it, next_elem = self.__setup_iterator(div, tree)

            while next_elem is not next_article:
                article_elem.append(next_elem)
                try:
                    next_elem = it.next()
                # the last last tag can't access the parent closing tag with next()
                # Todo: Is there a neater way to write this?
                except StopIteration:
                    article_elem.append(next_elem)
                    break

    def __wrap_into_article_tag(self, current_article, article_number):
        article_elem = self.__create_new_article_elem()
        self.__set_as_parent_node(article_elem, current_article)
        self.__set_article_pagenumber(article_elem, article_number)
        return article_elem

    def __create_new_article_elem(self):
        article_elem = etree.Element("article")
        return article_elem

    def __set_as_parent_node(self, article_elem, current_article):
        current_article.addprevious(article_elem)
        article_elem.insert(0, current_article)  # <div> is child of <article>

    """ The Text&Berg tokenizer requires every article to have a n-attribute """
    def __set_article_pagenumber(self, article_elem, value):
        article_elem.set("n", str(value))