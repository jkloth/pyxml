########################################################################
#
# File Name:            NodeList.py
#
# Documentation:        http://docs.4suite.com/4DOM/NodeList.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import UserList
import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node
DOMException = dom.DOMException
NoModificationAllowedErr = dom.NoModificationAllowedErr


class NodeList(UserList.UserList):
    # For internal purposes
    nodeType = Node._NODE_LIST

    def __init__(self, list=None):
        UserList.UserList.__init__(self, list or [])
        return

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
        raise NoModificationAllowedErr()

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


