#!/usr/bin/env python

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
    print "            --validate : use a validating parser"
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
    optlist, args = getopt.getopt(sys.argv[1:], "", ["debug", "validate"])
    opts = create_hash(optlist)

    if len(args) != 2:
        usage("Please give me two arguments.")
        
# Catch getopt errors and display usage information
except getopt.error, e:
        usage(e)

# Create Parser factory

if opts.has_key("--validate"):
    pf=saxexts.ParserFactory([
        "xmlproc_val"])

else:
    pf=saxexts.ParserFactory([
        "xml.sax.drivers.drv_xmlproc",
        "xml.sax.drivers.drv_pyexpat",
        "xml.sax.drivers.drv_sgmlop", 
        "xml.sax.drivers.drv_xmllib", 
        "xml.sax.drivers.drv_xmltok",
        "xml.sax.drivers.drv_xmltoolkit",
        "xml.sax.drivers.drv_xmldc"])

# Create parser
parser = pf.make_parser()

# Create architectures handler and reqister it with the parser
arch_handler = xmlarch.ArchDocHandler()

parser.setDocumentHandler(arch_handler)
#parser.setErrorHandler(saxutils.ErrorPrinter())
# parser.setLocale("no")

# Set the debug flag
if opts.has_key("--debug"): arch_handler.set_debug_level(1, sys.stderr)

# Register architecture document handlers
arch_handler.add_document_handler(args[0], xmlarch.Prettifier(sys.stdout))

if opts.has_key("--debug"):
    print "Parsing with:", parser.get_parser_name(), parser.get_parser_version()
    print "Starting architectual parsing..."

# Parse an architectural document
try:
    parser.parse(args[1])
except xmlarch.ArchException, e:
    sys.stderr.write("ArchException: " + str(e) + "\n")

if opts.has_key("--debug"): print "Finished architectual parsing..."



