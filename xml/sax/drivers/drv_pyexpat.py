"""
SAX driver for the Pyexpat C module.
"""

# Note: this driver is 100% experimental and has never been tested at all.
# The following things are missing because I couldn't figure out how to do
# them:
#  - location handling
#
# Event handling can be speeded up by bypassing the driver for some events.
# This will be implemented later when I can test this driver.
#
# This driver has been much improved by Geir Ove Grønmo, who writes:
#
#   "This version of the driver should work, but there are things that
#    need fixing. I have to create a new parser object every time parse_file
#    is called! This is necessary because pyexpat is not reset after parsing."

version="0.10"

from xml.sax import saxlib,saxutils
from xml.parsers import pyexpat
import urllib

# --- SAX_expat

class SAX_expat(saxlib.Parser,saxlib.Locator):
    "SAX driver for the Pyexpat C module."

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.parser=pyexpat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.characters
        self.parser.ProcessingInstructionHandler = self.processingInstruction

    def startElement(self,name,attrs):
        at = {}
        for i in range(0, len(attrs), 2):
            at[attrs[i]] = attrs[i+1]
            
        self.doc_handler.startElement(name,saxutils.AttributeMap(at))

    def endElement(self,name):
        self.doc_handler.endElement(name)

    def characters(self,data):
        self.doc_handler.characters(data,0,len(data))

    def processingInstruction(self,target,data):
        self.doc_handler.processingInstruction(target,data)

    def parse(self,sysID):
        self.sysID=sysID
        self.parseFile(urllib.urlopen(sysID))
        
    def parseFile(self,fileobj):
        self.reset()
        self.doc_handler.startDocument()

#        while 1:
#            buf=fileobj.read(16384)
#
#            if buf:
#               if not self.parser.Parse(buf):
#                    self.__report_error()
#                    return
#           else:
#               break

        if not self.parser.Parse(fileobj.read(),1):
            self.__report_error()
                            
        self.doc_handler.endDocument()

    # --- Locator methods. Only usable after errors.

    def getLineNumber(self):
        return self.parser.ErrorLineNumber

    def getColumnNumber(self):
        return self.parser.ErrorColumnNumber    

    # --- Internal

    def __report_error(self):
        msg=pyexpat.ErrorString(self.parser.ErrorCode)
        self.err_handler.fatalError(saxlib.SAXParseException(msg,None,self))

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS
        
    def get_parser_name(self):
        return "pyexpat"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version
    
    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.parser=pyexpat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.characters
        self.parser.ProcessingInstructionHandler = self.processingInstruction
    
    def feed(self,data):
        if not self.parser.Parse(data):
            self.__report_error()

    def close(self):
        if not self.parser.Parse("",1):
            self.__report_error()
        self.parser = None
        
# ---
        
def create_parser():
    return SAX_expat()
