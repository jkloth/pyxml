########################################################################
#
# File Name:            Text.py
#
# Documentation:        http://docs.4suite.com/4DOM/Text.py.html
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
CharacterData = implementation._4dom_fileImport('CharacterData').CharacterData
DOMException = dom.DOMException
INDEX_SIZE_ERR = dom.INDEX_SIZE_ERR


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

    def __repr__(self):
        # Trim to a managable size
        if len(self.data) > 20:
            data = self.data[:20] + '...'
        else:
            data = self.data

        # Escape unprintable chars
        import string
        for ws in ['\t','\n','\r']:
            data = string.replace(data, ws, '\\0x%x' % ord(ws))

        st = "<Text Node at %x: data = '%s'>" % (
                id(self),
                data
                )
        return st
