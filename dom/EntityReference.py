########################################################################
#
# File Name:            EntityReference.py
#
# Documentation:        http://docs.4suite.com/4DOM/EntityReference.py.html
#
# History:
# $Log: EntityReference.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:50  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.15  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.14  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.13  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.12  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.11  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.10  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.9  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.8  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.7  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.6  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""



from xml.dom.Node import Node

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

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createEntityReference(self.nodeName)
            else:
                node = newOwner.createEntityReference(self.nodeName)
        return Node.cloneNode(self, deep, node)

    def __repr__(self):
        return '<Entity Reference Node at %s: Name = "%s">' % (
            id(self),
            self.nodeName
            )
