########################################################################
#
# File Name:            NodeFilter.py
#
# Documentation:        http://docs.4suite.com/4DOM/NodeFilter.py.html
#
# History:
# $Log: NodeFilter.py,v $
# Revision 1.1  2000/06/06 01:36:05  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.9  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.8  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.7  1999/11/19 01:51:28  molson
# Added Filter support
#
# Revision 1.6  1999/11/19 01:32:41  uche
# Python/DOM binding changes.
#
# Revision 1.5  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.4  1999/09/09 08:04:52  uche
# NodeIterator.nextNode works and is tested.
#
# Revision 1.3  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


class NodeFilter:
    """
    This class is really just an abstract base.
    All implementation must be provided in a derived class
    """
    FILTER_ACCEPT = 1
    FILTER_REJECT = 2
    FILTER_SKIP   = 3

    SHOW_ALL                    = 0xFFFFFFFF
    SHOW_ELEMENT                = 0x00000001
    SHOW_ATTRIBUTE              = 0x00000002
    SHOW_TEXT                   = 0x00000004
    SHOW_CDATA_SECTION          = 0x00000008
    SHOW_ENTITY_REFERENCE       = 0x00000010
    SHOW_ENTITY                 = 0x00000020
    SHOW_PROCESSING_INSTRUCTION = 0x00000040
    SHOW_COMMENT                = 0x00000080
    SHOW_DOCUMENT               = 0x00000100
    SHOW_DOCUMENT_TYPE          = 0x00000200
    SHOW_DOCUMENT_FRAGMENT      = 0x00000400
    SHOW_NOTATION               = 0x00000800

    def acceptNode(self, node):
        raise TypeError("Please define and use a subclass.")

