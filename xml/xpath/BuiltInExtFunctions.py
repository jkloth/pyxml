########################################################################
#
# File Name:   BuiltInExtFunctions.py
#
# Docs:        http://docs.4suite.com/XPath/BuiltInExtFunctions.py.html
#
"""
4XPath-specific Extension functions
WWW: http://4suite.com/XSLT        e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string, urllib
from xml.dom import Node
from xml.xpath import CoreFunctions, Conversions, FT_EXT_NAMESPACE
from xml.utils import boolean
from xml.dom.Text import Text


def Version(context):
    from Ft.__init__ import __version__
    return __version__


def NodeSet(context, rtf):
    """Convert a result-tree fragment to a node-set"""
    if type(rtf) == type([]):
        return rtf
    if hasattr(rtf,'nodeType') and rtf.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
        node_set = list(rtf.childNodes)
    else:
        node_set = [rtf]
    return node_set


def Match(context, pattern, arg=None):
    """Do a regular expression match against the argument"""
    if not arg:
        arg = context.node
    arg = Conversions.StringValue(arg)
    bool = re.match(pattern, arg) and boolean.true or boolean.false
    return bool


#FIXME: Really only makes sense for XSLT
def SearchRe(context, pattern, arg=None):
    """Do a regular expression search against the argument (i.e. get all matches)"""
    if not arg:
        arg = context.node
    arg = Conversions.StringValue(arg)
    matches = re.findall(pattern, arg)
    proc = context.processor
    matches_nodeset = []
    for groups in matches:
        proc.pushResult()
        proc.writers[-1].startElement('Match', '')
        if type(groups) != type(()):
            groups = (groups,)
        for group in groups:
            proc.writers[-1].startElement('Group', '')
            proc.writers[-1].text(group)
            proc.writers[-1].endElement('Group')
        proc.writers[-1].endElement('Match')
        frag = proc.popResult()
        context.rtfs.append(frag)
        matches_nodeset.append(frag.childNodes[0])
    return matches_nodeset


#FIXME: Really only makes sense for XSLT (in fact, barely makes sense at all)
def Map(context, funcname, *nodesets):
    """
    Apply the function serially over the given node sets.
    In iteration i, the function is passed N parameters
    where N is the number of argument node sets.  Each
    parameter is a node set of size 1, whose node is
    the ith node of the corresponding argument node set.
    The return value is a node set consisting of a series
    of result-tree nodes, each of which is a text node
    whose value is the string value of the result of the
    ith function invocation.
    Warning: this function uses the implied ordering of the node set
    Based on its implementation as a Python list.  But in reality
    There is no reliable ordering of XPath node sets.
    In other words, this function is voodoo.
    """
    (prefix, local) = ExpandQName(funcname, namespaces=context.processorNss)
    func = (g_extFunctions.get(expanded) or
            CoreFunctions.CoreFunctions.get(expanded, None))
    if not func:
        raise Exception('Dynamically invoked function %s not found.'%funcname)
    flist = [f]*len(nodesets)
    lf = lambda x, f, *args: apply(f, args)
    retlist = apply(map, (lf, flist) + nodesets)

    proc = context.processor
    result_nodeset = []
    for ret in retlist:
        proc.pushResult()
        proc.writers[-1].text(Conversions.StringValue(ret))
        frag = proc.popResult()
        context.rtfs.append(frag)
        result_nodeset.append(frag.childNodes[0])
    return result_nodeset


def EscapeUrl(context, url):
    "Escape illegal characters in a URL"
    return urllib.quote(Conversions.StringValue(url))


def BaseUri(context, arg=None):
    """Get the base URI of the argument"""
    if not arg:
        arg = [context.node]
    return arg[0].baseUri


def IsoTime(context):
    import DateTime
    d = DateTime.now()
    return DateTime.ISO.str(d)


def Evaluate(context, expr):
    import xml.xpath
    return xml.xpath.Evaluate(Conversions.StringValue(expr), context=context)


##
## distinct, split, range if_function and find
## were contributed by Lars Marius Garshol.
## Their namespace URI was originally 'http://garshol.priv.no/symbolic/'
## but has been changed to the 4Suite.org NSRef
## so users don't have to declare yet another namespace.
##

def distinct(context, nodeset):
    if type(nodeset) != type([]):
        raise Exception("'distinct' parameter must be of type node-set!")
    
    nodes = {}
    for node in nodeset:
        nodes[Conversions.StringValue(node)] = node

    return nodes.values()

def split(context, arg, delim=None):
    doc = context.node
    while doc.parentNode:
        doc = doc.parentNode
    
    nodeset = []    
    for token in string.split(Conversions.StringValue(arg), delim):
        nodeset.append(doc.createTextNode(token))

    return nodeset

def join(context, nodeset, delim=None):
    comps = map(lambda x: Conversions.StringValue(x), nodeset)
    if delim:
        return string.joinfields(comps, delim)
    else:
        return string.joinfields(comps)

def range(context, lo, hi):
    doc = context.node
    while doc.parentNode:
        doc = doc.parentNode
        
    lo = Conversions.NumberValue(lo)
    hi = Conversions.NumberValue(hi)
    
    nodeset = []    
    for number in xrange(lo, hi):
        nodeset.append(doc.createTextNode(str(number)))

    return nodeset

def if_function(context, cond, v1, v2):
    if Conversions.BooleanValue(cond):
        return v1
    else:
        return v2

def find(context, outer, inner):
    return string.find(Conversions.StringValue(outer), Conversions.StringValue(inner))


ExtFunctions = {
    (FT_EXT_NAMESPACE, 'node-set'): NodeSet,
    (FT_EXT_NAMESPACE, 'match'): Match,
    (FT_EXT_NAMESPACE, 'search-re'): SearchRe,
    (FT_EXT_NAMESPACE, 'base-uri'): BaseUri,
    (FT_EXT_NAMESPACE, 'escape-url'): EscapeUrl,
    (FT_EXT_NAMESPACE, 'iso-time'): IsoTime,
    (FT_EXT_NAMESPACE, 'evaluate'): Evaluate,
    (FT_EXT_NAMESPACE, 'distinct'): distinct,
    (FT_EXT_NAMESPACE, 'split'): split,
    (FT_EXT_NAMESPACE, 'join'): join,
    (FT_EXT_NAMESPACE, 'range'): range,
    (FT_EXT_NAMESPACE, 'if'): if_function,
    (FT_EXT_NAMESPACE, 'find'): find,
    (FT_EXT_NAMESPACE, 'map'): Map,
    (FT_EXT_NAMESPACE, 'version'): Version,
    }

