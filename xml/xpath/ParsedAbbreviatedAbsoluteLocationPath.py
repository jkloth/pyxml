########################################################################
#
# File Name:   ParsedAbbreviatedAbsoluteLocationPath.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedAbbreviatedAbsoluteLocationPath.py.html
#
"""
A parsed token for an abreviated absolute location path.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import ParsedToken
from xml.xpath import ParsedNodeTest
from xml.xpath import ParsedPredicateList
from xml.xpath import ParsedStep
from xml.xpath import ParsedAxisSpecifier
from xml.xpath import XPath

LOOKAHEAD_OPTIMIZERS = {
    }

class ParsedAbbreviatedAbsoluteLocationPath(ParsedToken.ParsedToken):
    def __init__(self,rel):
        ParsedToken.ParsedToken.__init__(self,"ABBREVIATED_ABSOLUTE_LOCATION_PATH")
        self._rel = rel
        nt = ParsedNodeTest.ParsedNodeTest(XPath.NODE, '')
        ppl = ParsedPredicateList.ParsedPredicateList([])
        as = ParsedAxisSpecifier.ParsedAxisSpecifier(XPath.DESCENDANT_OR_SELF)
        self._step = ParsedStep.ParsedStep(as, nt, ppl)
        return

    def select(self, context):
        origState = context.copyNodePosSize()

        root = context.node.ownerDocument
        context.setNodePosSize((root,1,1))
        rt = self._step.select(context)
        res = []
        l = len(rt)
        
        sub_rt = []
        for ctr in range(l):
            n = rt[ctr]
            context.setNodePosSize((n,ctr+1,l))
            sub_rt.extend(self._rel.select(context))

        if sub_rt and hasattr(sub_rt[0], 'ownerElement'):
            result = sub_rt
        else:
            result = filter(lambda x, compare=sub_rt: x in compare, rt)

        context.setNodePosSize(origState)

        return result

    def pprint(self, indent=''):
        print indent + str(self)
        self._step.pprint(indent + '  ')
        self._rel.pprint(indent + '  ')

    def __str__(self):
        return '<AbbreviatedAbsoluteLocationPath at %x: %s>' % (
            id(self),
            repr(self)
            )

    def __repr__(self):
        return '/%s/%s' % (repr(self._step), repr(self._rel))
        