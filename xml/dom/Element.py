########################################################################
#
# File Name:            Element.py
#
# Documentation:        http://docs.4suite.com/4DOM/Element.py.html
#
# History:
# $Log: Element.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.53  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.52  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.51  2000/05/04 00:03:26  jkloth
# bug fixes
#
# Revision 1.50  2000/04/27 18:43:36  jkloth
# changed imports
#
# Revision 1.49  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.48  2000/03/15 21:34:25  uche
# Last-minute packaging fixes
# Major fixes to SortDocOrder: ahndle document() function and attr wrappers
# Other fixes
#
# Revision 1.47  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.46  2000/02/07 15:53:54  uche
# Minor fixes to __repr__s
#
# Revision 1.45  2000/02/06 00:46:57  uche
# Fixed xsl:import
# Fixed document()
# Added XPath/HTML test
#
# Revision 1.44  2000/01/26 05:53:31  uche
# Fix AVTs
# Implement optimization by delaying and not repeating parser invocation
# Completed error-message framework
# NaN --> None, hopefully temporarily
#
# Revision 1.43  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.42  1999/12/17 23:24:11  uche
# Began testing using xsl-list messages and fixed many bugs consequently.
#
# Revision 1.41  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.40  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
#
# Revision 1.39  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.38  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.37  1999/11/18 07:50:59  molson
# Added namespaces to Nodes
#
# Revision 1.36  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.35  1999/11/16 03:25:43  molson
# Finished testing node in the new format
#
# Revision 1.34  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.33  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.32  1999/10/19 16:27:59  molson
# Fixed bug in element normalize
#
# Revision 1.31  1999/10/18 18:52:04  molson
# Fixed typo in Normalize
#
# Revision 1.30  1999/09/14 03:42:43  uche
# XXX -> FIXME
# Fix retrieval of attr values
#
# Revision 1.29  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.28  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.27  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.26  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import xml.dom.ext
from xml.dom.Node import Node
from xml.dom import INVALID_CHARACTER_ERR
from xml.dom import WRONG_DOCUMENT_ERR
from xml.dom import INUSE_ATTRIBUTE_ERR
from xml.dom import NOT_FOUND_ERR
from xml.dom import implementation
from xml.dom import DOMException
import string


