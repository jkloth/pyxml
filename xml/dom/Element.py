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

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node

ext = implementation._4dom_fileImport('ext')
Event = implementation._4dom_fileImport('Event')
InvalidCharacterErr = dom.InvalidCharacterErr
WrongDocumentErr = dom.WrongDocumentErr()
InuseAttributeErr = dom.InuseAttributeErr
NotFoundErr = dom.NotFoundErr
XML_NAMESPACE = dom.XML_NAMESPACE

import re, string
#FIXME: should allow combining characters: fix when Python gets Unicode
g_namePattern = re.compile('[a-zA-Z_:][\w\.\-_:]*\Z')


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
        if self.hasAttribute(name):
            att = self.getAttributeNode(name)
            att.value = value
        else:
            attrChange = Event.MutationEvent.ADDITION
            att = self.ownerDocument.createAttribute(name)
            att.value = self._4dom_validateString(value)
            self.setAttributeNode(att)
        # the mutation event is fired in Attr.py

    def removeAttribute(self, name):
        try:
            old = self.attributes.removeNamedItem(name)
        except NotFoundErr:
            return
        old._4dom_setOwnerElement(None)
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=self.getAttributeNode(name),
                                     attrName=name,
                                     attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMSubtreeModified')

    def getAttributeNode(self, name):
        return self.attributes.getNamedItem(name)

    def setAttributeNode(self, node):
        ourOwner = self.ownerDocument
        nodeOwner = node.ownerDocument
        if ourOwner != None and nodeOwner != None:
            if (ourOwner.isXml() != nodeOwner.isXml()) or (ourOwner.isHtml() != nodeOwner.isHtml()):
                raise WrongDocumentErr()
        if node.ownerElement != None:
            raise InuseAttributeErr()

        old_att = None
        if self.hasAttribute(node.name):
            attrChange = Event.MutationEvent.REMOVAL
            old_att = self.getAttributeNode(node.name)

        rt = self.attributes.setNamedItem(node)
        
        node._4dom_setOwnerElement(self)
        if old_att:
            self._4dom_fireMutationEvent('DOMAttrModified',
                                         relatedNode=old_att,
                                         prevValue=old_att.value,
                                         attrName=old_att.name,
                                         attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=node,
                                     newValue=node.value,
                                     attrName=node.name,
                                     attrChange=Event.MutationEvent.ADDITION)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return rt

    def removeAttributeNode(self, node):
        old = self.getAttributeNode(node.name)
        if old != None:
            self.removeAttribute(node.name)
            name = node.name
        else:
            old = self.getAttributeNodeNS(node.namespaceURI, node.localName)
            if old != None:
                self.removeAttributeNS(node.namespaceURI, node.localName)
                name = node.localName
            else:
                raise NotFoundErr()
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=node,
                                     attrName=name,
                                     attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
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
        if self.hasAttributeNS(namespaceURI, qualifiedName):
            att = self.getAttributeNodeNS(namespaceURI, qualifiedName)
            att.value = value
        else:
            if not g_namePattern.match(qualifiedName):
                raise InvalidCharacterErr()
            att = self.ownerDocument.createAttributeNS(namespaceURI, qualifiedName)
            att.value = value
            self.setAttributeNodeNS(att)
        return

    def removeAttributeNS(self, namespaceURI, localName):
        try:
            old = self.attributes.removeNamedItemNS(namespaceURI,localName)
            if old != None:
                old._4dom_setOwnerElement(None)
        except DOMException, e:
            pass
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=self.getAttributeNodeNS(namespaceURI,localName),
                                     attrName=localName,
                                     attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return None

    def getAttributeNodeNS(self, namespaceURI, localName):
        return self.attributes.getNamedItemNS(namespaceURI, localName)

    def setAttributeNodeNS(self, node):
        ourOwner = self.ownerDocument
        nodeOwner = node.ownerDocument
        if ourOwner != nodeOwner:
            raise WrongDocumentErr()
        if node.ownerElement != None:
            raise InuseAttributeErr()

        old_att = None
        if self.hasAttribute(node.name):
            attrChange = Event.MutationEvent.REMOVAL
            old_att = self.getAttributeNode(name)
            old_value = att.value
            
        rt = self.attributes.setNamedItemNS(node)
        node._4dom_setOwnerElement(self)
        if old_att:
            self._4dom_fireMutationEvent('DOMAttrModified',
                                         relatedNode=old_att,
                                         prevValue=old_value,
                                         attrName=node.name,
                                         attrChange=Event.MutationEvent.REMOVAL)
        self._4dom_fireMutationEvent('DOMAttrModified',
                                     relatedNode=node,
                                     newValue=node.value,
                                     attrName=node.name,
                                     attrChange=Event.MutationEvent.ADDITION)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return rt

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

    def __repr__(self):
        return "<Element Node at %s: Name = '%s' with %d attributes and %d children>" % (
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

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName,
                self.namespaceURI,
                self.prefix,
                self.localName
                )

    def __getstate__(self):
        return self.attributes

    def __setstate__(self, attributes):
        for attr in attributes:
            # Attribute children are the value, so they're cloned
            # when the attribute is cloned, no need to go deep
            newAttr = attr.cloneNode(0, newOwner=self.ownerDocument)
            if self.ownerDocument._4dom_isNsAware:
                self.attributes.setNamedItemNS(newAttr)
            else:
                self.attributes.setNamedItem(newAttr)
            newAttr._4dom_setOwnerElement(self)

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
