########################################################################
#
# File Name:            Document.py
#
# Documentation:        http://docs.4suite.com/4DOM/Document.py.html
#
# History:
# $Log: Document.py,v $
# Revision 1.3  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.75  2000/09/22 02:47:23  uogbuji
# Fixes before 0.9.0.1
#
# Revision 1.74  2000/09/22 01:55:46  uogbuji
# Namespace bugs fixed
#
# Revision 1.73  2000/09/19 23:20:08  uogbuji
# Pre-packaging bug-fixes
#
# Revision 1.72  2000/09/19 20:24:00  uogbuji
# Buncha DOM fixes: namespaces, printing, etc.
# Add Alex F's problem reports to Dom/test_suite/problems
#
# Revision 1.71  2000/09/13 07:10:18  molson
# More packaging
#
# Revision 1.70  2000/09/10 22:56:46  uogbuji
# Minor fixes
#
# Revision 1.69  2000/09/09 00:43:19  uogbuji
# Fix illegal character checks
# Printer fixes
#
# Revision 1.68  2000/09/07 15:11:34  molson
# Modified to abstract import
#
# Revision 1.67  2000/08/17 06:31:08  uogbuji
# Update SplitQName to simplify usage
# Fix namespace declaration namespaces acc to May DOM CR
#
# Revision 1.66  2000/08/07 05:16:29  molson
# HHHunted down memory leakes
#
# Revision 1.65  2000/07/26 18:37:21  molson
# Tested speed and made some improvements
#
# Revision 1.64  2000/07/25 18:25:09  jkloth
# Fixed cloning bugs
#
# Revision 1.63  2000/07/18 16:58:52  jkloth
# Fixed small bugs
#
# Revision 1.62  2000/07/09 19:02:20  uogbuji
# Begin implementing Events
# bug-fixes
#
# Revision 1.61  2000/07/03 02:12:52  jkloth
#
# fixed up/improved cloneNode
# changed Document to handle DTS as children
# fixed miscellaneous bugs
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

import re, string, copy


import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node
Text = implementation._4dom_fileImport('Text')
SplitQName = implementation._4dom_fileImport('ext').SplitQName

DOMException = dom.DOMException
HIERARCHY_REQUEST_ERR = dom.HIERARCHY_REQUEST_ERR
INVALID_CHARACTER_ERR = dom.INVALID_CHARACTER_ERR
NOT_SUPPORTED_ERR = dom.NOT_SUPPORTED_ERR
XMLNS_NAMESPACE = dom.XMLNS_NAMESPACE
XML_NAMESPACE = dom.XML_NAMESPACE
NAMESPACE_ERR = dom.NAMESPACE_ERR

#FIXME: should allow combining characters: fix when Python gets Unicode
g_namePattern = re.compile('[a-zA-Z_:][\w\.\-_:]*\Z')

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
        Node.__init__(self,None,'','','')
        self.__dict__['__doctype'] = None
        self.__dict__['__implementation'] = implementation
        self.__dict__['__documentElement'] = None
        self.__dict__['_4dom_isNsAware'] = 1
        self.__dict__['_singleChildren'] = {Node.ELEMENT_NODE:'__documentElement',
                                            Node.DOCUMENT_TYPE_NODE:'__doctype'
                                            }
        self._4dom_setDocumentType(doctype)
