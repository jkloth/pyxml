########################################################################
#
# File Name:   Conversions.py
#
# Docs:        http://docs.4suite.com/XPATH/Conversions.py.html
#
"""
The implementation of all of the core functions for the XPath spec.
WWW: http://4suite.com/XPATH        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, cStringIO

from xml.dom import Node
from xml.xpath import ExpandedNameWrapper
from xml.xpath import NamespaceNode
from xml.xpath import NaN, Inf
from xml.xpath import Util
from xml.xpath import NAMESPACE_NODE
from xml.xpath import boolean


import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]


def BooleanEvaluate(exp, context):
    rt = exp.evaluate(context)
    return BooleanValue(rt)


def StringValue(object):
    for func in g_stringConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def BooleanValue(object):
    if boolean.IsBooleanType(object):
        return object
    elif type(object) in [type(1), type(2.3), type(4L)]:
        if str(object) == 'nan':
            return boolean.false
        return boolean.BooleanValue(object)
    elif type(object) == type(''):
        return boolean.BooleanValue(object)
    for func in g_booleanConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def NumberValue(object):
    for func in g_numberConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def NodeSetValue(object):
    for func in g_nodeSetConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def CoreStringValue(object):
    """Get the string value of any object"""
    object_type = type(object)
    if object_type in g_stringTypes:
        return 1, object
    elif object_type in [types.IntType, types.LongType]:
        return 1, `object`
    elif object_type == types.FloatType:
        if str(object) == 'nan':
            return 1,'NaN'
        return 1, "%g"%(object)
    elif boolean.IsBooleanType(object):
        return 1, str(object)
    elif hasattr(object, 'nodeType'):
        node_type = object.nodeType
        if node_type == Node.ELEMENT_NODE:
            #The concatenation of all text descendants
            text_elem_children = filter(lambda x: x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE], object.childNodes)
            return 1, reduce(lambda x, y: CoreStringValue(x)[1] + CoreStringValue(y)[1], text_elem_children, '')
        elif node_type == Node.ATTRIBUTE_NODE:
            return 1, object.value
        elif node_type in [Node.PROCESSING_INSTRUCTION_NODE, Node.COMMENT_NODE, Node.TEXT_NODE]:
            return 1, object.data
        elif node_type == Node.DOCUMENT_NODE:
            #Use the String value of the document root
            return 1, StringValue(object.documentElement)
##        elif node_type == Node.DOCUMENT_FRAGMENT_NODE:
##            #The concatenation of all descendants
##            return 1, reduce(lambda x, y: StringValue(x) + StringValue(y), object.childNodes, '')
        elif node_type == NAMESPACE_NODE:
            return 1, object.value
    elif object_type == types.ListType:
        return 1, (object and CoreStringValue(object[0])[1] or '')
    # Don't know what it is
    return 0, None


def CoreNumberValue(object):
    """Get the number value of any object"""
    if type(object) in [type(1), type(2.3), type(4L)]:
        return 1, object
    elif boolean.IsBooleanType(object):
        return 1, int(object)
    #FIXME: This can probably be optimized
    object = StringValue(object)
    try:
        object = float(object)
    except:
        #Many platforms seem to have a problem with strtod() and NaN: reported on Windows and FreeBSD
        #object = float('NaN')
        if object == '':
            object = 0
        else:
            object = NaN
    return 1, object


g_seqTypes = [type([])] + g_stringTypes
def CoreBooleanValue(object):
    """Get the boolean value of any object"""
    if boolean.IsBooleanType(object):
        return 1, object
    elif type(object) in [type(1), type(2.3), type(4L)]:
        if str(object) == 'nan':
            return 1, boolean.false
        return 1, boolean.BooleanValue(object)
    elif type(object) in g_seqTypes:
        return 1, (len(object) and boolean.true or boolean.false)
    object = StringValue(object)
    return 1, (object and boolean.true or boolean.false)


g_stringConversions = [CoreStringValue]
g_numberConversions = [CoreNumberValue]
g_booleanConversions = [CoreBooleanValue]
#g_nodeSetConversions = [CoreNodeSetValue]
