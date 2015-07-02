__author__ = 'Dolores'
from os import path

project_dir = path.dirname(path.dirname(__file__))  #  required to create somewhat cwd independent paths
__settings_file = path.abspath(path.join(project_dir, "Align_XML/settings.conf"))

__input_dict = dict()

execfile(__settings_file, __input_dict)

parallel_xml_dir = u"" + path.abspath(path.join(project_dir, __input_dict["parallel_xml_dir"]))
aligned_xml_files = u"" + path.abspath(path.join(project_dir, __input_dict["aligned_xml_files"]))

# Checked
#print project_dir
#print __settings_file
#print parallel_xml_dir
#print aligned_xml_dir