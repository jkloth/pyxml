"""
A module of experimental extensions to the standard SAX interface.

$Id: saxexts.py,v 1.8 2000/09/26 20:01:02 loewis Exp $
"""

import _exceptions,handler,sys,string,os

# --- Parser factory

class ParserFactory:
    """A general class to be used by applications for creating parsers on
    foreign systems where it is unknown which parsers exist."""

    def __init__(self,list=None):
        # Python 2 compatibility: let consider environment variables
        # and properties override list argument
        if os.environ.has_key("PY_SAX_PARSER"):
            list = string.split(os.environ["PY_SAX_PARSER"], ",")
        _key = "python.xml.sax.parser"
        if sys.platform[:4] == "java" \
           and sys.registry.containsKey(_key):
            list = string.split(sys.registry.getProperty(_key), ",")
        self.parsers=list

    def get_parser_list(self):
        "Returns the list of possible drivers."
        return self.parsers

    def set_parser_list(self,list):
        "Sets the driver list."
        self.parsers=list

    if sys.platform[ : 4] == "java":
        def _create_parser(self,parser_name):
            from org.python.core import imp
            drv_module = imp.importName(parser_name, 0, globals())
            return drv_module.create_parser()

    else:
        def _create_parser(self,parser_name):
            drv_module = __import__(parser_name,{},{},['create_parser'])
            return drv_module.create_parser()

    def make_parser(self, parser_list):
        """Returns a SAX driver for the first available parser of the parsers
        in the list. Note that the list is one of drivers, so it first tries
        the driver and if that exists imports it to see if the parser also
        exists. If no parsers are available a SAXException is thrown.

        Accepts the driver package name as an optional argument."""

        for parser_name in parser_list+self.parsers:
            try:
                return self._create_parser(parser_name)
            except ImportError,e:
                pass

        raise _exceptions.SAXException("No parsers found",None)  

# --- Experimental extension to Parser interface
import saxlib
class ExtendedParser(saxlib.Parser):
    "Experimental unofficial SAX level 2 extended parser interface."

    def get_parser_name(self):
        "Returns a single-word parser name."
        raise _exceptions.SAXException("Method not supported.",None)

    def get_parser_version(self):
        """Returns the version of the imported parser, which may not be the
        one the driver was implemented for."""
        raise _exceptions.SAXException("Method not supported.",None)

    def get_driver_version(self):
        "Returns the version number of the driver."
        raise _exceptions.SAXException("Method not supported.",None)        
    
    def is_validating(self):
        "True if the parser is validating, false otherwise."
        raise _exceptions.SAXException("Method not supported.",None)

    def is_dtd_reading(self):
        """True if the parser is non-validating, but conforms to the spec by
        reading the DTD."""
        raise _exceptions.SAXException("Method not supported.",None)

    def reset(self):
        "Makes the parser start parsing afresh."
        raise _exceptions.SAXException("Method not supported.",None)
    
    def feed(self,data):
        "Feeds data to the parser."
        raise _exceptions.SAXException("Method not supported.",None)

    def close(self):
        "Called after the last call to feed, when there are no more data."
        raise _exceptions.SAXException("Method not supported.",None)
        
# --- Experimental document handler which does not slice strings

class NosliceDocumentHandler(saxlib.DocumentHandler):
    """A document handler that does not force the client application to
    slice character data strings."""

    def __init__(self):
        handler.DocumentHandler.__init__()
        self.characters=self.safe_handler

    def safe_handler(self,data,start,length):
        """A characters event handler that always works, but doesn't always
        slice strings."""
        if start==0 and length==len(data):
            self.handle_data(data)
        else:
            self.handle_data(data[start:start+length])

    def slice_handler(self,data,start,length):
        "A character event handler that always slices strings."
        self.handle_data(data[start:start+length])

    def noslice_handler(self,data,start,length):
        "A character event handler that never slices strings."
        self.handle_data(data)
        
    def handle_data(self,data):
        "This is the character data event method to override."
        pass

# --- Creating parser factories

XMLParserFactory=ParserFactory(["xml.sax.drivers.drv_pyexpat",
                                "xml.sax.drivers.drv_xmltok",
                                "xml.sax.drivers.drv_xmlproc",
                                "xml.sax.drivers.drv_xmltoolkit",
                                "xml.sax.drivers.drv_xmllib",
                                "xml.sax.drivers.drv_xmldc",
                                "xml.sax.drivers.drv_sgmlop"])

XMLValParserFactory=ParserFactory(["xml.sax.drivers.drv_xmlproc_val"])

HTMLParserFactory=ParserFactory(["xml.sax.drivers.drv_htmllib",
                                 "xml.sax.drivers.drv_sgmlop",
                                 "xml.sax.drivers.drv_sgmllib"])

SGMLParserFactory=ParserFactory(["xml.sax.drivers.drv_sgmlop",
                                 "xml.sax.drivers.drv_sgmllib"])

def make_parser(parser_list = []):
    return XMLParserFactory.make_parser(parser_list)
