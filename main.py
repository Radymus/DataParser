__author__ = 'Radim Spigel'
__version__ = '1.0'
import sys
from dataparser import print_help, DataParser
from qtgui import qt_main


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print sys.argv
        if '-h' in sys.argv:
            print_help()
            sys.exit()
        datagetter = DataParser(sys.argv[1])
        datagetter.from_command_line(sys.argv[1:])
    elif len(sys.argv) > 6:
        print_help()
    else:
        qt_main()