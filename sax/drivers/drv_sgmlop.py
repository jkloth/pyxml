"""
SAX driver for the sgmlop parser.
"""

version="0.10"

from xml.parsers import _sgmlop
from xml.sax import saxlib,saxutils
import urllib

class DHWrapper:

    def __init__(self,real_dh):
        self.real_dh=real_dh

    def __getattr__(self,attr):
        return getattr(self.real_dh,attr)

    def startElement(self,name,attrs):
        self.real_dh.startElement(name,saxutils.AttributeMap(attrs))
        
class Parser(saxlib.Parser):

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.parser = _sgmlop.XMLParser()
    
    def setDocumentHandler(self, dh):
	self.parser.register(DHWrapper(dh), 1)
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
        self.parser=_sgmlop.XMLParser()
    
    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()
        self.doc_handler.endDocument()
        
# ----

def create_parser():
    return Parser()
