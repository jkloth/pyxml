"""
A simple command-line interface to the DTD parser. Intended for those rare
cases when one wants to just parse a DTD and nothing more.
"""

import sys
from xml.parsers.xmlproc import xmlproc,dtdparser,utils

# --- Doco

usage=\
"""
Usage:

  python dtdcmd.py <urltodtd>  
"""

# --- Head

print
print "xmlproc version %s" % xmlproc.version

# --- Argument interpretation

if len(sys.argv)<2:
    print usage
    sys.exit(1)

# --- Initialization

parser=dtdparser.DTDParser()
parser.set_error_handler(utils.ErrorPrinter(parser))

print "Parsing"
parser.parse_resource(sys.argv[1])
print "Parsing complete"
