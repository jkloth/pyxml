########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4DOM/__init__.py.html
#
# History:
# $Log: __init__.py,v $
# Revision 1.5  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.19  2000/09/14 06:42:25  jkloth
# Fixed circular import errors
#
# Revision 1.18  2000/09/07 15:11:34  molson
# Modified to abstract import
#
# Revision 1.17  2000/08/29 19:29:06  molson
# Fixed initial parameters
#
# Revision 1.16  2000/08/17 06:31:08  uogbuji
# Update SplitQName to simplify usage
# Fix namespace declaration namespaces acc to May DOM CR
#
# Revision 1.15  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.14  2000/05/04 01:12:05  pweinstein
# xml.dom.Html changes to xml.dom.html
#
# Revision 1.13  2000/05/04 01:05:22  pweinstein
# typo fix
#
# Revision 1.12  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.11  1999/12/15 17:32:10  uche
# Many bug-fixes.
#
# Revision 1.10  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.9  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.8  1999/11/16 03:25:43  molson
# Finished testing node in the new format
#
# Revision 1.7  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.6  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
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
    def __init__(self, code):
        self.code = code

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

