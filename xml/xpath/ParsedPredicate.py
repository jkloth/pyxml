########################################################################
#
# File Name:   ParsedPredicate.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedPredicate.py.html
#
"""
A Parsed token that represents a predicate.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import ParsedToken


class ParsedPredicate(ParsedToken.ParsedToken):
    def __init__(self,exp):
        raise Exception('Depreciated: append expression directly')
        ParsedToken.ParsedToken.__init__(self,'PREDICATE')
        if not self.isParsedToken(exp) or not exp.isa('EXPRESSION'):
            raise "Invalid Expression: ", str(exp)
        self._exp = exp

    def evaluate(self, context):
        rt = Conversions.BooleanEvaluate(self._exp, context)
        return rt

    def dump(self,f):
        f.write('[');
        self._exp.dump(f)
        f.write(']');

    def __str__(self):
        return '<Predicate at %s: "%s">' % (
            id(self),
            str(self._exp)
            )

    def __repr__(self):
        return  repr(self._exp)

