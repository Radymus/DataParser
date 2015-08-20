__author__ = 'Radim Spigel'
__version__ = '1.0'

import re
import pylab
from datetime import datetime
import logging
import sys
LOG_FORMAT = "(asctime)s:%(message)s"
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def print_help():
    print ""
    print "This program takes file for statistics, for correct work in command line"
    print "is need to be setup 2 parameters FILE and REGEX other parameters are"
    print "optimal. REGEXP is for format of data in file."
    print "Parameters:"
    print "-r for regex"
    print "-g for allow graphs"
    print "-sp for separate graphs"
    print "-ns for disable statistics"
    print "--csv [file] to convert to csv file, data will be save in format YYYY-MM-DD_HH-mm-ss.csv"
    print "numbers are saved like float with , for separating of columns is used ;"
    print "example: "
    print 'python %s file -r "(/w+);(/w+);(\d{2})" -g -s' % sys.argv[0]
    print


class DataParser(object):
    """
    ##  DataParser
    ## This class selects data from current file based by regex.
    ## @param fname name of file
    """

    def __init__(self, fname):
        self._file = fname
        self.compiled = None
        self.dictionary = None

    """
    ##  from_command_line
    ## This method takes list of arguments and evaluate this over data
    ## @param args this is list of arguments
    """
    def from_command_line(self, args):
        if len(args) <= 0:
            print_help()
            return
        g, s, n = False, False, False
        csv = False
        regex = None
        for idx, opt in enumerate(args):
            if opt == '-g':
                g = True
            if opt == '-sp':
                s = True
            if opt == '-ns':
                n = True
            if opt == '--csv':
                csv = True
            if opt == '-r':
                regex = args[idx+1]
        if regex is None:
            log.error("ERROR: regex must be set")
            print_help()
            return
        self.init_regex(regex)
        self.filled_data()
        if not n:
            self.print_statistics()
        if csv:
            self.save_to_csv()
        if g:
            self.print_graphs(s)

    """
    ## init_regex
    ## This method creates csv file
    ## @param fname name of file
    """
    def save_to_csv(self, fname="{}.csv".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))):
        with open(fname, "w") as wfile:
            size = len(self.dictionary[self.dictionary.keys()[0]])
            for idx in xrange(size):
                line = ""
                for key in self.dictionary.keys():
                    line += "{};".format(self.dictionary[key][idx]).replace(".", ",")
                wfile.write(line)
                wfile.write('\n')
    """
    ## init_regex
    ## This method checks and create regex getted from gui
    ## @param regex argument for regex gets from gui
    """
    def init_regex(self, regex):
        try:
            self.compiled = re.compile(regex)
        except Exception as e:
            log.error("Wrong regex {0}".format(regex))
            return None

    """
    ## create_structure
    ## This method create structure for evaluation
    ## @param needed_groups string contains int for elements in group what
    ##      we wanna eval.
    ## example: 1,2,3,4,5,6
    #def create_structure(self, needed_groups):
     #   splited = needed_groups.split(",")
     #   self.dictionary = {idx: [] for idx in splited}
    ## filled_data
    ## This method filled structure with data before this method
    ## is need to be called init_regex() and create_structure()
    """
    def filled_data(self):
        flag = False
        if self.dictionary is None:
            flag = True
            self.dictionary = {}
        else:
            self.dictionary = {}
        try:
            with open(self._file) as file:
                for line in file:
                    found = self.compiled.search(line)
                    if found is not None:
                        if flag:
                            for idx, item in enumerate(found.groups()):
                                if idx == '' or idx is None:
                                    continue
                                if idx not in self.dictionary:
                                    self.dictionary[idx] = []
                                self.dictionary[idx].append(item)
                        else:
                            for key in self.dictionary.keys():
                                self.dictionary[key].append(float(found.group(int(key))))
            if self.dictionary.has_key(''):
                del self.dictionary['']
        except Exception as e:
            log.error("Error when program parsing this file {0}".format(self._file))
            return None

    """
    ## print_graphs
    ## This method print graphs for dictionary of data
    ## @param subplot bool type if we wanna subplots
    ## @param diffrent_data is dictionary. By default is setted
    ##      to None if we wanna plot data gets from file.
    ##      If we want to print diffrent data
    ##      this is argument for that.
    """
    def print_graphs(self, subplot, diffrent_data=None):
        if diffrent_data is None:
            print_data = self.dictionary
        else:
            print_data = diffrent_data
        if subplot:
            subplot = len(print_data) * 100 + 10
            for ix, key in enumerate(print_data):
                pylab.subplot(int(subplot + ix + 1))
                pylab.plot(print_data[key])
        else:
            for key in print_data:
                pylab.plot(print_data[key])
        pylab.show()

    """
    ## print_statistics
    ## This method print to stdout max, min, avg for each data
    ## @param diffrent_data is dictionary. By default is setted
    ##      to None if we wanna print statistics for data gets from file.
    ##      If we want to print diffrent data
    ##      this is argument for that.
    """
    def print_statistics(self, diffrent_data=None):
        if diffrent_data is None:
            data = self.dictionary
        else:
            data = diffrent_data
        for key in data:
            log.info("Key > {}".format(key))
            data[key] = [float(i) for i in data[key]]
            log.info("\tMax > {}".format(max(data[key])))
            log.info("\tMin > {}".format(min(data[key])))
            log.info("\tAvg > {}".format(pylab.mean(data[key])))
            log.info("\tStd > {}".format(pylab.std(data[key])))