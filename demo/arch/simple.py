#!/usr/bin/python

# Import needed modules
from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys

# Create architecture processor handler
arch_handler = xmlarch.ArchDocHandler()

# Create parser and register architecture processor with it
parser = saxexts.XMLParserFactory.make_parser()
parser.setDocumentHandler(arch_handler)

# Add an document handler to process the html architecture
arch_handler.add_document_handler("html", xmlarch.Prettifier(sys.stdout))

# Parse (and process) the document
parser.parse("simple.xml")
