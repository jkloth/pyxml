#!/usr/bin/python

from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys

# =============================================================================
# Functions
# =============================================================================

def usage(message = ""):
    
    print "A simple utility for testing architectural from processing with xmlarch.py."
    print "Usage: minitest.py archname file.xml"
    print message
    sys.exit(1)

# =============================================================================
# MAIN PROGRAM
# =============================================================================

if len(sys.argv) < 3:
    usage()

# Create parser
pf=saxexts.ParserFactory([
    "xml.sax.drivers.drv_xmlproc",
    "xml.sax.drivers.drv_xmlproc_val",
    "xml.sax.drivers.drv_pyexpat",
    "xml.sax.drivers.drv_sgmlop", 
    "xml.sax.drivers.drv_xmllib", 
    "xml.sax.drivers.drv_xmltok",
    "xml.sax.drivers.drv_xmltoolkit",
    "drv_xmldc.py"])

parser = pf.make_parser()
#parser = xml.sax.drivers.drv_xmlproc_val.create_parser()
#print parser.get_parser_name()

# Create architectures handler
arch_handler = xmlarch.ArchDocHandler()
arch_handler.set_debug(0)

# Register architecture processor handler with parser
parser.setErrorHandler(saxutils.ErrorPrinter())
parser.setDocumentHandler(arch_handler)

# Register architecture document handlers
#arch_handler.addArchDocumentHandler("html", xmlarch.Normalizer(open("htmlesi.out", "w")))

arch_handler.addArchDocumentHandler(sys.argv[1], xmlarch.Normalizer(sys.stdout))
#arch_handler.addArchDocumentHandler(sys.argv[1], xmlarch.Normalizer(open("htmlesi.out", "w")))

# Parse an architectural document
#parser.parseFile(sys.stdin)
parser.parse(sys.argv[2])
