########################################################################
#
# File Name:   ParsedNodeTest.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedNodeTest.py.html
#
"""
A Parsed Token that represents a node test.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import Node
from xml.xpath import ParsedToken
from xml.xpath import NamespaceNode
from xml.xpath import XPath
from xml.xpath import NAMESPACE_NODE
from xml.xpath import g_xpathRecognizedNodes 

import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]

def ParsedNodeTest(tok,st):
    if tok == XPath.WILDCARD_NAME:
        if st == '*':
            return PrincipalTypeTest(tok, st)
        index = string.find(st, ':')
        if st[index:] == ':*':
            return LocalNameTest(tok, st, st[:index])
        elif index >= 0:
            return QualifiedNameTest(tok, st, st[:index], st[index+1:])
        return NodeNameTest(tok, st)
    return g_classMap[tok](tok,st)


class NodeTestBase(ParsedToken.ParsedToken):
    def __init__(self, tok, st):
        ParsedToken.ParsedToken.__init__(self, 'NODE_TEST')
        self.tok = tok
        self.st = st
        self.priority = -0.5

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        """
        The principalType is discussed in section [2.3 Node Tests]
        of the XPath 1.0 spec.  Only attribute and namespace axes
        differ from the default of elements.
        """
        return 0

    def __str__(self):
        return '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self),
            )

    def __repr__(self):
        if self.tok == XPath.WILDCARD_NAME or self.tok == 0:
            result = self.st
        else:
            token = string.lower(ParsedToken.TOKEN_MAP[self.tok])
            result = string.replace(token, '_', '-') + '(' + self.st + ')'
        return result


class NodeTest(NodeTestBase):
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType in g_xpathRecognizedNodes or isinstance(node,NamespaceNode.NamespaceNode)


class CommentNodeTest(NodeTestBase):
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType == Node.COMMENT_NODE


class TextNodeTest(NodeTestBase):
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType == Node.TEXT_NODE

class ProcessingInstructionNodeTest(NodeTestBase):
    def __init__(self, tok, st):
        NodeTestBase.__init__(self, tok, st)
        if st:
            self.priority = 0
            if st[0] == st[-1] and st[0] in ['"', "'"]:
                self.st = st[1:-1]

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType != Node.PROCESSING_INSTRUCTION_NODE:
            return 0
        if self.st:
            return node.target == self.st
        return 1

class PrincipalTypeTest(NodeTestBase):
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType == principalType

class LocalNameTest(NodeTestBase):
    def __init__(self, tok, st, prefix):
        NodeTestBase.__init__(self, tok, st)
        self.priority = -0.25
        self._prefix = prefix
        
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType != principalType:
            return 0
        uri = self._prefix and context.processorNss.get(self._prefix) or ''
        return node.namespaceURI == uri
    
class QualifiedNameTest(NodeTestBase):
    def __init__(self, tok, st, prefix, localName):
        NodeTestBase.__init__(self, tok, st)
        self.priority = 0
        self._prefix = prefix
        self._localName = localName

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType == principalType:
            if node.localName == self._localName:
                try:
                    return node.namespaceURI == context.processorNss[self._prefix]
                except KeyError:
                    raise Exception("Unknown namespace prefix '%s'" % self._prefix)
        return 0

class NodeNameTest(NodeTestBase):
    def __init__(self,tok,st):
        NodeTestBase.__init__(self, tok, st)
        self.priority = 0
        self._nodeName = st

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType == principalType:
            return node.nodeName == self._nodeName
        return 0



g_classMap = {XPath.NODE:NodeTest,
              XPath.COMMENT:CommentNodeTest,
              XPath.TEXT:TextNodeTest,
              XPath.PROCESSING_INSTRUCTION:ProcessingInstructionNodeTest,
             }
             
