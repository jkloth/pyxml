########################################################################
#
# File Name:   ParsedStep.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedStep.py.html
#
"""
A Parsed token that represents a step on the result tree.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import Util
from xml.xpath import XPath
from xml.xpath import ParsedToken
from xml.xpath import NamespaceNode

import sys

class ParsedStep(ParsedToken.ParsedToken):
    def __init__(self, axis, nodeTest, predicates):
        ParsedToken.ParsedToken.__init__(self, 'STEP')
        self._axis = axis
        self._nodeTest = nodeTest
        self._predicates = predicates
        return

    def select(self, context):
        """
        Select a set of nodes from the axis, then filter through the node
        test and the predicates.
        """
        (node_set, reverse) = self._axis.select(context, self._nodeTest.match)
        if len(self._predicates) and len(node_set):
            node_set = self._predicates.filter(node_set, context, reverse)
        return node_set

    # For XSLT expressions
    evaluate = select
    
    def pprint(self, indent=''):
        print indent + str(self)
        self._axis.pprint(indent + '  ')
        self._nodeTest.pprint(indent + '  ')
        self._predicates.pprint(indent + '  ')

    def __str__(self):
        return '<Step at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._axis) + '::' + repr(self._nodeTest) + repr(self._predicates)
        
