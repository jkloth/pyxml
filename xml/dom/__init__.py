########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4DOM/__init__.py.html
#
"""
WWW: http://4suite.org/4DOM         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""


class Node:
    """Class giving the NodeType constants."""

    # DOM implementations may use this as a base class for their own
    # Node implementations.  If they don't, the constants defined here
    # should still be used as the canonical definitions as they match
    # the values given in the W3C recommendation.  Client code can
    # safely refer to these values in all tests of Node.nodeType
    # values.

    ELEMENT_NODE                = 1
    ATTRIBUTE_NODE              = 2
    TEXT_NODE                   = 3
    CDATA_SECTION_NODE          = 4
    ENTITY_REFERENCE_NODE       = 5
    ENTITY_NODE                 = 6
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE                = 8
    DOCUMENT_NODE               = 9
    DOCUMENT_TYPE_NODE          = 10
    DOCUMENT_FRAGMENT_NODE      = 11
    NOTATION_NODE               = 12


# DOMException codes
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

# EventException codes
UNSPECIFIED_EVENT_TYPE_ERR     = 0

# Fourthought specific codes
FT_EXCEPTION_BASE = 1000
XML_PARSE_ERR = FT_EXCEPTION_BASE + 1

#RangeException codes
BAD_BOUNDARYPOINTS_ERR = 1
INVALID_NODE_TYPE_ERR = 2


class DOMException(Exception):
    def __init__(self, code, msg=''):
        self.code = code
        self.msg = msg or DOMExceptionStrings[code]

    def __str__(self):
        return self.msg

class EventException(Exception):
    def __init__(self, code, msg=''):
        self.code = code
        self.msg = msg or EventExceptionStrings[code]
        return

    def __str__(self):
        return self.msg

class RangeException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg or RangeExceptionStrings[code]
        Exception.__init__(self, self.msg)

class FtException(Exception):
    def __init__(self, code, *args):
        self.code = code
        self.msg = FtExceptionStrings[code] % args
        return

    def __str__(self):
        return self.msg

class IndexSizeErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INDEX_SIZE_ERR, msg)

class DOMStringSizeErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, DOMSTRING_SIZE_ERR, msg)

class HierarchyRequestErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, HIERARCHY_REQUEST_ERR, msg)

class WrongDocumentErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, WRONG_DOCUMENT_ERR, msg)

class InvalidCharacterErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INVALID_CHARACTER_ERR, msg)

class NoDataAllowedErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, NO_DATA_ALLOWED_ERR, msg)

class NoModificationAllowedErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, NO_MODIFICATION_ALLOWED_ERR, msg)

class NotFoundErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, NOT_FOUND_ERR, msg)

class NotSupportedErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, NOT_SUPPORTED_ERR, msg)

class InuseAttributeErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INUSE_ATTRIBUTE_ERR, msg)

class InvalidStateErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INVALID_STATE_ERR, msg)

class SyntaxErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, SYNTAX_ERR, msg)

class InvalidModificationErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INVALID_MODIFICATION_ERR, msg)

class NamespaceErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, NAMESPACE_ERR, msg)

class InvalidAccessErr(DOMException):
    def __init__(self, msg=''):
        DOMException.__init__(self, INVALID_ACCESS_ERR, msg)

class UnspecifiedEventTypeErr(EventException):
    def __init__(self, msg=''):
        EventException.__init__(self, UNSPECIFIED_EVENT_TYPE_ERR, msg)

class XmlParseErr(FtException):
    def __init__(self, msg=''):
        FtException.__init__(self, XML_PARSE_ERR, msg)

#Specific Range Exceptions
class BadBoundaryPointsErr(RangeException):
    def __init__(self, msg=''):
        RangeException.__init__(self, BAD_BOUNDARYPOINTS_ERR, msg)

class InvalidNodeTypeErr(RangeException):
    def __init__(self, msg=''):
        RangeException.__init__(self, INVALID_NODE_TYPE_ERR, msg)

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
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

import MessageSource
DOMExceptionStrings = MessageSource.__dict__['DOMExceptionStrings']
EventExceptionStrings = MessageSource.__dict__['EventExceptionStrings']
FtExceptionStrings = MessageSource.__dict__['FtExceptionStrings']
RangeExceptionStrings = MessageSource.__dict__['RangeExceptionStrings']

