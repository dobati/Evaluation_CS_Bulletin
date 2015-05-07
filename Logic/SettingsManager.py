__author__ = 'Till'
from os import path

project_dir = path.dirname(path.dirname(__file__))  #  required to create somewhat cwd independent paths
__settings_file = path.abspath(path.join(project_dir, "settings.conf"))

__input_dict = dict()
execfile(__settings_file, __input_dict)

pdf_input_dir = u"" + path.abspath(path.join(project_dir, __input_dict["pdf_input_dir"]))
headings_input_dir = u"" + path.abspath(path.join(project_dir, __input_dict["headings_input_dir"]))
tetml_output_dir = u"" + path.abspath(path.join(project_dir, __input_dict["tetml_output_dir"]))
prettyprinter_output_dir = u"" + path.abspath(path.join(project_dir, __input_dict["prettyprinter_output_dir"]))
xml_output_dir = u"" + path.abspath(path.join(project_dir, __input_dict["xml_output_dir"]))

testcases_input_dir = u"" + path.abspath(path.join(project_dir, __input_dict["testcases_input_dir"]))
testcases_output_dir = u"" + path.abspath(path.join(project_dir, __input_dict["testcases_output_dir"]))

prettyprinter_template_html = u"" + path.abspath(path.join(project_dir, __input_dict["prettyprinter_template_html"]))
headings_history_generator_output = u"" + path.abspath(path.join(project_dir, __input_dict["headings_history_generator_output"]))

webserver_pdf_path = __input_dict["webserver_pdf_path"]
webserver_prettyprint_path = __input_dict["webserver_prettyprint_path"]

text_berg_executable = u"" + path.abspath(path.join(project_dir, __input_dict["text_berg_executable"]))