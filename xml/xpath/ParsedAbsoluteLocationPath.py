########################################################################
#
# File Name:   ParsedAbsoluteLocationPath.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedAbsoluteLocationPath.py.html
#
"""
A Parsed Token that represents a absolute location path in the parsed tree.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000, 2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import ParsedToken
from xml.dom import Node


class ParsedAbsoluteLocationPath(ParsedToken.ParsedToken):
    def __init__(self, child):
        ParsedToken.ParsedToken.__init__(self,'ABSOLUTE_LOCATION_PATH')
        self._child = child

    def select(self, context):
        if context.node.nodeType == Node.DOCUMENT_NODE:
            root = context.node
        else:
            root = context.node.ownerDocument
        if self._child == None:
            return [root]

        origState = context.copyNodePosSize()

        context.setNodePosSize((root,1,1))
        rt = self._child.select(context)

        context.setNodePosSize(origState)

        return rt

    def pprint(self, indent=''):
        print indent + str(self)
        self._child and self._child.pprint(indent + '  ')


    def __str__(self):
        return '<AbsoluteLocationPath at %x: %s>' % (
            id(self),
            repr(self),
            )

    def __repr__(self):
        return '/' + (self._child and repr(self._child) or '')
