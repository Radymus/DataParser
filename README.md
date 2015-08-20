DataParser
==========

This is simple program which takes log file in some format and based by regexp will parsed
this log. Over this data is calculated simple statistics min, max, avg, std and can be printout
graph. For other data manipulation can be parsed data saved in csv format.

Dependencies::
    pylab, pyside

This program can be run in command line:
python main.py file -r "(/w+);(/w+);(\d{2})" -g -s
or in gui written in pyqt
python main.py

