########################################################################
#
# File Name:            HTMLCollection.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLCollection.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import NoModificationAllowedErr
from xml.dom.html import HTML_NAME_ALLOWED
import UserList

class HTMLCollection(UserList.UserList):

    def __init__(self, list=None):
        UserList.UserList.__init__(self, list or [])

    ### Attribute Access Methods ###

    def __getattr__(self, name):
        if name == 'length':
            return self._get_length()
        # Pass-through
        return getattr(HTMLCollection, name)

    def __setattr__(self, name, value):
        if name == 'length':
            self._set_length(value)
        # Pass-through
        self.__dict__[name] = value

    ### Attribute Methods ###

    def _get_length(self):
        return self.__len__()

    def _set_length(self, value):
        raise NoModificationAllowedErr()

    ### Methods ###

    def item(self, index):
        if index >= self.__len__():
            return None
        else:
            return self[int(index)]

    def namedItem(self, name):
        found_node = None
        for node in self:
            if node.getAttribute('ID') == name:
                return node
            if not found_node and node.getAttribute('NAME') == name \
            and node.tagName in HTML_NAME_ALLOWED:
                found_node = node
        return found_node

    ### Overridden Methods ###

    def __repr__(self):
        st = "<HTMLCollection at %s: [" % (id(self))
        if len(self):
            for i in self[:-1]:
                st = st + repr(i) + ', '
            st = st + repr(self[-1])
        st = st + ']>'
        return st
