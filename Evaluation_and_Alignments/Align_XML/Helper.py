__author__ = 'Dolores'

import os.path as path
import glob
import SettingsManager


def get_files_in_directory(abs_sourcedir, file_extension="*.xml"):
    sourcedir_glob = path.join(abs_sourcedir, file_extension)
    files = sorted(glob.glob(sourcedir_glob))
    return files

#print get_files_in_directory(SettingsManager.parallel_xml_dir, "*.xml")

