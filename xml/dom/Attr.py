########################################################################
#
# File Name:            Attr.py
#
# Documentation:        http://docs.4suite.com/4DOM/Attr.py.html
#
# History:
# $Log: Attr.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.31  2000/06/09 01:37:23  jkloth
# Updated copyright
# Fixed return value for nodeValue
#
# Revision 1.30  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.29  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.28  2000/01/26 05:53:31  uche
# Fix AVTs
# Implement optimization by delaying and not repeating parser invocation
# Completed error-message framework
# NaN --> None, hopefully temporarily
#
# Revision 1.27  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.26  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.25  1999/11/18 08:08:09  molson
# Added namespaces
#
# Revision 1.24  1999/11/18 07:36:17  molson
# Removed Factories
# Updated to new python/DOM interface binding
#
# Revision 1.23  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.22  1999/11/18 06:38:36  uche
# Changes to new Python/Dom Binding
#
# Revision 1.21  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.20  1999/09/14 03:42:43  uche
# XXX -> FIXME
# Fix retrieval of attr values
#
# Revision 1.19  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.18  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.17  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.16  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
DOM Level 2 Attribute Node
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import xml.dom
from xml.dom.Node import Node

class Attr(Node):
    nodeType = Node.ATTRIBUTE_NODE
    _allowedChildren = [Node.TEXT_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, name, namespaceURI, prefix, localName):
        Node.__init__(self, ownerDocument, namespaceURI, prefix, localName)
        self.__dict__['__nodeName'] = name
        self.__dict__['__ownerElement'] = None

    ### Attribute Methods ###

    def _get_name(self):
        return self.__dict__['__nodeName']

    def _get_specified(self):
        #True if this attribute was explicitly given a value in the document
        return self._get_value() != ''

    def _get_value(self):
        str = ''
        for child in self.childNodes:
            str = str + child.nodeValue
        return str

    def _set_value(self, value):
        if value is not None:
            nl = [self.ownerDocument.createTextNode(value)]
        else:
            nl = []
        self.__dict__['__childNodes'] = xml.dom.implementation._4dom_createNodeList(nl)

    def _get_ownerElement(self):
        return self.__dict__['__ownerElement']

    ### Overridden Methods ###

    def _get_nodeValue(self):
        return self._get_value()

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createAttribute(self.name)
            else:
                node = newOwner.createAttribute(self.name)
        #Clone from our ancestors
        Node.cloneNode(self, deep, node)
        return node

    def __repr__(self):
         return '<Attribute Node at %s: Name = "%s", Value = "%s">' % (
             id(self),
             self.name,
             self.value
             )

    ### Internal Methods ###

    def _4dom_setOwnerElement(self, owner):
        self.__dict__['__ownerElement'] = owner

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({
        'name':_get_name,
        'specified':_get_specified,
        'ownerElement':_get_ownerElement,
        'value':_get_value,
        'nodeValue':_get_value
        })

    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        'value':_set_value,
        'nodeValue':_set_value
        })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
