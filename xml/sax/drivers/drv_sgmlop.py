"""
SAX driver for the sgmlop parser.

$Id: drv_sgmlop.py,v 1.6 2000/09/26 14:43:11 loewis Exp $
"""

version="0.11"

import sgmlop
from xml.sax import saxlib,saxutils
import urllib

# --- Driver

class Parser(saxlib.Parser):

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.parser = sgmlop.XMLParser()
    
    def setDocumentHandler(self, dh):
	self.parser.register(self) # older version wanted ,1 arg
        self.doc_handler=dh

    def parse(self, url):
        self.parseFile(urllib.urlopen(url))
        
    def parseFile(self, file):
	parser = self.parser

	while 1:
	    data = file.read(16384)
	    if not data:
		break
	    parser.feed(data)

	self.close()

    # --- SAX 1.0 METHODS

    def handle_cdata(self, data):
        self.doc_handler.characters(data,0,len(data))

    def handle_data(self, data):
        self.doc_handler.characters(data,0,len(data))
        
    def handle_proc(self, target, data):
        self.doc_handler.processingInstruction(target,data)

    def handle_charref(self, charno):
        if charno<256:
            self.doc_handler.characters(chr(charno),0,1)

    def finish_starttag(self, name, attrs):
        self.doc_handler.startElement(name,saxutils.AttributeMap(attrs))

    def finish_endtag(self,name):
        self.doc_handler.endElement(name)

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "sgmlop"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version
    
    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.parser=sgmlop.XMLParser()
    
    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()
        self.doc_handler.endDocument()
        
# ----

def create_parser():
    return Parser()
