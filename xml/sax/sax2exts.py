"""
Various extensions to the core SAX 2.0 API.

$Id: sax2exts.py,v 1.2 2000/09/26 14:43:10 loewis Exp $
"""

import saxexts

# --- XMLReader factory

XMLReaderFactory = saxexts.ParserFactory

# --- Creating parser factories

XMLParserFactory = XMLReaderFactory(["xml.sax.drivers2.drv_pyexpat",
                                     "xml.sax.drivers2.drv_xmlproc"])

XMLValParserFactory = XMLReaderFactory(["xml.sax.drivers2.drv_xmlproc"])

HTMLParserFactory = XMLReaderFactory([])

SGMLParserFactory = XMLReaderFactory([])

def make_parser(parser = None):
    return XMLParserFactory.make_parser(parser)
