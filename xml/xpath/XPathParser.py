########################################################################
#
# File Name:   XPathParser.py
#
# Docs:        http://docs.4suite.com/XPATH/XPathParser.py.html
#
"""

The interface between the yacc parser and python.  this class creates a parsed tree from yacc events.

WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000, 2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import xml.xpath
from xml.xpath import XPath
import sys, traceback

G_TEST_ERROR = 0

from xml.xpath import ParsedToken

p = ParsedToken.ParsedToken('')
def isParsedToken(param):
    return p.isParsedToken(param)


class XPathParser:
    def parseExpression(self, st):
        from xml.xpath import pyxpath
        return pyxpath.parser.parseExpr(st)

if __name__ == '__main__':
    import XPathParserBase
    import sys
    if len(sys.argv) > 1:
        expr = sys.argv[1]
    else:
        expr = raw_input(">>> ")
    parser = XPathParser()
    try:
        result = parser.parseExpression(expr)
        result.pprint()
    except XPathParserBase.InternalException, e:
        XPathParserBase.PrintInternalException(e)
    except XPathParserBase.SyntaxException, e:
        XPathParserBase.PrintSyntaxException(e)
