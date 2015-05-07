import sys
sys.path.append('..')

import TestHelper
import unittest
import os.path
from Logic.PrettyPrinter.PrettyHTMLPrinter import PrettyHTMLPrinter
from Logic import Helper

__author__ = 'Till'

""" Succeeds if all text is preserved and order of text is correct """
class PrettyHTMLPrinterTest(unittest.TestCase):
    def test_output_preserved(self):
        input_file = "referenzCS_de.tetml"
        input_file_abs = os.path.abspath(os.path.join("Input", input_file))
        output_path = os.path.abspath("Output")

        printer = PrettyHTMLPrinter()
        printer.start(input_file_abs, output_path)

        input_original = os.path.abspath(os.path.join("Input", "referenzCS_de_prettyprint.html"))
        generated_file = Helper.replace_extension_and_path(input_file, output_path, ".tetml", "_prettyprint.html")
        origial_content = TestHelper.get_file_content(input_original)
        test_content = TestHelper.get_file_content(generated_file)

        self.assertEqual(test_content, origial_content)