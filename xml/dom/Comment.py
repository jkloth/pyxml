########################################################################
#
# File Name:            Comment.py
#
# Documentation:        http://docs.4suite.com/4DOM/Comment.py.html
#
# History:
# $Log: Comment.py,v $
# Revision 1.1  2000/06/06 01:36:04  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.17  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.16  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.15  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.14  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.13  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
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

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""



from xml.dom.CharacterData import CharacterData

from xml.dom.Node import Node

class Comment(CharacterData):
    nodeType = Node.COMMENT_NODE

    def __init__(self,ownerDocument,data):
        CharacterData.__init__(self, ownerDocument, data)
        self.__dict__['__nodename'] = '#comment'

    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner = None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createComment(self.data)
            else:
                node = newOwner.createComment(self.data)
        return CharacterData.cloneNode(self,deep,node)

    def __repr__(self):
        st = "<Comment Node at %s: data = '%s%s'>" % (id(self)
                                                   ,self.data[:20]
                                                   ,(len(self.data) > 20 and "..." or "")
                                                   )
        return st
