########################################################################
#
# File Name:            NodeIterator.py
#
# Documentation:        http://docs.4suite.com/4DOM/NodeIterator.py.html
#
"""
Node Iterators from DOM Level 2.  Allows "flat" iteration over nodes.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node
NodeFilter = implementation._4dom_fileImport('NodeFilter').NodeFilter

DOMException = dom.DOMException
NO_MODIFICATION_ALLOWED_ERR = dom.NO_MODIFICATION_ALLOWED_ERR
INVALID_STATE_ERR = dom.INVALID_STATE_ERR

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
        return next_node

    def previousNode(self):
        if self.__dict__['__detached']:
            raise DOMException(INVALID_STATE_ERR)
        prev_node = self.__regress()
        while prev_node and not (self.__checkWhatToShow(prev_node) and self.__checkFilter(prev_node) == NodeFilter.FILTER_ACCEPT):
            prev_node = self.__regress()
        return prev_node
        
    def detach(self):
        self.__dict__['__detached'] = 1

    def __advance(self):
        #Deasil?  --Uche
        if not self.__dict__['__nodeStack']:
            self.__dict__['__nodeStack'].append(self.__dict__['__root'])
            return self.__dict__['__root']
        index = 1
        for sub_root in self.__dict__['__nodeStack'][1:]:
            #FIXME: getChildIndex Not DOM compliant
            if getChildNodeIndex(self.__dict__['__nodeStack'][index-1],sub_root) == -1:
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
        return curr_node

    def __regress(self):
        #Widdershins?  --Uche
        if not self.__dict__['__nodeStack']:
            return None
        index = 1
        for sub_root in self.__dict__['__nodeStack'][1:]:
            if getChildNodeIndex(self.__dict__['__nodeStack'][index-1],sub_root) == -1:
                self.__dict__['__nodeStack'] = self.__dict__['__nodeStack'][:index]
                break
            index = index + 1
        result = self.__dict__['__nodeStack'][-1]

        curr_node = self.__dict__['__nodeStack'][-1].previousSibling
        del self.__dict__['__nodeStack'][-1]
        while curr_node:
            self.__dict__['__nodeStack'].append(curr_node)
            curr_node = curr_node.lastChild

        return result

    def __checkWhatToShow(self, node):
        show_bit = 1 << (node.nodeType - 1)
        return self.__dict__['__whatToShow'] & show_bit

    def __checkFilter(self, node):
        if self.__dict__['__filter']:
            return self.__dict__['__filter'].acceptNode(node)
        else:
            return NodeFilter.FILTER_ACCEPT



def getChildNodeIndex(pNode,child):
    if child in pNode.childNodes:
        return pNode.childNodes.index(child)
    return -1
