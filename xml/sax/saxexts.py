"""
A module of experimental extensions to the standard SAX interface.

$Id: saxexts.py,v 1.5 2000/09/16 06:18:37 loewis Exp $
"""

import saxlib,sys,string

try:
    import imp
except ImportError:
    pass  # imp does not exist in JPython, it seems.

# --- Internal utility methods

def rec_load_module(module):
    """Improvement over imp.find_module which loads submodules.
     It takes sys.modules into account, so renaming of xml to _xmlplus
     is honored."""
    path=""
    lastmod = None
    for mod in string.split(module,"."):
        if not lastmod:
            if sys.modules.has_key(mod):
                lastmod = sys.modules[mod]
                continue
        else:
            if hasattr(lastmod,mod):
                lastmod = getattr(lastmod,mod)
                continue
            else:
                try:
                    path=lastmod.__path__[0]
                except AttributeError,e:
                    pass
                
        if path=="":
            info=(mod,)+imp.find_module(mod)
        else:
            info=(mod,)+imp.find_module(mod,[path])
            
        lastmod=apply(imp.load_module,info)

    return lastmod

# --- Parser factory

class ParserFactory:
    """A general class to be used by applications for creating parsers on
    foreign systems where it is unknown which parsers exist."""

    def __init__(self,list=None):
        self.parsers=list

    def get_parser_list(self):
        "Returns the list of possible drivers."
        return self.parsers

    def set_parser_list(self,list):
        "Sets the driver list."
        self.parsers=list

    def make_parser(self, drv_name = None):
        """Returns a SAX driver for the first available parser of the parsers
        in the list. Note that the list is one of drivers, so it first tries
        the driver and if that exists imports it to see if the parser also
        exists. If no parsers are available a SAXException is thrown.

        Accepts the driver package name as an optional argument."""

        if drv_name==None:
            list=self.parsers
        else:
            list=[drv_name]
            
        for parser_name in list:
	    if sys.platform[:4] == "java": # JPython compatibility patch
	        try:
		    from org.python.core import imp
		    drv_module = imp.importName(parser_name, 0, globals())
	            return drv_module.create_parser()
                except ImportError,e:
                    pass
                except:
                    raise saxlib.SAXException("Problems during import, gave up"
                                              ,None)
	    else:
		import imp
	        try:
		    drv_module=rec_load_module(parser_name)
	            return drv_module.create_parser()
                except ImportError,e:
                    pass

        raise saxlib.SAXException("No parsers found",None)  

# --- Experimental extension to Parser interface

class ExtendedParser(saxlib.Parser):
    "Experimental unofficial SAX level 2 extended parser interface."

    def get_parser_name(self):
        "Returns a single-word parser name."
        raise saxlib.SAXException("Method not supported.",None)

    def get_parser_version(self):
        """Returns the version of the imported parser, which may not be the
        one the driver was implemented for."""
        raise saxlib.SAXException("Method not supported.",None)

    def get_driver_version(self):
        "Returns the version number of the driver."
        raise saxlib.SAXException("Method not supported.",None)        
    
    def is_validating(self):
        "True if the parser is validating, false otherwise."
        raise saxlib.SAXException("Method not supported.",None)

    def is_dtd_reading(self):
        """True if the parser is non-validating, but conforms to the spec by
        reading the DTD."""
        raise saxlib.SAXException("Method not supported.",None)

    def reset(self):
        "Makes the parser start parsing afresh."
        raise saxlib.SAXException("Method not supported.",None)
    
    def feed(self,data):
        "Feeds data to the parser."
        raise saxlib.SAXException("Method not supported.",None)

    def close(self):
        "Called after the last call to feed, when there are no more data."
        raise saxlib.SAXException("Method not supported.",None)
        
# --- Experimental document handler which does not slice strings

class NosliceDocumentHandler(saxlib.DocumentHandler):
    """A document handler that does not force the client application to
    slice character data strings."""

    def __init__(self):
        saxlib.DocumentHandler.__init__()
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

def make_parser(parser = None):
    return XMLParserFactory.make_parser(parser)
