########################################################################
#
# File Name:            HTMLCollection.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLCollection.py.html
#
# History:
# $Log: HTMLCollection.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.23  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.22  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.21  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.19  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.18  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.17  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.16  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.15  1999/11/04 01:38:12  molson
# Fixed Minor bugs
#
# Revision 1.14  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import DOMException
from xml.dom.Node import Node
from xml.dom import INDEX_SIZE_ERR
import UserList

class HTMLCollection(UserList.UserList):

    def __init__(self, list=None):
        UserList.UserList.__init__(self, list or [])
        self.length = len(self)

    def _get_length(self):
        return self.length

    def item(self,index):
        if self.length <= index:
            return None
        else:
            return self[int(index)]

    def namedItem(self,name):
    #First check based on ID
        for node in self:
            if node.getAttribute('ID') == name:
                return node
    #Now check for a name
        for node in self:
            if node.getAttribute('NAME') == name:
                return node
        return None

    def append(self,value):
        rt =  UserList.UserList.append(self,value)
        self.length = len(self)
        return rt

    def insert(self,index,value):
        rt = UserList.UserList.insert(self,index,value)
        self.length = len(self)
        return rt

    def __delitem__(self,index):
        rt = UserList.UserList.__delitem__(self,index)
        self.length = len(self)
        return rt

    def __add__(self,other):
        rt = UserList.UserList.__add__(self,other)
        self.length = len(self)
        return rt

    def __mul__(self,other):
        rt = UserList.UserList.__mul__(self,other)
        self.length = len(self)
        return rt

    def __repr__(self):
        st = "<HTMLCollection at %s: ["%(id(self))
        for i in self:
            st = st + repr(i) + ', '
        st = st[:-2] + ']>'
        return st

#--- (end HTMLCollection.py) ---
