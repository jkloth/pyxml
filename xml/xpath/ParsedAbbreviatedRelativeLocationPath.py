########################################################################
#
# File Name:   ParsedAbbreviatedRelativeLocationPath.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedAbbreviatedRelativeLocationPath.py.html
#
"""
A parsed token that represents a abbreviated relative location path.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import ParsedToken
from xml.xpath import ParsedNodeTest
from xml.xpath import ParsedPredicateList
from xml.xpath import ParsedAxisSpecifier
from xml.xpath import ParsedStep
from xml.xpath import XPath

import Set

class ParsedAbbreviatedRelativeLocationPath(ParsedToken.ParsedToken):
    def __init__(self,left,right):
        """
        left can be a step or a relative location path
        right is only a step
        """
        ParsedToken.ParsedToken.__init__(self,'ABBREVIATED_RELATIVE_LOCATION_PATH')
        self._left = left
        self._right = right
        nt = ParsedNodeTest.ParsedNodeTest(XPath.NODE,'')
        ppl = ParsedPredicateList.ParsedPredicateList([])
        as = ParsedAxisSpecifier.ParsedAxisSpecifier(XPath.DESCENDANT_OR_SELF)
        self._middle = ParsedStep.ParsedStep(as, nt, ppl)

    def select(self, context):

        res = []
        rt = self._left.select(context)
        l = len(rt)

        origState = context.copyNodePosSize()

        for ctr in range(l):
            context.setNodePosSize((rt[ctr],ctr+1,l))
            subRt = self._middle.select(context)
            res = Set.Union(res,subRt)

        rt = res
        res = []
        l = len(rt)
        for ctr in range(l):
            context.setNodePosSize((rt[ctr],ctr+1,l))
            subRt = self._right.select(context)
            res = Set.Union(res,subRt)


        context.setNodePosSize(origState)

        return res

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._middle.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<AbbreviatedRelativeLocationPath at %x: %s>' % (
            id(self),
            repr(self),
            )
    def __repr__(self):
        return repr(self._left) + '//' + repr(self._right)
