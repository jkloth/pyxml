########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4Path/__init__.py.html
#
"""
WWW: http://4suite.org/4XPath         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string


NAMESPACE_NODE = 10000
FT_EXT_NAMESPACE = 'http://namespaces.4suite.org/xpath/extensions'

#Simple trick (thanks Tim Peters) to enable crippled IEEE 754 support until ANSI C (or Python) sorts it all out...
Inf = Inf = 1e300**2
NaN = Inf - Inf

from xml.dom import Node

g_xpathRecognizedNodes = [
        Node.ELEMENT_NODE,
        Node.ATTRIBUTE_NODE,
        Node.TEXT_NODE,
        Node.DOCUMENT_NODE,
        Node.PROCESSING_INSTRUCTION_NODE,
        Node.COMMENT_NODE
        ]

g_extFunctions = {}

import yappsrt
SyntaxException = yappsrt.SyntaxError
InternalException = SyntaxError # not used

class GeneralException:
    def __init__(self, errorCode):
        self.errorCode = errorCode


class Error:
    LEXICAL_ERROR = 1
    SYNTAX_ERROR = 2
    INTERNAL_ERROR = 3
    PROCESSING_ERROR = 4
    NO_CONTEXT_ERROR = 5


def Evaluate(expr, contextNode=None, context=None):
    import pyxpath
    import os
    if os.environ.has_key('EXTMODULES'):
        RegisterExtensionModules(string.split(os.environ["EXTMODULES"], ':'))

    if context:
        con = context
    elif contextNode:
        con = Context.Context(contextNode, 0, 0)
    else:
        raise GeneralException(Error.NO_CONTEXT_ERROR)
    retval = pyxpath.Compile(expr).evaluate(con)
    return retval


def Compile(expr):
    import pyxpath
    return pyxpath.Compile(expr)

def CreateContext(contextNode):
    return Context.Context(contextNode, 0, 0)


def RegisterExtensionModules(moduleNames):
    mod_names = moduleNames[:]
    mods = []
    for mod_name in mod_names:
        if mod_name:
            mod = __import__(mod_name,{},{},['ExtFunctions'])
            if hasattr(mod,'ExtFunctions'):
                g_extFunctions.update(mod.ExtFunctions)
                mods.append(mod)
    return mods


import Context, XPathParser

def Init():
    from xml.xpath import BuiltInExtFunctions
    g_extFunctions.update(BuiltInExtFunctions.ExtFunctions)

Init()

