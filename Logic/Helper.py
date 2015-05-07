import subprocess
import os.path as path
import glob

__author__ = 'Till'


def get_files_in_directory(abs_sourcedir, file_extension="*.tetml"):
    sourcedir_glob = path.join(abs_sourcedir, file_extension)
    files = sorted(glob.glob(sourcedir_glob))
    return files


def replace_extension_and_path(absolute_file, output_dir, prev_extension, new_extension):
    file_name = path.basename(absolute_file)
    file_name = file_name.replace(prev_extension, new_extension)
    output_file = path.join(output_dir, file_name)
    return output_file


def launch_by_commandline(command):
    try:
        subprocess.check_call(command.split())
    except Exception as ex:
        print(ex)