########################################################################
#
# File Name:            Document.py
#
# Documentation:        http://docs.4suite.com/4DOM/Document.py.html
#
# History:
# $Log: Document.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.60  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.59  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.58  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.57  2000/02/10 06:22:27  molson
# Fixed bugs
#
# Revision 1.56  2000/01/26 05:53:31  uche
# Fix AVTs
# Implement optimization by delaying and not repeating parser invocation
# Completed error-message framework
# NaN --> None, hopefully temporarily
#
# Revision 1.55  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.54  1999/12/18 22:54:51  uche
# Fix Namespaces to Match DOM Level 2 spec.
# Bug-fixes.
#
# Revision 1.53  1999/12/17 23:24:11  uche
# Began testing using xsl-list messages and fixed many bugs consequently.
#
# Revision 1.52  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.51  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.50  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.49  1999/11/19 02:13:23  uche
# Python/DOM binding update.
#
# Revision 1.48  1999/11/19 01:51:28  molson
# Added Filter support
#
# Revision 1.47  1999/11/19 01:16:57  molson
# Tested DOM level 2
#
# Revision 1.46  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.45  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.44  1999/11/18 08:08:09  molson
# Added namespaces
#
# Revision 1.43  1999/11/18 07:50:59  molson
# Added namespaces to Nodes
#
# Revision 1.42  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.41  1999/11/18 07:02:09  molson
# Removed Factories from node and node list and named node map
#
# Revision 1.40  1999/11/18 06:55:28  uche
# Python/DOM binding changes.
#
# Revision 1.39  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.38  1999/11/18 06:38:36  uche
# Changes to new Python/Dom Binding
#
# Revision 1.37  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
#
# Revision 1.36  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.35  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.34  1999/09/14 03:42:43  uche
# XXX -> FIXME
# Fix retrieval of attr values
#
# Revision 1.33  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.32  1999/09/09 08:04:52  uche
# NodeIterator.nextNode works and is tested.
#
# Revision 1.31  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.30  1999/09/08 23:54:07  uche
# Add machinery for updated DOM Level 2 Iterators and Filters (untested)
#
# Revision 1.29  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.28  1999/08/31 15:54:58  molson
# Abstracted node comparision to config_core.  Tested orbless and fnorb
#
# Revision 1.27  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import DOMException
from xml.dom import implementation

from xml.dom.Node import Node
import string,copy

from xml.dom import HIERARCHY_REQUEST_ERR
from xml.dom import INVALID_CHARACTER_ERR
from xml.dom import NOT_SUPPORTED_ERR
from xml import dom

