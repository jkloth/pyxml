#!/usr/bin/env python

# Import needed modules
from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys
        
# ============================================================================
# SAX document handler that produces normalized XML output
# ============================================================================

class ElementComparer(saxlib.HandlerBase):

    """A SAX document handler that compares architectural events and client document events."""

    def __init__(self, event_tracker, writer=sys.stdout):

        "Initialize a new instance."

	self.writer = writer
        self.event_tracker = event_tracker
        
    def startElement(self, name, amap):

	"Handle an event for the beginning of an element."

        print "<%s> was derived from the <%s> element." % (self.event_tracker.get_event("startElement")[0], name)
        
# ============================================================================
# Main program
# ============================================================================

# Create architecture processor handler
arch_handler = xmlarch.ArchDocHandler()

# Create parser and register architecture processor with it
parser = saxexts.XMLParserFactory.make_parser()
parser.setDocumentHandler(arch_handler)

# Register a default document handler that tracks all events
event_tracker = xmlarch.EventTracker()
arch_handler.set_default_document_handler(event_tracker)

# Add an document handler to process the html architecture
comparer_handler = ElementComparer(event_tracker)
arch_handler.add_document_handler(sys.argv[1], comparer_handler)

# Parse (and process) the document
parser.parse(sys.argv[2])
