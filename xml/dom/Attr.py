########################################################################
#
# File Name:            Attr.py
#
# Documentation:        http://docs.4suite.com/4DOM/Attr.py.html
#
"""
DOM Level 2 Attribute Node
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')
Node = implementation._4dom_fileImport('FtNode').Node
MutationEvent = implementation._4dom_fileImport('Event').MutationEvent

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
        owner = self.__dict__['__ownerElement']
        old_value = self.value
        if value != old_value:
            if value is not None:
                nl = [self.ownerDocument.createTextNode(value)]
            else:
                nl = []
                attrChange = MutationEvent.REMOVAL

            self.__dict__['__childNodes'] = implementation._4dom_createNodeList(nl)

            if owner:
                owner._4dom_fireMutationEvent('DOMAttrModified',
                                              relatedNode=self,
                                              prevValue=old_value,
                                              newValue=value,
                                              attrName=self.name,
                                              attrChange=MutationEvent.MODIFICATION)
                owner._4dom_fireMutationEvent('DOMSubtreeModified')


    def _get_ownerElement(self):
        return self.__dict__['__ownerElement']

    ### Overridden Methods ###

    def _get_nodeValue(self):
        return self._get_value()

    def _set_nodeValue(self, value):
        self._set_value(value)

    def __repr__(self):
         return '<Attribute Node at %s: Name = "%s", Value = "%s">' % (
             id(self),
             self.name,
             self.value
             )

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName,
                self.namespaceURI,
                self.prefix,
                self.localName
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
