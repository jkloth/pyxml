########################################################################
#
# File Name:   ExpandedNameWrapper.py
#
# Docs:        http://docs.4suite.com/XPATH/ExpandedNameWrapper.py.html
#
"""
A structure to hold a node's expanded name.  Internal use only.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from xml.xpath import NAMESPACE_NODE
from xml.xpath import NamespaceNode

class ExpandedNameWrapper:
    def __init__(self, node):
        self.namespaceURI = ''
        self.localName = ''
        self.qName = ''
        if hasattr(node, 'nodeType'):
            if node.nodeType in [Node.ELEMENT_NODE, Node.ATTRIBUTE_NODE]:
                self.namespaceURI = node.namespaceURI
                self.localName = node.localName
                self.qName = node.nodeName
            elif node.nodeType == NAMESPACE_NODE:
                self.qName = self.localName = node.localName
            elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
                self.qName = self.localName = node.target

