"""
A SAX 2.0 driver for htmllib.

$Id: drv_htmllib.py,v 1.1 2001/07/26 08:03:44 larsga Exp $
"""

import types, string

from xml.sax import SAXNotSupportedException, SAXNotRecognizedException
from xml.sax.xmlreader import IncrementalParser
from drv_sgmllib import SgmllibDriver

class HtmllibDriver(SgmllibDriver):

    from htmlentitydefs import entitydefs
        
# ---
        
def create_parser():
    return HtmllibDriver()
