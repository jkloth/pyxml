########################################################################
#
# File Name:            DocumentType.py
#
# Documentation:        http://docs.4suite.com/4DOM/DocumentType.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('FtNode').Node


class DocumentType(Node):
    nodeType = Node.DOCUMENT_TYPE_NODE

    def __init__(self, name, entities, notations, publicId, systemId):
        Node.__init__(self, None, '', '', '')
        #Initialize defined member variables
        self.__dict__['__nodeName'] = name
        self.__dict__['__entities'] = entities
        self.__dict__['__notations'] = notations
        self.__dict__['__publicId'] = publicId;
        self.__dict__['__systemId'] = systemId;
        #FIXME: Text repr of the entities
        self.__dict__['__internalSubset'] = ''

    ### Attribute Methods ###

    def _get_name(self):
        return self.__dict__['__nodeName']

    def _get_entities(self):
        return self.__dict__['__entities']

    def _get_notations(self):
        return self.__dict__['__notations']

    def _get_publicId(self):
        return self.__dict__['__publicId']

    def _get_systemId(self):
        return self.__dict__['__systemId']

    def _get_internalSubset(self):
        return self.__dict__['__internalSubset']

    ### Overridden Methods ###

    def __repr__(self):
        return "<DocumentType Node at %s: Name = '%s' with %d entities and %d notations>" % (
            id(self),
            self.nodeName,
            len(self.entities),
            len(self.notations)
            )

    ### Internal Methods ###

    # Behind the back setting of doctype's ownerDocument
    # Also sets the owner of the NamedNodeMaps
    def _4dom_setOwnerDocument(self, newOwner):
        self.__dict__['__ownerDocument'] = newOwner
        #self.__dict__['__entities']._4dom_setOwnerDocument(newOwner)
        #self.__dict__['__notations']._4dom_setOwnerDocument(newOwner)

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.nodeName,
                implementation._4dom_createNamedNodeMap(),    # entities
                implementation._4dom_createNamedNodeMap(),    # notations
                self.publicId,
                self.systemId
                )

    def __getstate__(self):
        return (self.ownerDocument, self.entities, self.notations)

    def __setstate__(self, state):
        self._4dom_setOwnerDocument(state[0])
        for entity in state[1]:
            # Entities can contain children, so go deep
            newEntity = entity.cloneNode(1)
            self.__dict__['__entities'].setNamedItem(newEntity)
        for notation in state[2]:
            # Notations cannot contain children
            newNotation = notation.cloneNode(0)
            self.__dict__['__notations'].setNamedItem(newNotation)

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'name':_get_name,
                               'entities':_get_entities,
                               'notations':_get_notations,
                               'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'internalSubset':_get_internalSubset
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
