########################################################################
#
# File Name:            Document.py
#
# Documentation:        http://docs.4suite.com/4DOM/Document.py.html
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

Node = implementation._4dom_fileImport('FtNode').Node
Text = implementation._4dom_fileImport('Text')
Event = implementation._4dom_fileImport('Event')
SplitQName = implementation._4dom_fileImport('ext').SplitQName

HierarchyRequestErr = dom.HierarchyRequestErr
InvalidCharacterErr = dom.InvalidCharacterErr
NotSupportedErr = dom.NotSupportedErr
XMLNS_NAMESPACE = dom.XMLNS_NAMESPACE
XML_NAMESPACE = dom.XML_NAMESPACE
NamespaceErr = dom.NamespaceErr

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
            raise InvalidCharacterErr()
        e = Element(self,tagname,'','',tagname)
        return e

    def createDocumentFragment(self):
        DocumentFragment = implementation._4dom_fileImport('DocumentFragment').DocumentFragment
        newDocFrag = DocumentFragment(self)
        return newDocFrag

    def createTextNode(self, data):
        tn = Text.Text(self,data)
        return tn

    def createComment(self, data):
        Comment = implementation._4dom_fileImport('Comment').Comment
        c = Comment(self,data)
        return c

    def createCDATASection(self, data):
        CDATASection = implementation._4dom_fileImport('CDATASection').CDATASection
        if not self.isXml():
            raise NotSupportedErr()
        c = CDATASection(self,data)
        return c

    def createProcessingInstruction(self, target, data):
        ProcessingInstruction = implementation._4dom_fileImport('ProcessingInstruction').ProcessingInstruction
        if not self.isXml():
            raise NotSupportedErr()
        #FIXME: Technically, chacters from the unicode surrogate blocks are illegal.  Fix when Python gets unicode
        #for c in target:
        #    if c in unicode_surrogate_blocks:
        #        raise InvalidCharacterErr()
        if not g_namePattern.match(target):
            raise InvalidCharacterErr()


        newPI = ProcessingInstruction(self, target, data);
        return newPI
    
    def createAttribute(self, name):
        Attr = implementation._4dom_fileImport('Attr').Attr
        if not g_namePattern.match(name):
            raise InvalidCharacterErr()
        a = Attr(self,name, '', '', '')
        return a

    def createEntityReference(self, name):
        EntityReference = implementation._4dom_fileImport('EntityReference').EntityReference
        if not self.isXml():
            raise NotSupportedErr()
        if not g_namePattern.match(name):
            raise InvalidCharacterErr()
        e = EntityReference(self, name)
        return e

    def _4dom_createEntity(self, publicId, systemId, notationName):
        Entity = implementation._4dom_fileImport('Entity').Entity
        if not self.isXml():
            raise NotSupportedErr()
        e = Entity(self, publicId, systemId, notationName)
        return e

    def _4dom_createNotation(self, publicId, systemId, name):
        Notation = implementation._4dom_fileImport('Notation').Notation
        if not self.isXml():
            raise NotSupportedErr()
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
            raise NotSupportedErr()

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
            raise InvalidCharacterErr()
        if prefix == 'xml':
            if namespaceURI and namespaceURI != XML_NAMESPACE:
                raise NamespaceErr()
        if (not namespaceURI and prefix):
            raise NamespaceErr()
        e = Element(self, qualifiedName, namespaceURI, prefix, localName)
        return e

    def createAttributeNS(self, namespaceURI, qualifiedName):
        if not g_namePattern.match(qualifiedName):
            raise InvalidCharacterErr()
        Attr = implementation._4dom_fileImport('Attr').Attr
        (prefix, localName) = SplitQName(qualifiedName)
        if prefix == 'xml':
            if namespaceURI and namespaceURI != XML_NAMESPACE:
                raise NamespaceErr()
        if localName == 'xmlns':
            if namespaceURI != XMLNS_NAMESPACE:
                raise NamespaceErr()
            a = Attr(self, qualifiedName, XMLNS_NAMESPACE, 'xmlns', prefix)
        else:
            if (not namespaceURI and prefix) or (not prefix and namespaceURI):
                raise NamespaceErr()
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

    def _4dom_addSingle(self, node):
        '''Make sure only one Element node is added to a Document'''
        if node.nodeType == Node.ELEMENT_NODE:
            self._4dom_validateNode(node)
            if node.parentNode != None:
                node.parentNode.removeChild(node)
            if self.__dict__['__documentElement']:
                raise HierarchyRequestErr()
            self.__dict__['__documentElement'] = node

    def appendChild(self, newChild):
        self._4dom_addSingle(newChild)
        return Node.appendChild(self, newChild)

    def insertBefore(self, newChild, oldChild):
        self._4dom_addSingle(newChild)
        return Node.insertBefore(self, newChild, oldChild)

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType != Node.DOCUMENT_FRAGMENT_NODE:
            root = self.__dict__['__documentElement']
            if root in [oldChild, newChild]:
                self.__dict__['__documentElement'] = None
            else:
                raise HierarchyRequestErr()
        replaced = Node.replaceChild(self, newChild, oldChild)
        if newChild.nodeType == Node.ELEMENT_NODE:
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
    def createEvent(self,eventType):
        if eventType in Event.supportedEvents:
            #Only mutation events are supported
            return Event.MutationEvent(eventType)
        else:
            raise NotSupportedErr()

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
