########################################################################
#
# File Name:            CDATASection.py
#
# Documentation:        http://docs.4suite.com/4DOM/CDATASection.py.html
#
# History:
# $Log: CDATASection.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.19  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.18  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.17  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.16  1999/11/26 08:22:42  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.15  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.14  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
#
# Revision 1.13  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.12  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.11  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.10  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.9  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
Implementation of DOM Level 2 CDATASection interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Text import Text
from xml.dom.Node import Node

class CDATASection(Text):
    nodeType = Node.CDATA_SECTION_NODE

    def __init__(self, ownerDocument, data):
        Text.__init__(self, ownerDocument, data)
        self.__dict__['__nodeName'] = "#cdata-section"
    
    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createCDATASection(self.data)
            else:
                node = newOwner.createCDATASection(self.data)
        return Node.cloneNode(self,deep,node)

    def __repr__(self):
        return "<CDATA Section at %s: data = '%s%s'>" % (
            id(self)
            ,self.data[:20]
            ,(len(self.data) > 20 and "..." or "")
            )


