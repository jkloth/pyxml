########################################################################
#
# File Name:            NodeList.py
#
# Documentation:        http://docs.4suite.com/4DOM/NodeList.py.html
#
# History:
# $Log: NodeList.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.34  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.33  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.32  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.31  2000/02/07 15:53:54  uche
# Minor fixes to __repr__s
#
# Revision 1.30  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.29  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.28  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.27  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.26  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.25  1999/11/18 04:35:17  molson
# Finished converting nodelist and namednodemap to new interface
#
# Revision 1.24  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.23  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.22  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.21  1999/09/09 08:04:52  uche
# NodeIterator.nextNode works and is tested.
#
# Revision 1.20  1999/08/31 19:03:10  uche
# Change NodeLists and NamedNodeMaps to use UserList and UserDict.
#
# Revision 1.19  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import UserList
from xml.dom import DOMException
from xml.dom import NO_MODIFICATION_ALLOWED_ERR

class NodeList(UserList.UserList):
    def __init__(self, list=None):
        UserList.UserList.__init__(self, list or [])

    ### Attribute Access Methods ###

    def __getattr__(self, name):
        if name == 'length':
            return self._get_length()
        #Pass-through
        return getattr(NodeList, name)

    def __setattr__(self, name, value):
        if name == 'length':
            self._set_length(value)
        #Pass-through
        self.__dict__[name] = value

    ### Attribute Methods ###

    def _get_length(self):
        return self.__len__()

    def _set_length(self,value):
        raise DOMException(NO_MODIFICATION_ALLOWED_ERR)

    ### Methods ###

    def item(self, index):
        if index >= self.__len__():
            return None
        else:
            return self[int(index)]

    #Not defined in the standard
    def contains(self, node):
        return node in self

    def __repr__(self):
        st = "<NodeList at %s: ["%(id(self))
        if len(self):
            for i in self[:-1]:
                st = st + repr(i) + ', '
            st = st + repr(self[-1])
        st = st + ']>'
        return st
