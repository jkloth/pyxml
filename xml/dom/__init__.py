########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4DOM/__init__.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

#ExceptionCode
INDEX_SIZE_ERR                 = 1
DOMSTRING_SIZE_ERR             = 2
HIERARCHY_REQUEST_ERR          = 3
WRONG_DOCUMENT_ERR             = 4
INVALID_CHARACTER_ERR          = 5
NO_DATA_ALLOWED_ERR            = 6
NO_MODIFICATION_ALLOWED_ERR    = 7
NOT_FOUND_ERR                  = 8
NOT_SUPPORTED_ERR              = 9
INUSE_ATTRIBUTE_ERR            = 10
INVALID_STATE_ERR              = 11
SYNTAX_ERR                     = 12
INVALID_MODIFICATION_ERR       = 13
NAMESPACE_ERR                  = 14
INVALID_ACCESS_ERR             = 15

class DOMException(Exception):
    def __init__(self, *args):
	if len(args) >= 1:
	    self.code = args[0]
        self.args = args
        Exception.__init__(self, g_errorMessages[self.code] % args)

from xml.dom import DOMImplementation

try:
    from xml.dom.html import HTMLDOMImplementation
    implementation =  HTMLDOMImplementation.HTMLDOMImplementation()
    HTMLDOMImplementation.implementation = implementation
except ImportError:
    implementation = DOMImplementation.DOMImplementation()
DOMImplementation.implementation = implementation

XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
XMLNS_NAMESPACE = "http://www.w3.org/2000/xmlns/"

locale = 'en_US'
locale_module = __import__('xml.dom.'+locale, globals(), locals(), ['g_errorMessages'])
g_errorMessages = locale_module.__dict__['g_errorMessages']

