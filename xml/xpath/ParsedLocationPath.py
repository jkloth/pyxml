########################################################################
#
# File Name:   ParsedLocationPath.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedLocationPath.py.html
#
"""
The top level parsed token in a parsed tree.  Can also be contained in a PathExpr.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""
import sys

from xml.xpath import ParsedToken

class ParsedLocationPath(ParsedToken.ParsedToken):
    def __init__(self,path):
        ParsedToken.ParsedToken.__init__(self,'LOCATION_PATH')
        if (not self.isParsedToken(path)
            and not (param.isa('RELATIVE_LOCATION_PATH')
                     or param.isa('ABSOLUTE_LOCATION_PATH'))):
            raise "Invalid parameter for location path ",str(param)
        self.__path = path

    def select(self, context):
        """Select a set of nodes from the list of steps"""
        #Should have no context list
        
        origState = context.copyNodePosSize()
        context.setNodePosSize((context.node,1,1))
        rt = self.__path.select(context)
        context.setNodePosSize(origState)
        return rt

    def dump(self,f = sys.stdout):
        self.__path.dump(f)
        f.write('\n')

    def __str__(self):
        return '<LocationPath at %s: "%s">' % (
            id(self),
            str(self.__path)
            )
    def __repr__(self):
        return repr(self.__path)
