########################################################################
#
# File Name:            NodeIterator.py
#
# Documentation:        http://docs.4suite.com/4DOM/NodeIterator.py.html
#
# History:
# $Log: NodeIterator.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.20  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.19  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.18  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.17  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.16  1999/11/19 02:13:23  uche
# Python/DOM binding update.
#
# Revision 1.15  1999/11/19 01:51:28  molson
# Added Filter support
#
# Revision 1.14  1999/11/19 01:32:41  uche
# Python/DOM binding changes.
#
# Revision 1.13  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.12  1999/09/10 02:12:19  uche
# Added TreeWalker implementation.
# Fixes to NodeIterator (runs all the way through the test suite now)
#
# Revision 1.11  1999/09/09 08:04:52  uche
# NodeIterator.nextNode works and is tested.
#
# Revision 1.10  1999/09/08 23:54:07  uche
# Add machinery for updated DOM Level 2 Iterators and Filters (untested)
#
# Revision 1.9  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.8  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
Node Iterators from DOM Level 2.  Allows "flat" iteration over nodes.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Node import Node
from xml.dom.NodeFilter import NodeFilter
from xml.dom import DOMException
from xml.dom import NO_MODIFICATION_ALLOWED_ERR
from xml.dom import INVALID_STATE_ERR

class NodeIterator:
    def __init__(self, root, whatToShow, filter, expandEntityReferences):
        self.__dict__['__root'] = root
        self.__dict__['__filter'] = filter
        self.__dict__['__expandEntityReferences'] = expandEntityReferences
        self.__dict__['__whatToShow'] = whatToShow
        self.__dict__['__nodeStack'] = []
        self.__dict__['__detached'] = 0

    def __setattr__(self,name,value):
        raise DOMException(NO_MODIFICATION_ALLOWED_ERR)

    def _get_root(self):
        return self.__dict__['__root']

    def _get_filter(self):
        return self.__dict__['__filter']

    def _get_expandEntityReferences(self):
        return self.__dict__['__expandEntityReferences']

    def _get_whatToShow(self):
        return self.__dict__['__whatToShow']
    
    def nextNode(self):
        if self.__dict__['__detached']:
            raise DOMException(INVALID_STATE_ERR)
        next_node = self.__advance()
        while next_node and not (self.__checkWhatToShow(next_node) and self.__checkFilter(next_node) == NodeFilter.FILTER_ACCEPT):
            next_node = self.__advance()
        pass
        return next_node

    def previousNode(self):
        if self.__dict__['__detached']:
            raise DOMException(INVALID_STATE_ERR)
        prev_node = self.__regress()
        while prev_node and not (self.__checkWhatToShow(prev_node) and self.__checkFilter(prev_node) == NodeFilter.FILTER_ACCEPT):
            prev_node = self.__regress()
        pass
        return prev_node
        
    def detach(self):
        self.__dict__['__detached'] = 1

    def __advance(self):
        #Deasil?  --Uche
        if not self.__dict__['__nodeStack']:
            self.__dict__['__nodeStack'].append(self.__dict__['__root'])
            pass
            return self.__dict__['__root']
        index = 1
        for sub_root in self.__dict__['__nodeStack'][1:]:
            #FIXME: getChildIndex Not DOM compliant
            if self.__dict__['__nodeStack'][index-1]._4dom_getChildIndex(sub_root) == -1:
                self.__dict__['__nodeStack'] = self.__dict__['__nodeStack'][:index]
                break
            index = index + 1
        curr_node = self.__dict__['__nodeStack'][-1].firstChild
        #If there are no children, back-track until we find a node with an unvisited sibling
        index = len(self.__dict__['__nodeStack'])
        while not curr_node and index > 1:
            curr_node = self.__dict__['__nodeStack'][index-1].nextSibling
            index = index - 1
        if curr_node:
            self.__dict__['__nodeStack'] = self.__dict__['__nodeStack'][:index]
            self.__dict__['__nodeStack'].append(curr_node)
        pass
        return curr_node

    def __regress(self):
        #Widdershins?  --Uche
        if not self.__dict__['__nodeStack']:
            pass
            return None
        index = 1
        for sub_root in self.__dict__['__nodeStack'][1:]:
            if self.__dict__['__nodeStack'][index-1]._4dom_getChildIndex(sub_root) == -1:
                self.__dict__['__nodeStack'] = self.__dict__['__nodeStack'][:index]
                break
            index = index + 1
        result = self.__dict__['__nodeStack'][-1]

        curr_node = self.__dict__['__nodeStack'][-1].previousSibling
        del self.__dict__['__nodeStack'][-1]
        while curr_node:
            self.__dict__['__nodeStack'].append(curr_node)
            curr_node = curr_node.lastChild

        pass
        return result

    def __checkWhatToShow(self, node):
        show_bit = 1 << (node._get_nodeType() - 1)
        return self.__dict__['__whatToShow'] & show_bit

    def __checkFilter(self, node):
        if self.__dict__['__filter']:
            return self.__dict__['__filter'].acceptNode(node)
        else:
            return NodeFilter.FILTER_ACCEPT

