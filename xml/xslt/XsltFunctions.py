########################################################################
#
# File Name:   XsltFunctions.py
#
# Docs:        http://docs.4suite.com/XSLT/XsltFunctions.py.html
#

"""
WWW: http://4suite.com/XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import cStringIO, os, re, urlparse, urllib
import xml.dom.ext
from xml.dom import Node
from xml.dom.DocumentFragment import DocumentFragment
from xml.xpath import CoreFunctions, Conversions, Util, g_extFunctions
from xml.xslt import XsltException, Error, XSL_NAMESPACE
from xml.xslt import g_extElements
# from Ft.Lib import Uri


#  import os
#  BETA_DOMLETTE = os.environ.get("BETA_DOMLETTE")
#  if BETA_DOMLETTE:
#      from Ft.Lib import cDomlette
#      g_readerClass = cDomlette.RawExpatReader
#      g_domModule = cDomlette
#  else:
#      from Ft.Lib import pDomlette
#      g_readerClass = pDomlette.PyExpatReader
#      g_domModule = pDomlette


def Document(context, object, nodeSet=None):
    result = []

    baseUri = getattr(context.stylesheet, 'baseUri', '')
    #if baseUri: baseUri= baseUri + '/'
    if nodeSet:
        print dir(nodeSet[0])
        baseUri = getattr(nodeSet[0], 'baseUri', baseUri)

    if nodeSet is None:
        if type(object) == type([]):
            for curr_node in object:
                result = result + Document(context, Conversions.StringValue(curr_node),
                                           [curr_node])
        elif object == '':
            result = [context.stylesheet.ownerDocument]
            context.stylesheet.newSource(context.stylesheet.ownerDocument,
                                         context.processor)
            #Util.IndexDocument(context.stylesheet.ownerDocument)
        else:
            try:
                #FIXME: Discard fragments before checking for dupes
                uri = Conversions.StringValue(object)
                if context.documents.has_key(uri):
                    result = context.documents[uri]
                else:
                    try:
                        doc = context.stylesheet._docReader.fromUri(uri, baseUri=baseUri)
                    except:
                        raise
                    #Util.IndexDocument(doc)
                    context.stylesheet.newSource(doc, context.processor)
                    result = [doc]
            except IOError:
                pass
    elif type(nodeSet) == type([]):
        if type(object) == type([]):
            for curr_node in object:
                result = result + Document(
                    context,
                    Conversions.StringValue(curr_node),
                    nodeSet
                    )
        else:
            try:
                uri = Conversions.StringValue(object)
                #FIXME: Discard fragments before checking for dupes
                if context.documents.has_key(uri):
                    result = context.documents[uri]
                else:
                    doc = context.stylesheet._docReader.fromUri(uri, baseUri=baseUri)
                    #Util.IndexDocument(doc)
                    context.stylesheet.newSource(doc, context.processor)
                    result = [doc]
            except IOError:
                pass
    return result


def Key(context, qname, keyList):
    result = []
    name = Util.ExpandQName(Conversions.StringValue(qname),
                            namespaces=context.processorNss)
    if context.stylesheet.keys.has_key(name):
        a_dict = context.stylesheet.keys[name]
        if type(keyList) != type([]):
            keyList = [keyList]
        for key in keyList:
            key = Conversions.StringValue(key)
            result = result + a_dict.get(key, [])
    return result


def Current(context):
    return [context.currentNode]


def UnparsedEntityUri(context, name):
    if hasattr(context.node.ownerDoc, '_unparsedEntities') and context.node.ownerDoc._unparsedEntities.has_key(name):
        return context.node.ownerDoc._unparsedEntities[name]
    return ''


def GenerateId(context, nodeSet=None):
    if nodeSet is not None and type(nodeSet) != type([]):
        raise XsltException(Error.WRONG_ARGUMENT_TYPE)
    if not nodeSet:
        return 'id' + `id(context.node)`
    else:
        node = Util.SortDocOrder(nodeSet)[0]
        return 'id' + `id(node)`
        

def SystemProperty(context, qname):
    split_name = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if split_name[0] == XSL_NAMESPACE:
        if split_name[1] == 'version':
            return 1.0
        if split_name[1] == 'vendor':
            return "Fourthought Inc."
        if split_name[1] == 'vendor-url':
            return "http://4Suite.org"
    if split_name[0] == 'http://namespaces.4suite.org/environmentsystemproperty':
        if os.environ.has_key(name):
            return os.environ[name]
    return ''


def FunctionAvailable(context, qname):
    split_name = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if g_extFunctions.has_key(split_name) or CoreFunctions.CoreFunctions.has_key(split_name):
        return CoreFunctions.True(context)
    else:
        return CoreFunctions.False(context)


def ElementAvailable(context, qname):
    split_name = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if g_extElements.has_key(split_name) or CoreFunctions.CoreFunctions.has_key(split_name):
        return CoreFunctions.True(context)
    else:
        return CoreFunctions.False(context)


def XsltStringValue(object):
    if hasattr(object, 'nodeType') and object.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
        result = ''
        for node in object.childNodes:
            result = result + Conversions.CoreStringValue(node)[1]
        return 1, result
    return 0, None

def XsltNumberValue(object):
    handled, value = XsltStringValue(object)
    if handled:
        return 1, Conversions.NumberValue(value)
    return 0, None

def XsltBooleanValue(object):
    handled, value = XsltStringValue(object)
    if handled:
        return 1, Conversions.BooleanValue(value)
    return 0, None

##0 decimal-separator
##1 grouping-separator
##2 infinity
##3 minus-sign
##4 NaN
##5 percent
##6 per-mille
##7 zero-digit
##8 digit
##9 pattern-separator

def FormatNumber(context, number, formatString, decimalFormatName=None):
    decimal_format = ''
    num = Conversions.NumberValue(number)
    format_string = Conversions.StringValue(formatString)
    if decimalFormatName is not None:
        split_name = Util.ExpandQName(decimalFormatName,
                                      namespaces=context.processorNss)
        decimal_format = context.stylesheet.decimalFormats[split_name]
    else:
        decimal_format = context.stylesheet.decimalFormats['']
    from Ft.Lib import routines
    result = routines.FormatNumber(num, format_string)
    return result


##    format_string = Conversions.StringValue(formatString)
##    fslen = len(format_string)
##    fraction_ix = string.find(format_string, decimal_format[0])
##    fraction_len = fraction_ix - fslen
##    numstr = "%*f"%(fraction_len, Conversions.NumberValue(number))
##    digit_ix = len(numstr) - 1
##    fstr_ix = fslen - 1
##    output = ''
##    done = 0
##    while not done:
##        curr = format_string[fstr_ix]
##        if curr in [decimal_format[0], decimal_format[1], decimal_format[5], decimal_format[6]]:
##            output = output + curr
##        elif curr == decimal_format[8]:
##            output = output + numstr[digit_ix]
##            digit_ix = digit_ix - 1
            
##        fstr_ix = fstr_ix - 1

##    special_chars = decimal_format[0]+decimal_format[1]+decimal_format[3]+decimal_format[5]+decimal_format[6]+decimal_format[7]+decimal_format[8]+decimal_format[9]
##    decimal_format_match = re.match("([^%s]*?)(%s*)(%s+)(%s)(%s*)(%s*)([^%s]*?)"%(special_chars, decimal_format[8], decimal_format[7], decimal_format[0], decimal_format[7], decimal_format[8], special_chars), formatString)
##    width = str(len(decimal_format_match.group(1) + decimal_format_match.group(2) + decimal_format_match.group(3) + decimal_format_match.group(4) + decimal_format_match.group(5)))
##    leading_zero = decimal_format_match.group(1) and '0'
##    decimal = decimal_format_match.group(3) and '.'
##    fract_width = str(len(decimal_format_match.group(4) + decimal_format_match.group(5)))
##    return (decimal_format_match.group(0) + '%' + leading_zero + width + decimal + fract_width + decimal_format_match.group(6))%(num)

Conversions.g_stringConversions.insert(0, XsltStringValue)
Conversions.g_numberConversions.insert(0, XsltNumberValue)
Conversions.g_booleanConversions.insert(0, XsltBooleanValue)

ExtFunctions = {
    ('', 'document'): Document,
    ('', 'key'): Key,
    ('', 'current'): Current,
    ('', 'generate-id'): GenerateId,
    ('', 'system-property'): SystemProperty,
    ('', 'function-available'): FunctionAvailable,
    ('', 'element-available'): ElementAvailable,
    ('', 'string-value'): XsltStringValue,
    ('', 'format-number'): FormatNumber,
    ('', 'unparsed-entity-uri'): UnparsedEntityUri
    }

