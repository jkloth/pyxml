#!/usr/bin/python

from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys, getopt

# =============================================================================
# Functions
# =============================================================================

def usage(message = ""):
    
    print "A utility for testing architectural from processing with xmlarch.py."
    print "Usage: archtest.py --options* archname file.xml"
    print "Parameters: --debug    : write debug information to stdout"
    print message
    sys.exit(1)

def create_hash(optlist):
    
    # Create hash table out of an item list
    opthash = {}
    for a in optlist:
	opthash[a[0]] = a[1]
    return opthash

# =============================================================================
# MAIN PROGRAM
# =============================================================================


try:
    # Read options from command line
    optlist, args = getopt.getopt(sys.argv[1:], "", ["debug"])
    opts = create_hash(optlist)

    # Get debug flag setting
    if opts.has_key("--debug"):
	debug = 1
    else:
	debug = 0

    if len(args) != 2:
	usage("Please give me two arguments.")
	
# Catch getopt errors and display usage information
except getopt.error, e:
	usage(e)

# Create Parser factory
pf=saxexts.ParserFactory([
    "xml.sax.drivers.drv_xmlproc",
    "xml.sax.drivers.drv_xmlproc_val",
    "xml.sax.drivers.drv_pyexpat",
    "xml.sax.drivers.drv_sgmlop", 
    "xml.sax.drivers.drv_xmllib", 
    "xml.sax.drivers.drv_xmltok",
    "xml.sax.drivers.drv_xmltoolkit",
    "drv_xmldc.py"])

# Create parser
parser = pf.make_parser()

# Create architectures handler and reqister it with the parser
arch_handler = xmlarch.ArchDocHandler()

parser.setDocumentHandler(arch_handler)
parser.setErrorHandler(saxutils.ErrorPrinter())
# parser.setLocale("no")

# Set the debug flag
if debug: arch_handler.set_debug(debug, sys.stderr)

# Register architecture document handlers
arch_handler.addArchDocumentHandler(args[0], xmlarch.Normalizer(sys.stdout))

if debug:
    print "Parsing with:", parser.get_parser_name(), parser.get_parser_version()
    print "Starting architectual parsing..."

# Parse an architectural document
try:
    parser.parse(args[1])
except xmlarch.ArchException, e:
    sys.stderr.write("ArchException: " + str(e) + "\n")

if debug: print "Finished architectual parsing..."



