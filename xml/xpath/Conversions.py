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
from xml.utils import boolean

import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]


def BooleanEvaluate(exp, context):
    rt = exp.evaluate(context)
    return BooleanValue(rt)


def StringValue(object):
#def StringValue(object, context=None):
    #print "StringValue context", context
    #if context:
    #    cache = context.stringValueCache
    #else:
    #    cache = None
    for func in g_stringConversions:
        #handled, result = func(object, cache)
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
    # See bottom of file for conversion functions
    result = _strConversions.get(type(object), _strUnknown)(object)
    return result is not None, result


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


def _strInstance(object):
    if hasattr(object, 'stringValue'):
        return object.stringValue
    if hasattr(object, 'nodeType'):
        node_type = object.nodeType
        if node_type == Node.ELEMENT_NODE:
            # The concatenation of all text descendants
            text_elem_children = filter(lambda x:
                                        x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE, Node.CDATA_SECTION_NODE],
                                        object.childNodes)
            return reduce(lambda x, y:
                          CoreStringValue(x)[1] + CoreStringValue(y)[1],
                          text_elem_children,
                          '')
        if node_type in [Node.ATTRIBUTE_NODE, NAMESPACE_NODE]:
            return object.value
        if node_type in [Node.PROCESSING_INSTRUCTION_NODE, Node.COMMENT_NODE, Node.TEXT_NODE, Node.CDATA_SECTION_NODE]:
            return object.data
        if node_type == Node.DOCUMENT_NODE:
            # Use the String value of the document root
            return StringValue(object.documentElement)
    return None
        
def _strElementInstance(object):
    if hasattr(object, 'stringValue'):
        return object.stringValue
    if object.nodeType == Node.ELEMENT_NODE:
        # The concatenation of all text descendants
        text_elem_children = filter(
            lambda x: x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE, Node.CDATA_SECTION_NODE],
            object.childNodes
            )
        return reduce(lambda x, y:
                      CoreStringValue(x)[1] + CoreStringValue(y)[1],
                      text_elem_children,
                      '')

_strUnknown = lambda x: None

_strConversions = {
    types.StringType : str,
    types.IntType : str,
    types.LongType : str,
    types.FloatType : lambda x: x is NaN and 'NaN' or '%g' % x,
    boolean.BooleanType : str,
    types.InstanceType : _strInstance,
    types.ListType : lambda x: x and _strConversions[type(x[0])](x[0]) or '',
}

try:
    from Ft.Lib import cDomlettec
    _strConversions.update({
        cDomlettec.DocumentType : lambda x: _strDocumentInstance(x.documentElement),
        cDomlettec.ElementType : _strElementInstance,
        cDomlettec.TextType : lambda x: x.data,
        cDomlettec.CommentType : lambda x: x.data,
        cDomlettec.ProcessingInstructionType : lambda x: x.data,
        cDomlettec.AttrType : lambda x: x.value,
        })
except:
    pass

if hasattr(types, 'UnicodeType'):
    _strConversions[types.UnicodeType] = unicode

