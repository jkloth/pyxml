########################################################################
#
# File Name:            NamedNodeMap.py
#
# Documentation:        http://docs.4suite.com/4DOM/NamedNodeMap.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('FtNode').Node

DOMException = dom.DOMException
NoModificationAllowedErr = dom.NoModificationAllowedErr
NotFoundErr = dom.NotFoundErr
WrongDocumentErr = dom.WrongDocumentErr
InuseAttributeErr = dom.InuseAttributeErr

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
            raise NoModificationAllowedErr()
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
            raise WrongDocumentErr()
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise InuseAttributeErr()
        retval = self.get(arg.nodeName)
        self[arg.nodeName] = arg
        return retval

    def setNamedItemNS(self, arg):
        if self._ownerDocument != arg.ownerDocument:
            raise WrongDocumentErr()
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise InuseAttributeErr()
        retval = self.get((arg.namespaceURI, arg.localName))
        self[(arg.namespaceURI, arg.localName)] = arg
        return retval

    def removeNamedItem(self, name):
        oldNode = self.get(name)
        if not oldNode:
            raise NotFoundErr()
        del self[name]
        return oldNode

    def removeNamedItemNS(self, namespaceURI, localName):
        if namespaceURI == None:
            namespaceURI = ''
        oldNode = self.get((namespaceURI, localName))
        if not oldNode:
            raise NotFoundErr()
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