#        if doctype:
#            doctype._4dom_setOwnerDocument(self)
#            Node.appendChild(self, doctype)

    ### Attribute Methods ###

    def _get_doctype(self):
        return self.__dict__['__doctype']

    def _get_implementation(self):
        return self.__dict__['__implementation']

    def _get_documentElement(self):
        return self.__dict__['__documentElement']

    def _get_ownerDocument(self):
        return self

    ### Methods ###

    def createElement(self, tagname):
        Element = implementation._4dom_fileImport('Element').Element
        if self.isHtml(): tagname = string.upper(tagname)
        if not g_namePattern.match(tagname):
            raise DOMException(INVALID_CHARACTER_ERR)
        e = Element(self,tagname,'','',tagname)
        #trace("Create Element")
        return e

    def createDocumentFragment(self):
        DocumentFragment = implementation._4dom_fileImport('DocumentFragment').DocumentFragment
        newDocFrag = DocumentFragment(self)
        return newDocFrag

    def createTextNode(self, data):
        tn = Text.Text(self,data)
        #trace("Create Text Node")
        return tn

    def createComment(self, data):
        Comment = implementation._4dom_fileImport('Comment').Comment
        c = Comment(self,data)
        #trace("Create comment")
        return c

    def createCDATASection(self, data):
        CDATASection = implementation._4dom_fileImport('CDATASection').CDATASection
        if not self.isXml():
            raise DOMException(NOT_SUPPORTED_ERR)
        c = CDATASection(self,data)
        return c

    def createProcessingInstruction(self, target, data):
        ProcessingInstruction = implementation._4dom_fileImport('ProcessingInstruction').ProcessingInstruction
        if not self.isXml():
            raise DOMException(NOT_SUPPORTED_ERR)
        #FIXME: Technically, chacters from the unicode surrogate blocks are illegal.  Fix when Python gets unicode
        #for c in target:
        #    if c in unicode_surrogate_blocks:
        #        trace('Create Processing Instruction Failed, Invalid character')
        #        raise DOMException(INVALID_CHARACTER_ERR);
        if not g_namePattern.match(target):
            raise DOMException(INVALID_CHARACTER_ERR)


        newPI = ProcessingInstruction(self, target, data);
        return newPI
    
    def createAttribute(self, name):
        Attr = implementation._4dom_fileImport('Attr').Attr
        if not g_namePattern.match(name):
            raise DOMException(INVALID_CHARACTER_ERR)
        a = Attr(self,name, '', '', '')
        return a

    def createEntityReference(self, name):
        EntityReference = implementation._4dom_fileImport('EntityReference').EntityReference
        if not self.isXml():
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        if not g_namePattern.match(name):
            raise DOMException(INVALID_CHARACTER_ERR)
        e = EntityReference(self, name)
        return e

    def _4dom_createEntity(self, publicId, systemId, notationName):
        Entity = implementation._4dom_fileImport('Entity').Entity
        if not self.isXml():
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        e = Entity(self, publicId, systemId, notationName)
        return e

    def _4dom_createNotation(self, publicId, systemId, name):
        Notation = implementation._4dom_fileImport('Notation').Notation
        if not self.isXml():
            raise dom.DOMException(NOT_SUPPORTED_ERR)
        n = Notation(self, publicId, systemId, name)
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

    def importNode(self, importedNode, deep):
        importType = importedNode.nodeType

        # No import allow per spec
        if importType in [Node.DOCUMENT_NODE, Node.DOCUMENT_TYPE_NODE]:
            raise DOMException(NOT_SUPPORTED_ERR)

        # Only the EntRef itself is copied since the source and destination
        # documents might have defined the entity differently
        #FIXME: If the document being imported into provides a definition for
        #       this entity name, its value is assigned.
        #       Need entity support for this!!
        elif importType == Node.ENTITY_REFERENCE_NODE:
            deep = 0

        return importedNode.cloneNode(deep, newOwner=self)

    def createElementNS(self, namespaceURI, qualifiedName):
        Element = implementation._4dom_fileImport('Element').Element
        (prefix, localName) = SplitQName(qualifiedName)
        if not g_namePattern.match(qualifiedName):
            raise DOMException(INVALID_CHARACTER_ERR)
        if prefix == 'xml':
            if namespaceURI and namespaceURI != XML_NAMESPACE:
                raise DOMException(NAMESPACE_ERR)
        if (not namespaceURI and prefix):
            raise DOMException(NAMESPACE_ERR)
        e = Element(self, qualifiedName, namespaceURI, prefix, localName)
        return e

    def createAttributeNS(self, namespaceURI, qualifiedName):
        if not g_namePattern.match(qualifiedName):
            raise DOMException(INVALID_CHARACTER_ERR)
        Attr = implementation._4dom_fileImport('Attr').Attr
        (prefix, localName) = SplitQName(qualifiedName)
        if prefix == 'xml':
            if namespaceURI and namespaceURI != XML_NAMESPACE:
                raise DOMException(NAMESPACE_ERR)
        if localName == 'xmlns':
            if namespaceURI != XMLNS_NAMESPACE:
                raise DOMException(NAMESPACE_ERR)
            a = Attr(self, qualifiedName, XMLNS_NAMESPACE, 'xmlns', prefix)
        else:
            if (not namespaceURI and prefix) or (not prefix and namespaceURI):
                raise DOMException(NAMESPACE_ERR)
            a = Attr(self, qualifiedName, namespaceURI, prefix, localName)
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

    ### Document Traversal Factory Functions ###

    def createNodeIterator(self, root, whatToShow, filter, entityReferenceExpansion):
        NodeIterator = implementation._4dom_fileImport('NodeIterator')
        nodi = NodeIterator.NodeIterator(root, whatToShow, filter, entityReferenceExpansion)
        return nodi

    def createTreeWalker(self, root, whatToShow, filter, entityReferenceExpansion):
        TreeWalker = implementation._4dom_fileImport('TreeWalker')
        tw = TreeWalker.TreeWalker(root, whatToShow, filter, entityReferenceExpansion)
        return tw

    ### Overridden Methods ###

    def _4dom_setDocumentType(self, doctype):
        if not self.__dict__['__doctype'] and doctype is not None:
            self.__dict__['__doctype'] = doctype
            doctype._4dom_setOwnerDocument(self)
            return Node.appendChild(self, doctype)
        pass

    def _4dom_addSingle(self, node):
        '''Make sure only one Element node is added to a Document'''
        if node.nodeType == Node.ELEMENT_NODE:
            if self.__dict__['__documentElement']:
                raise DOMException(HIERARCHY_REQUEST_ERR)
            self.__dict__['__documentElement'] = node

    def appendChild(self, newChild):
        self._4dom_addSingle(newChild)
        return Node.appendChild(self, newChild)

    def insertBefore(self, newChild, oldChild):
        self._4dom_addSingle(newChild)
        return Node.insertBefore(self, newChild, oldChild)

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == Node.ELEMENT_NODE \
        and oldChild.nodeType != Node.ELEMENT_NODE \
        and self.__dict__['__documentElement']:
            raise DOMException(HIERARCHY_REQUEST_ERR)
        replaced = Node.replaceChild(self, newChild, oldChild)
        if self.documentElement == replaced:
            if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
                newChild = newChild.firstChild
            self.__dict__['__documentElement'] = newChild
        return replaced

    def removeChild(self,oldChild):
        node = Node.removeChild(self, oldChild)
        if self.documentElement == node:
            self.__dict__['__documentElement'] = None
        if self.__dict__['__doctype'] == node:
            self.__dict__['__doctype'] = None
        return node

    #DocumentEvent interface
    import Event
    def createEvent(eventType):
        if eventType in Event.supportedEvents:
            #Only mutation events are supported
            return Event.MutationEvent(eventType)
        else:
            raise DOMException(NOT_SUPPORTED_ERR)

    def __repr__(self):
        return "<%s Document at %s>" % (
            (self.isXml() and 'XML' or 'HTML'),
            id(self)
            )

    def cloneNode(self, deep):
        clone = Document(None)
        if deep:
            if self.doctype is not None:
                # Cannot have any children, no deep needed
                dt = self.doctype.cloneNode(0)
                clone._4dom_setDocumentType(dt)
            if self.documentElement is not None:
                # The root element can have children, duh
                root = self.documentElement.cloneNode(1, newOwner=clone)
                clone.appendChild(root)
        return clone

    ### Helper Functions for Pickling ###

    def __getinitargs__(self):
        return (None,)

    def __getstate__(self):
        return {}

    ### Convenience Functions ###

    def isXml(self):
        return 1

    def isHtml(self):
        return 0

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'doctype':_get_doctype,
                               'implementation':_get_implementation,
                               'documentElement':_get_documentElement,
                               'ownerDocument':_get_ownerDocument,
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
