########################################################################
#
# File Name:            DocumentFragment.py
#
# Documentation:        http://docs.4suite.com/4DOM/DocumentFragment.py.html
#
# History:
# $Log: DocumentFragment.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:50  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.20  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.19  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.18  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.17  2000/02/20 02:57:45  uche
# Add Mike Kay complex count example and fix some bugs that cropped up.
#
# Revision 1.16  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.15  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.14  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.13  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.12  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.11  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.10  1999/08/29 04:07:59  uche
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

class DocumentFragment(Node):
    nodeType = Node.DOCUMENT_FRAGMENT_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE]

    def __init__(self, ownerDocument):
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeName'] = '#document-fragment'

    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createDocumentFragment()
            else:
                node = newOwner.createDocumentFragment()
        Node.cloneNode(self, deep, node)
        return node

    def __repr__(self):
        return '<Document Fragment Node at %s: with %d children>' % (
                id(self),
                self.childNodes.length
                )
