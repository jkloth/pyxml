########################################################################
#
# File Name:            NamedNodeMap.py
#
# Documentation:        http://docs.4suite.com/4DOM/NamedNodeMap.py.html
#
# History:
# $Log: NamedNodeMap.py,v $
# Revision 1.3  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.37  2000/09/07 15:11:34  molson
# Modified to abstract import
#
# Revision 1.36  2000/08/01 17:49:19  jkloth
# Bug fixes from R20000724
#
# Revision 1.35  2000/07/18 16:58:52  jkloth
# Fixed small bugs
#
# Revision 1.34  2000/07/09 19:02:20  uogbuji
# Begin implementing Events
# bug-fixes
#
# Revision 1.33  2000/07/03 02:12:52  jkloth
#
# fixed up/improved cloneNode
# changed Document to handle DTS as children
# fixed miscellaneous bugs
#
# Revision 1.32  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.31  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.30  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.29  2000/02/07 15:53:54  uche
# Minor fixes to __repr__s
#
# Revision 1.28  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.27  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.26  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.25  1999/11/18 08:01:51  molson
# Added namespaces to NamedNodeMap
#
# Revision 1.24  1999/11/18 07:50:59  molson
# Added namespaces to Nodes
#
# Revision 1.23  1999/11/18 04:35:17  molson
# Finished converting nodelist and namednodemap to new interface
#
# Revision 1.22  1999/11/18 04:27:46  molson
# Tested Nodelist and namednodemap with new interface
#
# Revision 1.21  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.20  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.19  1999/09/09 17:03:41  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.18  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.17  1999/09/01 07:08:06  uche
# Fixed a bone-head error in NamedNodeMap.
#
# Revision 1.16  1999/08/31 19:03:10  uche
# Change NodeLists and NamedNodeMaps to use UserList and UserDict.
#
# Revision 1.15  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
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

DOMException = dom.DOMException
NO_MODIFICATION_ALLOWED_ERR = dom.NO_MODIFICATION_ALLOWED_ERR
NOT_FOUND_ERR = dom.NOT_FOUND_ERR
WRONG_DOCUMENT_ERR = dom.WRONG_DOCUMENT_ERR
INUSE_ATTRIBUTE_ERR = dom.INUSE_ATTRIBUTE_ERR

import UserDict
import string

class NamedNodeMap(UserDict.UserDict):
    # For internal purposes
    nodeType = Node._NAMED_NODE_MAP

    def __init__(self, owner=None):
        UserDict.UserDict.__init__(self)
        self._ownerDocument = owner

    ### Attribute Methods ###

    def __getattr__(self, name):
        if name == 'length':
            return self._get_length()
        return getattr(NamedNodeMap, name)

    def __setattr__(self, name, value):
        if name == 'length':
            raise DOMException(NO_MODIFICATION_ALLOWED_ERR)
        self.__dict__[name] = value

    def _get_length(self):
        return self.__len__()

    ### Methods ###

    def item(self, index):
        try:
            return self[self.keys()[int(index)]]
        except IndexError:
            return None

    def getNamedItem(self, name):
        return self.get(name)

    def getNamedItemNS(self, namespaceURI, localName):
        if namespaceURI == None:
            namespaceURI = ''
        return self.get((namespaceURI, localName))

    def setNamedItem(self, arg):
        if self._ownerDocument != arg.ownerDocument:
            raise DOMException(WRONG_DOCUMENT_ERR)
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise DOMException(INUSE_ATTRIBUTE_ERR)
        retval = self.get(arg.nodeName)
        self[arg.nodeName] = arg
        return retval

    def setNamedItemNS(self, arg):
        if self._ownerDocument != arg.ownerDocument:
            raise DOMException(WRONG_DOCUMENT_ERR)
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise DOMException(INUSE_ATTRIBUTE_ERR)
        retval = self.get((arg.namespaceURI, arg.localName))
        self[(arg.namespaceURI, arg.localName)] = arg
        return retval

    def removeNamedItem(self, name):
        oldNode = self.get(name)
        if not oldNode:
            raise DOMException(NOT_FOUND_ERR)
        del self[name]
        return oldNode

    def removeNamedItemNS(self, namespaceURI, localName):
        if namespaceURI == None:
            namespaceURI = ''
        oldNode = self.get((namespaceURI, localName))
        if not oldNode:
            raise DOMException(NOT_FOUND_ERR)
        del self[(namespaceURI, localName)]
        return oldNode

    ### Overridden Methods ###

    def __getitem__(self, index):
        if type(index) == type(0):
            return self[self.keys()[index]]
        else:
            return UserDict.UserDict.__getitem__(self, index)

    def __repr__(self):
        st = "<NamedNodeMap at %s: {"%(id(self))
        for k in self.keys():
            st = st + repr(k) + ': ' + repr(self[k]) + ', '
        if len(self):
            st = st[:-2]
        return st + '}>'

    ### Helper Methods for Cloning ###

    def __getinitargs__(self):
        return (self._ownerDocument,)

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state

    ### Internal Methods ###

    def _4dom_setOwnerDocument(self, newOwner):
        self._ownerDocument = newOwner
