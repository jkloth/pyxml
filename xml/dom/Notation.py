########################################################################
#
# File Name:            Notation.py
#
# Documentation:        http://docs.4suite.com/4DOM/Notation.py.html
#
"""
Implementation of DOM Level 2 Notation interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node

class Notation(Node):
    nodeType = Node.NOTATION_NODE

    def __init__(self, ownerDocument, publicId, systemId, name):
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeName'] = name
        self.__dict__['__publicId'] = publicId
        self.__dict__['__systemId'] = systemId

    ### Attribute Methods ###
        
    def _get_systemId(self):
        return self.__dict__['__systemId']
    
    def _get_publicId(self):
        return self.__dict__['__publicId']
        
    ### Overridden Methods ###

    def __repr__(self):
        return '<Notation Node at %s: PublicId = "%s" SystemId = "%s" Name = "%s">' % (id(self),self.publicId,self.systemId,self.nodeName)

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.publicId,
                self.systemId,
                self.nodeName
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'publicId':_get_publicId,
                               'systemId':_get_systemId
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
