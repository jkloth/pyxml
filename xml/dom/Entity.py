########################################################################
#
# File Name:            Entity.py
#
# Documentation:        http://docs.4suite.com/4DOM/Entity.py.html
#
# History:
# $Log: Entity.py,v $
# Revision 1.1  2000/06/06 01:36:05  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.15  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.14  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.13  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.12  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.11  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.10  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.9  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.8  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
Implementation of DOM Level 2 Entity interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Node import Node

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
        
   ### Overridden Methods (from Node) ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument._4dom_createEntity(self.publicId, self.systemId, self.notationName)
            else:
                node = self.ownerDocument._4dom_createEntity(self.publicId, self.systemId, self.notationName)
        return Node.cloneNode(self, deep, node)

    def __repr__(self):
        return '<Entity Node at %s: PublicId = "%s" SystemId = "%s" Notation Name = "%s">' % (id(self),self.publicId,self.systemId,self.notationName)

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'notationName':_get_notationName
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = Node._readOnlyAttrs
    for attr in _readComputedAttrs.keys():
        if not _writeComputedAttrs.has_key(attr):
            _readOnlyAttrs.append(attr)
