########################################################################
#
# File Name:   CoreFunctions.py
#
# Docs:        http://docs.4suite.com/XPATH/CoreFunctions.py.html
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
from xml.xpath import Util, Conversions
from xml.xpath import NAMESPACE_NODE
from xml.utils import boolean

class Types:
    NumberType = 0
    StringType = 1
    BooleanType = 2
    NodeSetType = 3
    ObjectType = 4

import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]

### Node Set Functions ###

def Last(context):
    """Function: <number> last()"""
    return context.size


def Position(context):
    """Function: <number> position()"""
    return context.position


def Count(context, nodeSet):
    """Function: <number> count(<node-set>)"""
    if type(nodeSet) != type([]):
        raise Exception("Count param must be a node set")
    return len(nodeSet)


def Id(context, object):
    """Function: <node-set> id(<object>)"""
    id_list = []
    if type(object) != type([]):
        st = Conversions.StringValue(object)
        id_list = string.split(st)
    else:
        for n in object:
            id_list.append(Conversions.StringValue(n))
    rt = []
    for i in id_list:
        r = _FindIds(context.node.ownerDocument.documentElement, i, [])
        if len(r) > 1:
            raise Exception("ID must be unique")
        elif len(r) == 1:
            rt.append(r[0].ownerElement)
    return rt


def _FindIds(node, name, result):
    attrs = node.attributes
    idattr = attrs.get(('', 'id')) or attrs.get(('', 'ID'))
    idattr and idattr.value == name and result.append(idattr)
    elements = filter(lambda node: node.nodeType == Node.ELEMENT_NODE,
                      node.childNodes)
    for node in elements:
        _FindIds(node, name, result)
    return result


