########################################################################
#
# File Name:            Entity.py
#
# Documentation:        http://docs.4suite.com/4DOM/Entity.py.html
#
"""
Implementation of DOM Level 2 Entity interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node

class Entity(Node):
    nodeType = Node.ENTITY_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, publicId, systemId, notationName):
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeName'] = '#entity'
        self.__dict__['__publicId'] = publicId
        self.__dict__['__systemId'] = systemId
        self.__dict__['__notationName'] = notationName
        
    ### Attribute Methods ###

    def _get_systemId(self):
        return self.__dict__['__systemId']
    
    def _get_publicId(self):
        return self.__dict__['__publicId']

    def _get_notationName(self):
        return self.__dict__['__notationName']
        
   ### Overridden Methods ###

    def __repr__(self):
        return '<Entity Node at %s: PublicId = "%s" SystemId = "%s" Notation Name = "%s">' % (id(self),self.publicId,self.systemId,self.notationName)

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.publicId,
                self.systemId,
                self.notationName
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'notationName':_get_notationName
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
