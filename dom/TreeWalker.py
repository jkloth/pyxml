########################################################################
#
# File Name:            TreeWalker.py
#
# Documentation:        http://docs.4suite.com/4DOM/TreeWalker.py.html
#
# History:
# $Log: TreeWalker.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:50  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.6  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.5  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.4  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.3  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.2  1999/09/10 22:12:38  uche
# Added treewalker test
# Fixed serious problems with PrettyPrint
#
# Revision 1.1  1999/09/10 02:12:19  uche
# Added TreeWalker implementation.
# Fixes to NodeIterator (runs all the way through the test suite now)
#
#
#
"""
Tree Walker from DOM Level 2.  Allows multi-directional iteration over nodes.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import Node
from xml.dom.Node import Node
from xml.dom.NodeFilter import NodeFilter
from xml.dom import DOMException
from xml.dom import NOT_SUPPORTED_ERR

class TreeWalker:
    def __init__(self, root, whatToShow, filter, expandEntityReferences):
        self.__dict__['__root'] = root
        self.__dict__['__whatToShow'] = whatToShow
        self.__dict__['__filter'] = filter
        self.__dict__['__expandEntityReferences'] = expandEntityReferences
        self.__dict__['__currentNode'] = root

    ### Attribute Access Methods -- Node.attr ###

    def __getattr__(self, name):
        attrFunc = self._readComputedAttrs.get(name)
        if attrFunc:
            return attrFunc(self)

    def __setattr__(self, name, value):
        #Make sure attribute is not read-only
        if name in self.__class__._readOnlyAttrs:
            raise DOMException(NO_MODIFICATION_ALLOWED_ERR)
        #If it's computed execute that function
        attrFunc = self.__class__._writeComputedAttrs.get(name)
        if attrFunc:
            attrFunc(self, value)
        #Otherwise, just set the attribute
        else:
            self.__dict__[name] = value

    ### Attribute Methods -- Node._get_attr() ###

    def _get_root(self):
        return self.__dict__['__root']

    def _get_filter(self):
        return self.__dict__['__filter']

    def _get_whatToShow(self):
        return self.__dict__['__whatToShow']

    def _get_expandEntityReferences(self):
        return self.__dict__['__expandEntityReferences']

    def _get_currentNode(self):
        return self.__dict__['__currentNode']

    def _set_currentNode(self, value):
        if value == None:
            raise DOMException(NOT_SUPPORTED_ERR)
        self.__dict__['__currentNode'] = value

    ### Methods ###

    def parentNode(self):
        next_node = None
        if self.__dict__['__currentNode'] != self.__dict__['__root']:
            next_node = self.__dict__['__currentNode']._get_parentNode()
            while next_node and next_node != self.__dict__['__root'] \
                and not (self.__checkWhatToShow(next_node) \
                and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
                next_node = next_node._get_parentNode()
        if next_node:
            self.__dict__['__currentNode'] = next_node
            pass
        return next_node
        
    def firstChild(self):
        next_node = None
        if self.__checkFilter(self.__dict__['__currentNode']) != NodeFilter.FILTER_REJECT:
            next_node = self.__dict__['__currentNode']._get_firstChild()
            while next_node and not (self.__checkWhatToShow(next_node) \
                and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
                next_node = next_node._get_nextSibling()
        if next_node:
            self.__dict__['__currentNode'] = next_node
            pass
        return next_node
        
    def lastChild(self):
        next_node = None
        if self.__checkFilter(self.__dict__['__currentNode']) != NodeFilter.FILTER_REJECT:
            next_node = self.__dict__['__currentNode']._get_lastChild()
            while next_node and not (self.__checkWhatToShow(next_node) \
                and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
                next_node = next_node._get_previousSibling()
        if next_node:
            self.__dict__['__currentNode'] = next_node
            pass
        return next_node

    def previousSibling(self):
        prev_node = None
        if self.__dict__['__currentNode'] != self.__root:
            prev_node = self.__dict__['__currentNode']._get_previousSibling()
            while prev_node and not (self.__checkWhatToShow(prev_node) \
                and self.__checkFilter(prev_node) == NodeFilter.FILTER_ACCEPT):
                prev_node = prev_node._get_previousSibling()
        if prev_node:
            self.__dict__['__currentNode'] = prev_node
            pass
        return prev_node

    def nextSibling(self):
        next_node = None
        if self.__dict__['__currentNode'] != self.__root:
            next_node = self.__dict__['__currentNode']._get_nextSibling()
            while next_node and not (self.__checkWhatToShow(next_node) and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
                next_node = next_node._get_nextSibling()
        if next_node:
            self.__dict__['__currentNode'] = next_node
            pass
        return next_node


    def nextNode(self):
        next_node = self.__advance()
        while next_node and not (self.__checkWhatToShow(next_node) and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
            next_node = self.__advance()
        pass
        return next_node

    def previousNode(self):
        prev_node = self.__regress()
        while prev_node and not (self.__checkWhatToShow(prev_node) and self.__checkFilter(prev_node) == NodeFilter.FILTER_ACCEPT):
            prev_node = self.__regress()
        pass
        return prev_node


    def __advance(self):
        if self.firstChild():
            return self.__dict__['__currentNode']
        if self.nextSibling():
            return self.__dict__['__currentNode']
        if self.parentNode():
            return self.nextSibling()
        return None


    def __regress(self):
        if self.previousSibling():
            self.lastChild()
            return self.__dict__['__currentNode']
        if self.parentNode():
            return self.__dict__['__currentNode']
        return None


    def __checkWhatToShow(self, node):
        show_bit = 1 << (node._get_nodeType() - 1)
        return self.__dict__['__whatToShow'] & show_bit

    def __checkFilter(self, node):
        if self.__dict__['__filter']:
            return __dict__['__filter'].acceptNode(node)
        else:
            return NodeFilter.FILTER_ACCEPT

    ### Attribute Access Mappings ###

    _readComputedAttrs = {'root':_get_root,
                          'whatToShow':_get_whatToShow,
                          'filter':_get_filter,
                          'expandEntityReferences':_get_expandEntityReferences,
                          'currentNode':_get_currentNode
                          }

    _writeComputedAttrs = {'currentNode': _set_currentNode
                           }

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            _readOnlyAttrs + _readComputedAttrs.keys())