class Element(Node):
    nodeType = Node.ELEMENT_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.TEXT_NODE,
                        Node.COMMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, nodeName, namespaceURI, prefix, localName):
        Node.__init__(self, ownerDocument, namespaceURI, prefix, localName);
        #Set our attributes
        self.__dict__['__attributes'] = implementation._4dom_createNamedNodeMap(ownerDocument)
        self.__dict__['__nodeName'] = nodeName

    ### Attribute Methods ###

    def _get_tagName(self):
        return self.__dict__['__nodeName']

    ### Methods ###

    def getAttribute(self, name):
        att = self.getAttributeNode(name)
        if att == None:
            return ''
        return att.value

    def setAttribute(self, name, value):
        ownerDoc = self.ownerDocument
        #Blindly use it
        #Will raise the INVALID_CHARACTER_ERR if needed
        att = ownerDoc.createAttribute(name)
        att.value=value
        self.setAttributeNode(att)

    def removeAttribute(self, name):
        try:
            old = self.attributes.removeNamedItem(name)
        except DOMException, err:
            if err.code != NOT_FOUND_ERR:
                raise err
            return
        old._4dom_setParentNode(None)
        old._4dom_setOwnerElement(None)

    def getAttributeNode(self, name):
        return self.attributes.getNamedItem(name)

    def setAttributeNode(self, node):
        ourOwner = self.ownerDocument
        nodeOwner = node.ownerDocument
        if ourOwner != None and nodeOwner != None:
            if (ourOwner.isXml() != nodeOwner.isXml()) or (ourOwner.isHtml() != nodeOwner.isHtml()):
                raise DOMException(WRONG_DOCUMENT_ERR)
        if node.parentNode != None:
            raise DOMException(INUSE_ATTRIBUTE_ERR)
        node._4dom_setOwnerElement(self)
        rt = self.attributes.setNamedItem(node)
        if rt:
            return rt

    def removeAttributeNode(self, node):
        old = self.getAttributeNode(node.name)
        if old != None:
            self.removeAttribute(node.name)
        else:
            old = self.getAttributeNodeNS(node.namespaceURI, node.localName)
            if old != None:
                self.removeAttributeNS(node.namespaceURI, node.localName)
            else:
                raise DOMException(NOT_FOUND_ERR)
        return old

    def getElementsByTagName(self,tagName):
        if self.ownerDocument.isHtml():
            tagName = string.upper(tagName)
        py = implementation._4dom_createNodeList()
        for cur_node in self.childNodes:
            if cur_node.nodeType == Node.ELEMENT_NODE:
                if tagName == '*':
                    py.append(cur_node)
                elif cur_node.tagName == tagName:
                    py.append(cur_node)
                cl = cur_node.getElementsByTagName(tagName)
                py = py + cl
        return py

    def getAttributeNS(self, namespaceURI, localName):
        attr = self.getAttributeNodeNS(namespaceURI, localName)
        if attr:
            return attr.value
        return ''

    def setAttributeNS(self, namespaceURI, qualifiedName, value):
        self._4dom_validateName(qualifiedName)
        #FIXME: Check for NAMESPACE_ERR
        att = self.ownerDocument.createAttributeNS(namespaceURI, qualifiedName)
        if not namespaceURI:
            name_parts = xml.dom.ext.SplitQName(qualifiedName)
            if name_parts[0] == 'xml':
                namespaceURI = 'http://www.w3.org/XML/1998/namespace'
        att.value = value
        self.setAttributeNodeNS(att)

    def removeAttributeNS(self, namespaceURI, localName):
        old = self.attributes.removeNamedItemNS(namespaceURI,localName)
        if old != None:
            old._4dom_setParentNode(None)
            old._4dom_setOwnerElement(None)

    def getAttributeNodeNS(self, namespaceURI, localName):
        return self.attributes.getNamedItemNS(namespaceURI, localName)

    def setAttributeNodeNS(self, node):
        ourOwner = self.ownerDocument
        nodeOwner = node.ownerDocument
        if ourOwner != nodeOwner:
            raise DOMException(WRONG_DOCUMENT_ERR)
        if node.parentNode != None:
            raise DOMException(INUSE_ATTRIBUTE_ERR)
        node._4dom_setOwnerElement(self)
        rt = self.attributes.setNamedItemNS(node)
        return rt or None

    def getElementsByTagNameNS(self, namespaceURI, localName):
        if namespaceURI == None:
            return self.getElementsByTagName(localName)
        py = implementation._4dom_createNodeList()
        for curr_node in self.childNodes:
            if curr_node.nodeType == Node.ELEMENT_NODE:
                #It is an element
                if namespaceURI == '*' or curr_node.namespaceURI == namespaceURI:
                    if localName == '*' or curr_node.localName == localName:
                        py.append(curr_node)
                #Get its children that match
                cl = curr_node.getElementsByTagNameNS(namespaceURI,localName)
                py = py + cl
        return py

    def hasAttribute(self, name):
        return self.getAttributeNode(name) != None

    def hasAttributeNS(self, namespaceURI, localName):
        return self.getAttributeNodeNS(namespaceURI, localName) != None

    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement(self.tagName)
            else:
                node = newOwner.createElement(self.tagName)
        #Clone our ancestors
        Node.cloneNode(self,deep,node)
        #Now clone our map
        for attr in self.attributes:
            if self.ownerDocument._4dom_isNsAware:
                node.setAttributeNodeNS(attr.cloneNode(1, newOwner=newOwner))
            else:
                node.setAttributeNode(attr.cloneNode(1, newOwner=newOwner))
        return node

    def __repr__(self):
        return "<Element Node at %s: Name = '%s' with %d attributes and %d children>" % (id(self),self.nodeName,len(self.attributes), len(self.childNodes))

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'tagName':_get_tagName,
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