class Document(Node):
    #Base node type for this class
    nodeType = Node.DOCUMENT_NODE
    nodeName = "#document"

    #This is for validation that the proper nodes are added
    _allowedChildren = [Node.PROCESSING_INSTRUCTION_NODE,
        Node.COMMENT_NODE,
        Node.ELEMENT_NODE,
        Node.DOCUMENT_TYPE_NODE
        ]


    def __init__(self, doctype):
        Node.__init__(self,self,'','','')
        self.__dict__['__doctype'] = None
        self.__dict__['__implementation'] = implementation
        self.__dict__['__documentElement'] = None
        self.__dict__['_4dom_isNsAware'] = 1
        self.__dict__['_singleChildren'] = {Node.ELEMENT_NODE:'__documentElement',
                                            Node.DOCUMENT_TYPE_NODE:'__doctype'
                                            }
        if doctype:
            doctype._4dom_setOwnerDocument(self)
            self.appendChild(doctype)


    ### Attribute Methods ###

    def _get_doctype(self):
        return self.__dict__['__doctype']

    def _get_implementation(self):
        return self.__dict__['__implementation']

    def _get_documentElement(self):
        return self.__dict__['__documentElement']

    ### Methods ###

    def createElement(self, tagname):
        from Element import Element
        if self.isHtml(): tagname = string.upper(tagname)
        self._4dom_validateName(tagname)
        e = Element(self,tagname,'','',tagname)
        #trace("Create Element")
        return e

    def createDocumentFragment(self):
        from xml.dom.DocumentFragment import DocumentFragment
        newDocFrag = DocumentFragment(self)
        return newDocFrag

    def createTextNode(self, data):
        from Text import Text
        tn = Text(self,data)
        #trace("Create Text Node")
        return tn

    def createComment(self, data):
        from Comment import Comment
        c = Comment(self,data)
        #trace("Create comment")
        return c

    def createCDATASection(self, data):
        from xml.dom.CDATASection import CDATASection
        if not self.isXml():
            pass
            raise DOMException(NOT_SUPPORTED_ERR)
        c = CDATASection(self,data)
        return c                

    def createProcessingInstruction(self, target, data):
        from xml.dom.ProcessingInstruction import ProcessingInstruction
        if not self.isXml():
            pass
            raise DOMException(NOT_SUPPORTED_ERR)
        #FIXME: Need to lookup the complete list of invalid chars
        for c in target:
            if c in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR);
        newPI = ProcessingInstruction(self,target,data);
        return newPI

    def createAttribute(self, name):
        #FIXME: Need to lookup the complete list of invalid chars
        from Attr import Attr
        for c in name:
            if c in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)
        a = Attr(self,name,'','','')
        pass
        return a

    def createEntityReference(self, name):
        from xml.dom.EntityReference import EntityReference
        if not self.isXml():
            pass
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        #FIXME: Complete the list of invalid chars
        for c in name:
            if c in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)
        e = EntityReference(self, name)
        pass
        return e

    def _4dom_createEntity(self, publicId, systemId, notationName):
        from xml.dom.Entity import Entity
        if not self.isXml():
            pass
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        e = Entity(self, publicId, systemId, notationName)
        pass
        return e

    def _4dom_createNotation(self, publicId, systemId, name):
        from xml.dom.Notation import Notation
        if not self.isXml():
            pass
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        n = Notation(self, publicId, systemId, name)
        pass
        return n

    def getElementsByTagName(self,tagName):
        root = self.documentElement
        if root == None:
            return implementation._4dom_createNodeList([])
        l = root.getElementsByTagName(tagName)
        if tagName == '*':
            l.insert(0,root)
        elif self.ownerDocument.isHtml() and string.upper(root.tagName) == string.upper(tagName):
            l.insert(0,root)
        elif root.tagName == tagName:
            l.insert(0,root)
        return l

    def getElementById(self, elementId):
        #FIXME: Must be implemented in the parser first
        return None

    def importNode(self,importedNode,deep):
        return importedNode.cloneNode(deep,newOwner = self)

    def createElementNS(self, namespaceURI, qualifiedName):
        from Element import Element
        fields = string.split(qualifiedName, ':')
        if len(fields) == 2:
            prefix = fields[0]
            localName = fields[1]
        elif len(fields) == 1:
            prefix = ''
            localName = fields[0]            
        #FIXME: I need to look up the full list of "not allowed" chars
        for c in localName:
            if c in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)
        e = Element(self, qualifiedName, namespaceURI, prefix, localName)
        pass
        return e

    def createAttributeNS(self, namespaceURI, qualifiedName):
        #FIXME: Need to lookup the complete list of invalid chars
        from Attr import Attr
        fields = string.split(qualifiedName,':')
        if len(fields) == 2:
            localName = fields[1]
            prefix = fields[0]
        elif len(fields) == 1:
            localName = fields[0]
            prefix = None
        for c in localName:
            if c in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)
        a = Attr(self, qualifiedName, namespaceURI, prefix, localName)
        pass
        return a

    def getElementsByTagNameNS(self,namespaceURI,localName):
        root = self.documentElement
        if root == None:
            return implementation.createNodeList([])
        py = root.getElementsByTagNameNS(namespaceURI,localName)
        if namespaceURI == '*' or namespaceURI == root.namespaceURI:
            if localName == '*' or localName == root.tagName:
                py.insert(0,root)
        return py

    #Document Traversal interface
    def createNodeIterator(self,root,whatToShow,filter,expand):
        from xml.dom import NodeIterator
        nodi = NodeIterator.NodeIterator(root, whatToShow, filter,expand)
        pass
        return nodi

    def createTreeWalker(self, root, whatToShow, filter, expand):
        from xml.dom import TreeWalker
        tw = TreeWalker.TreeWalker(root, whatToShow, filter, expand)
        pass
        return tw

    ### Overridden Methods ###

    def appendChild(self, newChild):
        '''Make sure only one of the singleChildren are added to a Document'''
        attr = self.__dict__['_singleChildren'].get(newChild.nodeType)
        if attr:
            if self.__dict__[attr] != None:
                pass
                raise DOMException(HIERARCHY_REQUEST_ERR)
            self.__dict__[attr] = newChild
        return Node.appendChild(self, newChild)

    def insertBefore(self, newChild, oldChild):
        '''Make sure only one of the singleChildren are added to a Document'''
        attr = self.__dict__['_singleChildren'].get(newChild.nodeType)
        if attr:
            if self.__dict__[attr] != None:
                pass
                raise DOMException(HIERARCHY_REQUEST_ERR)
            self.__dict__[attr] = newChild
        return Node.insertBefore(self, newChild, oldChild)

    def replaceChild(self, newChild, oldChild):
        '''Make sure only one of the singleChildren are added to a Document'''
        attr = self.__dict__['_singleChildren'].get(newChild.nodeType)
        if attr:
            if self.__dict__[attr] != None and self.__dict__[attr] != oldChild:
                pass
                raise DOMException(HIERARCHY_REQUEST_ERR)
            self.__dict__[attr] = newChild
        return Node.replaceChild(self, newChild, oldChild)

    def removeChild(self,oldChild):
        attr = self.__dict__['_singleChildren'].get(oldChild.nodeType)
        if attr:
            if self.__dict__[attr] == oldChild:
                self.__dict__[attr] = None
        return Node.removeChild(self, oldChild)

    def cloneNode(self,deep,node=None,newOwner=None):
        if node == None:
            #FIXME
            node = implementation.createDocument('','',self.doctype)
        node = Node.cloneNode(self,deep,node)
        return node

    def isXml(self):
        return 1

    def isHtml(self):
        return 0

    def __repr__(self):
        return "<%s Document at %s>" % (
            (self.isXml() and 'XML' or 'HTML'),
            id(self)
            )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'doctype':_get_doctype,
                               'implementation':_get_implementation,
                               'documentElement':_get_documentElement,
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
