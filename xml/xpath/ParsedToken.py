########################################################################
#
# File Name:   ParsedToken.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedToken.py.html
#
"""
The base class for all parsed tokens.  Parsed tokens are used to build
a parse tree for future parsing of a XPath path.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import XPath

ignore_keys = [
    '__doc__',
    'YYSTYPEPtr',
    'YYSTYPE',
    'XPathc',
    '__builtins__',
    'cvar',
    'my_XPathparse',
    '__file__',
    '__name__',
    'XPathlval'
    ]

TOKEN_MAP = {}
for k in XPath.__dict__.keys():
    if not k in ignore_keys:
        TOKEN_MAP[XPath.__dict__[k]] = k

class ParsedToken:
    def __init__(self,token):
        self._type = token
        self.literal = None

    def isa(self,token):
        return self._type == token

    def isParsedToken(self,param):
        return isinstance(param, ParsedToken)

    def evaluate(self, context):
        return self.select(context)

    def dump(self, stream):
        stream.write(repr(self))

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self),
            )
    
    def __repr__(self):
        return TOKEN_MAP.get(self._type, 'Unknown(%s)' % str(self._type))
