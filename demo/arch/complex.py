#!/usr/bin/python

# Import needed modules
from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys

# create architecture processor handler
arch_handler = xmlarch.ArchDocHandler()

# Create parser and register architecture processor with it
parser = saxexts.XMLParserFactory.make_parser()
parser.setDocumentHandler(arch_handler)

# Add an document handlers to process the html and biblio architectures
arch_handler.addArchDocumentHandler("html", xmlarch.Normalizer(open("html.out", "w")))
arch_handler.addArchDocumentHandler("biblio", saxutils.ESISDocHandler(open("biblio1.out", "w")))
arch_handler.addArchDocumentHandler("biblio", saxutils.Canonizer(open("biblio2.out", "w")))

# Register a default document handler that just passes through any incoming events
arch_handler.setDefaultDocumentHandler(xmlarch.Normalizer(sys.stdout))

# Parse (and process) the document
parser.parse("complex.xml")
