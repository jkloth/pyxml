########################################################################
#
# File Name:            EntityReference.py
#
# Documentation:        http://docs.4suite.com/4DOM/EntityReference.py.html
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

class EntityReference(Node):
    nodeType = Node.ENTITY_REFERENCE_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE,
                        ]

    def __init__(self, ownerDocument, name):
        #Note: the Entity's name is treated as nodeName
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeName'] = name

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName
                )

    def __repr__(self):
        return '<Entity Reference Node at %s: Name = "%s">' % (
            id(self),
            self.nodeName
            )
