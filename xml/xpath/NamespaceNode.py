########################################################################
#
# File Name:   NamespaceNode.py
#
# Docs:        http://docs.4suite.org/XPATH/NamespaceNode.py.py.html
#
"""
A container class for the namespace axis results.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.xpath import NAMESPACE_NODE

class NamespaceNode:
    def __init__(self, prefix, uri, ownerDoc=None):
        self.prefix = ''
        self.nodeName = self.localName = prefix
        self.namespaceURI = ''
        self.value = uri
        self.nodeType = NAMESPACE_NODE
        self.ownerDocument = ownerDoc
        return

