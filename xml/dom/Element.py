########################################################################
#
# File Name:            Element.py
#
# Documentation:        http://docs.4suite.com/4DOM/Element.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from DOMImplementation import implementation
from FtNode import FtNode

import Event
from xml.dom import Node
from xml.dom import XML_NAMESPACE
from xml.dom import EMPTY_NAMESPACE
from xml.dom import InvalidCharacterErr
from xml.dom import WrongDocumentErr
from xml.dom import InuseAttributeErr
from xml.dom import NotFoundErr
from xml.dom import SyntaxErr
from xml.dom import NamespaceErr

from ext import SplitQName, IsDOMString

import re, string
#FIXME: should allow combining characters: fix when Python gets Unicode
g_namePattern = re.compile('[a-zA-Z_:][\w\.\-_:]*\Z')

class Element(FtNode):
    nodeType = Node.ELEMENT_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.TEXT_NODE,
                        Node.COMMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, nodeName, namespaceURI, prefix, localName):
        FtNode.__init__(self, ownerDocument, namespaceURI, prefix, localName);
        #Set our attributes
        self.__dict__['__attributes'] = implementation._4dom_createNamedNodeMap(ownerDocument)
        self.__dict__['__nodeName'] = nodeName

    ### Attribute Methods ###

    def _get_tagName(self):
        return self.__dict__['__nodeName']

    ### Methods ###

    def getAttribute(self, name):
        return self.getAttributeNS(EMPTY_NAMESPACE,name)

    def getAttributeNode(self, name):
        return self.getAttributeNodeNS(EMPTY_NAMESPACE,name)

    def getElementsByTagName(self, tagName):
        return self.getElementsByTagNameNS(EMPTY_NAMESPACE,tagName)
    
    def hasAttribute(self, name):
        return self.hasAttributeNS(EMPTY_NAMESPACE,name)

    def removeAttribute(self, name):
        self.removeAttributeNS(EMPTY_NAMESPACE,name)

    def removeAttributeNode(self, node):
        self.attributes.removeNamedItemNS(node.namespaceURI, node.localName)
        node._4dom_setOwnerElement(None)
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=node,
                                     attrName=node.name,
                                     attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return node

    def setAttribute(self, name, value):
        self.setAttributeNS(EMPTY_NAMESPACE,name,value)

    def setAttributeNode(self, node):
        return self.setAttributeNodeNS(node)

    ### DOM Level 2 Methods ###

    def getAttributeNS(self, namespaceURI, localName):
        attr = self.attributes.getNamedItemNS(namespaceURI, localName)
        return attr and attr.value or ''

    def getAttributeNodeNS(self, namespaceURI, localName):
        return self.attributes.getNamedItemNS(namespaceURI, localName)

    def getElementsByTagNameNS(self, namespaceURI, localName):
        if namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        nodeList = implementation._4dom_createNodeList()
        elements = filter(lambda node, type=Node.ELEMENT_NODE:
                          node.nodeType == type,
                          self.childNodes)
        for element in elements:
            if ((namespaceURI == '*' or element.namespaceURI == namespaceURI)
                and (localName == '*' or element.localName == localName)):
                nodeList.append(element)
            nodeList.extend(list(element.getElementsByTagNameNS(namespaceURI,
                                                                localName)))
        return nodeList

    def hasAttributeNS(self, namespaceURI, localName):
        return self.attributes.getNamedItemNS(namespaceURI, localName) is not None

    def removeAttributeNS(self, namespaceURI, localName):
        # Silently return if not attribute
        node = self.attributes.getNamedItemNS(namespaceURI, localName)
        if node:
            self.removeAttributeNode(node)
        return

    def setAttributeNS(self, namespaceURI, qualifiedName, value):
        if not IsDOMString(value):
            raise SyntaxErr()
        if not g_namePattern.match(qualifiedName):
            raise InvalidCharacterErr()

        prefix, localName = SplitQName(qualifiedName)
        attr = self.attributes.getNamedItemNS(namespaceURI, localName)
        if attr:
            attr.value = value
        else:
            attr = self.ownerDocument.createAttributeNS(namespaceURI, qualifiedName)
            attr.value = value
            self.setAttributeNodeNS(attr)
        return

    def setAttributeNodeNS(self, node):
        if self.ownerDocument != node.ownerDocument:
            raise WrongDocumentErr()
        if node.ownerElement != None:
            raise InuseAttributeErr()

        old = self.attributes.getNamedItemNS(node.namespaceURI, node.localName)
        if old:
            self._4dom_fireMutationEvent('DOMAttrModified',
                                         relatedNode=old,
                                         prevValue=old.value,
                                         attrName=old.name,
                                         attrChange=Event.MutationEvent.REMOVAL)
        self.attributes.setNamedItemNS(node)
        node._4dom_setOwnerElement(self)
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=node,
                                     newValue=node.value,
                                     attrName=node.name,
                                     attrChange=Event.MutationEvent.ADDITION)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return old

    ### Overridden Methods ###

    def __repr__(self):
        return "<Element Node at %x: Name='%s' with %d attributes and %d children>" % (
            id(self),
            self.nodeName,
            len(self.attributes),
            len(self.childNodes)
            )

    # Behind the back setting of element's ownerDocument
    # Also sets the owner of the NamedNodeMaps
    def _4dom_setOwnerDocument(self, newOwner):
        self.__dict__['__ownerDocument'] = newOwner
        self.__dict__['__attributes']._4dom_setOwnerDocument(newOwner)

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        e = self.__class__(owner,
                           self.nodeName,
                           self.namespaceURI,
                           self.prefix,
                           self.localName)
        for attr in self.attributes:
            clone = attr._4dom_clone(owner)
            if clone.localName is None:
                e.attributes.setNamedItem(clone)
            else:
                e.attributes.setNamedItemNS(clone)
            clone._4dom_setOwnerElement(e)
        return e

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName,
                self.namespaceURI,
                self.prefix,
                self.localName
                )

    def __getstate__(self):
        return (self.childNodes, self.attributes)

    def __setstate__(self, (children, attrs)):
        FtNode.__setstate__(self, children)
        self.__dict__['__attributes'] = attrs
        for attr in attrs:
            attr._4dom_setOwnerElement(self)

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'tagName':_get_tagName,
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
