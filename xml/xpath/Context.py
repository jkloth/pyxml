########################################################################
#
# File Name:   Context.py
#
# Docs:        http://docs.4suite.com/XPATH/Context.py.html
#
"""
The context of an XPath expression.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import xml.dom.ext
import CoreFunctions

class Context:
    functions = CoreFunctions.CoreFunctions

    def __init__(self,
                 node,
                 position=1,
                 size=1,
                 varBindings=None,
                 processorNss=None):
        self.node = node
        self.position = position
        self.size = size
        self.varBindings = varBindings or {}
        self.processorNss = processorNss or {}
        self._cachedNss = None
        self._cachedNssNode = None

    def __repr__(self):
        return "<Context at %s: Node=%s, Postion=%d, Size=%d>" % (
            id(self),
            self.node,
            self.position,
            self.size
            )

    def nss(self):
        if self._cachedNss is None or self.node != self._cachedNssNode:
            nss = xml.dom.ext.GetAllNs(self.node)
            self._cachedNss = nss
            self._cachedNssNode = self.node
        return self._cachedNss

    def next(self):
        pass

    def setNamespaces(self, processorNss):
        self.processorNss = processorNss

    def copyNamespaces(self):
        return self.processorNss.copy()

    def copyNodePosSize(self):
        return (self.node,self.position,self.size)

    def setNodePosSize(self,(node,pos,size)):
        self.node = node
        self.position = pos
        self.size = size

    def copy(self):
        return self.__dict__.copy()

    def set(self,d):
        self.__dict__ = d

