#!/usr/bin/env python

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
    "xmlproc",
    "xmlproc_val",
    "pyexpat",
    "sgmlop", 
    "xmllib", 
    "xmltok",
    "xmltoolkit",
    "xmldc"])

parser = pf.make_parser()

# Create architectures handler
arch_handler = xmlarch.ArchDocHandler()
arch_handler.set_debug(0)

# Register architecture processor handler with parser
parser.setErrorHandler(saxutils.ErrorPrinter())
parser.setDocumentHandler(arch_handler)

# Register architecture document handlers
#arch_handler.add_document_handler("html", xmlarch.Prettifier(open("htmlesi.out", "w")))

arch_handler.add_document_handler(sys.argv[1], xmlarch.Prettifier(sys.stdout))
#arch_handler.add_document_handler(sys.argv[1], xmlarch.Prettifier(open("htmlesi.out", "w")))

# Parse an architectural document
#parser.parseFile(sys.stdin)
parser.parse(sys.argv[2])

