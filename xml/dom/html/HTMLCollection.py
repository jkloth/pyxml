########################################################################
#
# File Name:            HTMLCollection.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLCollection.py.html
#
# History:
# $Log: HTMLCollection.py,v $
# Revision 1.3  2000/06/20 16:03:15  uche
# Put back in the "static" HTML files.
#
# Revision 1.24  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
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

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR
from xml.dom import NO_MODIFICATION_ALLOWED_ERR
from xml.dom.Node import Node
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
        raise DOMException(NO_MODIFICATION_ALLOWED_ERR)

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
