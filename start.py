import getopt
import sys
from StartPDF2TETML import StartPDF2TETML
from StartPrettyPrint import StartPrettyPrint
from StartTETML2XML import StartTETML2XML
from Logic import Helper
from Logic import SettingsManager

__author__ = 'Till'

def usage():
    print """There are 4 steps you can control:
    PDF2TET: start.py -p OR --pdf2tet
    TET2XML: start.py -t OR --tet2xml
    PrettyPrint: start.py -y OR --prettyprint
    Tokenizing & Tagging: start.py -b OR --textberg

    By default all 4 steps are executed.
    If you want to execute only parts, select them explicitly
    Example: starting pdf2tet and prettyprint without tet2xml
    start.py -p -y """

def parse_arguments(argv):
    tb_exec = SettingsManager.text_berg_executable

    pdf2tet = False
    tet2xml = False
    prettyprint = False
    textberg = False

    try:
        opts, args = getopt.getopt(argv, "ptybh", ["pdf2tet", "tet2xml", "prettyprint", "textberg", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--pdf2tet"):
            pdf2tet = True
        elif opt in ("-t", "--tet2xml"):
            tet2xml = True
        elif opt in ("-y", "--prettyprint"):
            prettyprint = True
        elif opt in ("-b", "--textberg"):
            textberg = True

    if pdf2tet is tet2xml is prettyprint is textberg is False:
        pdf2tet = True
        tet2xml = True
        prettyprint = True
        textberg = True

    if pdf2tet:
        StartPDF2TETML().start()
    if prettyprint:
        StartPrettyPrint().start()
    if tet2xml:
        StartTETML2XML().start()
    if textberg:
        command = "python " + tb_exec
        Helper.launch_by_commandline(command)


if __name__ == "__main__":
    parse_arguments(sys.argv[1:])
