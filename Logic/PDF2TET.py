from Logic import Helper
import os

__author__ = 'Till'

""" Converts PDF to TETML by using the PDFLib TET command line tool """
class TET:

    def __init__(self, absolute_pdf_input_dir, absolute_output_dir):
        self.__absolute_input_dir = absolute_pdf_input_dir
        self.__absolute_output_dir = absolute_output_dir

    def convert(self):
        tet_exec = "tet"
        tet_params = " -m wordplus --targetdir "
        input_path = os.path.abspath(self.__absolute_input_dir)
        output_path = os.path.abspath(self.__absolute_output_dir)

        command = tet_exec + tet_params + output_path + " "
        files = Helper.get_files_in_directory(input_path, "*.pdf")
        if not files:
            print "Please create PDF input directory: " + input_path
            return

        print "Converting PDFs to TETML\n" \
              + input_path + " --> " + output_path
        for file_name in files:
            print "Processing " + os.path.basename(file_name)
            final_command = command + file_name
            Helper.launch_by_commandline(final_command)

