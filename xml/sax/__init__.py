"""Simple API for XML (SAX) implementation for Python.

This module provides an implementation of the SAX 2 interface;
information about the Java version of the interface can be found at
http://www.megginson.com/SAX/.  The Python version of the interface is
documented at <...>.

This package contains the following interface classes and functions:

ContentHandler, ErrorHandler - base classes for SAX2 handlers
SAXException, SAXNotRecognizedException,
SAXParseException, SAXNotSupportedException - SAX exceptions

make_parser            - creation of a new parser object
parse, parseString     - parse a document, using a provided handler

"""

from saxlib import ContentHandler, ErrorHandler
from saxlib import SAXException, SAXNotRecognizedException,\
                   SAXParseException, SAXNotSupportedException

from sax2exts import make_parser

def parse( filename_or_stream, handler, errorHandler=ErrorHandler() ):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(filename_or_stream)

def parseString( string, handler, errorHandler=ErrorHandler() ):
    try:
        import cStringIO
        StringIO=cStringIO
    except ImportError:
        import StringIO
        
    bufsize = len(string)
    buf = StringIO.StringIO(string)
 
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(buf)
