########################################################################
#
# File Name:            Text.py
#
# Documentation:        http://docs.4suite.com/4DOM/Text.py.html
#
# History:
# $Log: Text.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.28  2000/06/16 17:31:55  jkloth
# Added escaping to repr output
#
# Revision 1.27  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.26  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.25  2000/05/10 00:51:00  uogbuji
# Resurrect fixes to HTML reader and printer.
#
# Revision 1.24  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.21  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.20  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.19  1999/11/18 06:55:28  uche
# Python/DOM binding changes.
#
# Revision 1.18  1999/11/18 06:38:36  uche
# Changes to new Python/Dom Binding
#
# Revision 1.17  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
#
# Revision 1.16  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.15  1999/09/09 17:03:42  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.14  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.13  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.12  1999/08/31 14:45:51  molson
# Tested over the orb with Fnorb
#
# Revision 1.11  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR
from xml.dom.CharacterData import CharacterData
from xml.dom.Node import Node

class Text(CharacterData):
    nodeType = Node.TEXT_NODE

    def __init__(self, ownerDocument, data):
        CharacterData.__init__(self, ownerDocument, data)
        self.__dict__['__nodeName'] = '#text'

    ### Methods ###

    def splitText(self, offset):
        offset = int(offset)
        if offset >= self.length or offset < 0:
            raise DOMException(INDEX_SIZE_ERR)
        cur = self.data
        next = cur[offset:]
        cur = cur[:offset]
        self.data = cur
        n = self.ownerDocument.createTextNode(next)
        p = self.parentNode
        ns = self.nextSibling
        if p == None:
            return n
        if ns == None:
            p.appendChild(n)
        else:
            p.insertBefore(n, ns)
        return n

    ### Internal Methods ###

    def _4dom_joinText(self,node1,node2):
        #Create the new text node with Combined data
        newChild = self.ownerDocument.createTextNode(node1.data + node2.data)

        #Find where to add it 
        p1 = node1.parentNode
        p2 = node2.parentNode

        #Try to put it on the tree
        if (p1,p2) == (None,None):
            #Nothing we can do
            pass
        elif p1 == None:
            #We know p2 is good, put it on that tree
            p2.replaceChild(newChild,node2)
        elif p2 == None:
            #We know p1 is good, go for that tree
            p1.replaceChild(newChild,node1)
        else:
            #They are both good, go for p1
            p2.removeChild(node2)
            p1.replaceChild(newChild,node1)
        return newChild

    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createTextNode(self.data)
            else:
                node = newOwner.createTextNode(self.data)
        return CharacterData.cloneNode(self, deep, node)

    def __repr__(self):
        # Trim to a managable size
        if len(self.data) > 20:
            data = self.data[:20] + '...'
        else:
            data = self.data

        # Escape unprintable chars
        import string
        for ws in ['\011','\012','\015']:
            data = string.replace(data, ws, '\\%s' % oct(ord(ws)))

        st = "<Text Node at %s: data = '%s'>" % (
                id(self),
                data
                )
        return st

