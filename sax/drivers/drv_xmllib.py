"""
SAX driver for xmllib.py
"""

version="0.90"

from xml.sax import saxutils
from xml.sax.drivers import pylibs

import xmllib

# --- SAX_XLParser

class SAX_XLParser(pylibs.LibParser,xmllib.XMLParser):
    "SAX driver for xmllib.py."

    def __init__(self):
        xmllib.XMLParser.__init__(self)
        pylibs.LibParser.__init__(self)
        self.standalone=0
        self.reset()

    def unknown_starttag(self,tag,attributes):
        self.doc_handler.startElement(tag,saxutils.AttributeMap(attributes))
        
    def handle_endtag(self,tag,method):
        self.doc_handler.endElement(tag)

    def handle_proc(self,name,data):
        self.doc_handler.processingInstruction(name,data[1:])

    def getLineNumber(self):
        return self.lineno

    def getSystemId(self):
        return self.sysID

    def _can_locate(self):
        "Internal: returns true if location info is available."
        return 1

    # --- EXPERIMENTAL SAX PYTHON EXTENSIONS

    def get_parser_name(self):
        return "xmllib"

    def get_parser_version(self):
        return xmllib.version

    def get_driver_version(self):
        return version
    
    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        xmllib.XMLParser.reset(self)
        self.unfed_so_far=1 
    
    def feed(self,data):
        if self.unfed_so_far:
            self.doc_handler.startDocument()
            self.unfed_so_far=0
            
        xmllib.XMLParser.feed(self,data)
    
    def close(self):
        xmllib.XMLParser.close(self)
        self.doc_handler.endDocument()
    
# --- Global functions

def create_parser():
    return SAX_XLParser()