def LocalName(context, nodeSet=None):
    """Function: <string> local-name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise Exception("local-name() parameter must be a node set")
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None or en.localName == None:
        return ''
    return en.localName


def NamespaceUri(context, nodeSet=None):
    """Function: <string> namespace-uri(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise Exception("namespace-uri() parameter must be a node set")
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None or en.namespaceURI == None:
        return ''
    return en.namespaceURI


def Name(context, nodeSet=None):
    """Function: <string> name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise Exception("name() parameter must be a node set")
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None:
        return ''
    return en.qName


### String Functions ###

def String(context, object=None):
    """Function: <string> string(<object>?)"""
    if type(object) in g_stringTypes:
        return object
    if object is None:
        object = [context.node]
    return Conversions.StringValue(object)


def Concat(context, *args):
    """Function: <string> concat(<string>, <string>, ...)"""
    return reduce(lambda a,b: a + Conversions.StringValue(b), args, '')


def StartsWith(context, outer, inner):
    """Function: <string> starts-with(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    return outer[:len(inner)] == inner and boolean.true or boolean.false


def Contains(context, outer, inner):
    """Function: <string> contains(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    if len(inner) == 1:
        return inner in outer and boolean.true or boolean.false
    else:
        return string.find(outer, inner) != -1 and boolean.true or boolean.false


def SubstringBefore(context, outer, inner):
    """Function: <string> substring-before(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    index = string.find(outer, inner)
    if index == -1:
        return ''
    return outer[:index]


def SubstringAfter(context, outer, inner):
    """Function: <string> substring-after(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    index = string.find(outer, inner)
    if index == -1:
        return ''
    return outer[index+len(inner):]


def Substring(context, st, start, end=None):
    """Function: <string> substring(<string>, <number>, <number>?)"""
    st = Conversions.StringValue(st)
    start = Conversions.NumberValue(start)
    if start is NaN:
        return ''
    start = int(round(start))
    start = start > 1 and start - 1 or 0

    if end is None:
        return st[start:]
    end = Conversions.NumberValue(end)
    if start is NaN:
        return st[start:]
    end = int(round(end))
    return st[start:start+end]


def StringLength(context, st=None):
    """Function: <number> string-length(<string>?)"""
    if st is None:
        st = context.node
    return len(Conversions.StringValue(st))


def Normalize(context, st=None):
    """Function: <string> normalize-space(<string>?)"""
    if st is None:
        st = context.node
    st = Conversions.StringValue(st)
    return string.join(string.split(st))


def Translate(context, source, fromChars, toChars):
    """Function: <string> translate(<string>, <string>, <string>)"""
    remove_chars = ''
    source = Conversions.StringValue(source)
    fromChars = Conversions.StringValue(fromChars)
    toChars = Conversions.StringValue(toChars)
    if len(fromChars) > len(toChars):
        remove_chars = fromChars[len(toChars):]
        fromChars = fromChars[:len(toChars)]
    translator = string.maketrans(fromChars, toChars)
    result = string.translate(source, translator)
    for char in remove_chars:
        result = string.replace(result, char, '')
    return result

### Boolean Functions ###

def _Boolean(context, object):
    """Function: <boolean> boolean(<object>)"""
    return Conversions.BooleanValue(object)


def Not(context, object):
    """Function: <boolean> not(<boolean>)"""
    return (not Conversions.BooleanValue(object) and boolean.true) or boolean.false


def True(context):
    """Function: <boolean> true()"""
    return boolean.true


def False(context):
    """Function: <boolean> false()"""
    return boolean.false


def Lang(context, lang):
    """Function: <boolean> lang(<string>)"""
    lang = string.upper(Conversions.StringValue(lang))
    no_suffix = string.find(lang, '-') == -1
    node = context.node
    while node:
        value = filter(lambda x:x.name == 'xml:lang' and x.value, node.attributes)
        if value:
            # See if there is a suffix
            if no_suffix:
                index = string.find(value[0], '-')
                if index != -1:
                    value = value[:index]
            value = string.upper(value)
            return value == lang and boolean.true or boolean.false
        node = node.nodeType == Node.ATTRIBUTE_NODE and node.ownerElement or node.parentNode
    return boolean.false

### Number Functions ###

def Number(context, object=None):
    """Function: <number> number(<object>?)"""
    if object is None:
        object = [context.node]
    return Conversions.NumberValue(object)


def Sum(context, nodeSet):
    """Function: <number> sum(<node-set>)"""
    nns = map(lambda x: Conversions.NumberValue(x), nodeSet)
    return reduce(lambda x,y: x+y, nns, 0)


def Floor(context, number):
    """Function: <number> floor(<number>)"""
    if type(number) in g_stringTypes:
        number = string.atof(number)
    if int(number) == number:
        return number
    elif number < 0:
        return int(number) - 1
    else:
        return int(number)


def Ceiling(context, number):
    """Function: <number> ceiling(<number>)"""
    if type(number) in g_stringTypes:
        number = string.atof(number)
    if int(number) == number:
        return number
    elif number > 0:
        return int(number) + 1
    else:
        return int(number)


def Round(context, number):
    """Function: <number> round(<number>)"""
    number = Conversions.NumberValue(number)
    return round(number, 0)

### Helper Functions ###

def ExpandedName(node):
    """Get the expanded name of any object"""
    if hasattr(node, 'nodeType') and node.nodeType in [Node.ELEMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE, Node.ATTRIBUTE_NODE, NAMESPACE_NODE]:
        return ExpandedNameWrapper.ExpandedNameWrapper(node)
    return None


### Function Mappings ###

CoreFunctions = {
    ('', 'last'): Last,
    ('', 'position'): Position,
    ('', 'count'): Count,
    ('', 'id'): Id,
    ('', 'local-name'): LocalName,
    ('', 'namespace-uri'): NamespaceUri,
    ('', 'name'): Name,
    ('', 'string'): String,
    ('', 'concat'): Concat,
    ('', 'starts-with'): StartsWith,
    ('', 'contains'): Contains,
    ('', 'substring-before'): SubstringBefore,
    ('', 'substring-after'): SubstringAfter,
    ('', 'substring'): Substring,
    ('', 'string-length'): StringLength,
    ('', 'normalize-space'): Normalize,
    ('', 'translate'): Translate,
    ('', 'boolean'): _Boolean,
    ('', 'not'): Not,
    ('', 'true'): True,
    ('', 'false'): False,
    ('', 'lang'): Lang,
    ('', 'number'): Number,
    ('', 'sum'): Sum,
    ('', 'floor'): Floor,
    ('', 'ceiling'): Ceiling,
    ('', 'round'): Round,
    ('', 'expanded-name'): ExpandedName
    }

Args = {
    Substring : (Types.StringType, [Types.StringType, Types.StringType]),
    }
