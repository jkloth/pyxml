########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4DOM/__init__.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

"""Some Helper functions: 4DOM-specific Extensions to the DOM"""

import sys,string

import xml.dom
from xml.dom import Node
from xml.dom.NodeIterator import NodeIterator
from xml.dom.NodeFilter import NodeFilter
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE
import re

NodeTypeDict = {
    Node.ELEMENT_NODE : "Element",
    Node.ATTRIBUTE_NODE : "Attr",
    Node.TEXT_NODE : "Text",
    Node.CDATA_SECTION_NODE : "CDATASection",
    Node.ENTITY_REFERENCE_NODE : "EntityReference",
    Node.ENTITY_NODE : "Entity",
    Node.PROCESSING_INSTRUCTION_NODE : "ProcessingInstruction",
    Node.COMMENT_NODE : "Comment",
    Node.DOCUMENT_NODE : "Document",
    Node.DOCUMENT_TYPE_NODE : "DocumentType",
    Node.DOCUMENT_FRAGMENT_NODE : "DocumentFragment",
    Node.NOTATION_NODE : "Notation"
    }


def NodeTypeToClassName(nodeType):
    return NodeTypeDict[nodeType]


def Print(root, stream=sys.stdout, encoding='UTF-8'):
    if not hasattr(root, "nodeType"):
        return
    from xml.dom.ext import Printer
    nss_hints = SeekNss(root)
    visitor = Printer.PrintVisitor(stream, encoding, nss_hints)
    Printer.PrintWalker(visitor, root).run()
    return


def PrettyPrint(root, stream=sys.stdout, encoding='UTF-8', indent='  ',
                width=80, preserveElements=None):
    if not hasattr(root, "nodeType"):
        return
    from xml.dom.ext import Printer
    nss_hints = SeekNss(root)
    preserveElements = preserveElements or []
    if hasattr(root.ownerDocument,'isHtml') and root.ownerDocument.isHtml():
        #We don't want to insert any whitespace into HTML inline elements
        preserveElements = preserveElements + HTML_4_TRANSITIONAL_INLINE
    visitor = Printer.PrettyPrintVisitor(stream, encoding, indent, width,
                                         preserveElements, nss_hints)
    Printer.PrintWalker(visitor, root).run()
    stream.write('\n')
    return


def XHtmlPrettyPrint(root,stream=sys.stdout, encoding='UTF-8',indent=' ',newLine='\n'):
    if not hasattr(root, "nodeType"):
        return
    from xml.dom.ext import XHtmlPrinter

    visitor = XHtmlPrinter.XHtmlPrintVisitor(stream, encoding, indent, newLine)
    Printer.PrintWalker(visitor, root).run()
    stream.write(newLine)
    return

def XHtmlPrint(root,stream=sys.stdout, encoding='UTF-8'):
    XHtmlPrettyPrint(root,stream,encoding,'','')
    

def ReleaseNode(node):
    cn = node.childNodes[:]
    for child in cn:
        if child.nodeType == Node.ELEMENT_NODE:
            ReleaseNode(child)
        node.removeChild(child)

    if node.nodeType == Node.ELEMENT_NODE:
        for ctr in range(node.attributes.length):
            attr = node.attributes.item(0)
            node.removeAttributeNode(attr)
            ReleaseNode(attr)


def StripHtml(startNode, preserveElements=None):
    '''
    Remove all text nodes in a given tree that do not have at least one
    non-whitespace character, taking into account special HTML elements
    '''
    preserveElements = preserveElements or []
    preserveElements = preserveElements + HTML_4_TRANSITIONAL_INLINE
    remove_list = []
    snit = startNode.ownerDocument.createNodeIterator(startNode, NodeFilter.SHOW_TEXT, None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #first of all make sure it is not inside one of the preserve_elements
        ancestor = curr_node
        while ancestor != startNode:
            if ancestor.nodeType == Node.ELEMENT_NODE:
                if ancestor.nodeName in preserveElements:
                    break
                ancestor = ancestor.parentNode
            else:
                if not string.strip(curr_node.data):
                    remove_list.append(curr_node)
                ancestor = ancestor.parentNode
        curr_node = snit.nextNode()
    for node_to_remove in remove_list:
        node_to_remove.parentNode.removeChild(node_to_remove)
    return startNode


def StripXml(startNode, preserveElements=None):
    '''
    Remove all text nodes in a given tree that do not have at least one
    non-whitespace character, taking into account xml:space
    '''
    preserveElements = preserveElements or []
    remove_list = []
    snit = startNode.ownerDocument.createNodeIterator(startNode, NodeFilter.SHOW_TEXT, None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #first of all make sure it is not inside xml:space='preserve'
        if XmlSpaceState(curr_node) != 'preserve':
            if not string.strip(curr_node.data):
                #also make sure it is not inside one of the preserve elements
                ancestor = curr_node
                while ancestor != startNode:
                    if ancestor.nodeType == Node.ELEMENT_NODE:
                        if ancestor.localName in preserveElements or (ancestor.namespaceURI, ancestor.localName) in preserveElements:
                            break
                    ancestor = ancestor.parentNode
                else:
                    remove_list.append(curr_node)
                    ancestor = ancestor.parentNode
        curr_node = snit.nextNode()
    for node_to_remove in remove_list:
        node_to_remove.parentNode.removeChild(node_to_remove)
    return startNode


def GetElementById(startNode, targetId):
    '''
    Return the element in the given tree with an ID attribute of the given
    value
    '''
    result = None
    snit = startNode.ownerDocument.createNodeIterator(startNode, NodeIterator.SHOW_ELEMENT, None, 0)
    curr_node = snit.nextNode()
    while not result and curr_node:
        attrs = curr_node.attributes
        if attrs.has_key("ID") and attrs["ID"] == target_id:
            result = curr_node
        curr_node = snit.nextNode()
    return result


def XmlSpaceState(node):
    '''
    Return the valid value of the xml:space attribute currently in effect
    '''
    valid_values = ['', 'preserve', 'default']
    xml_space_found = 0
    root_reached = 0
    xml_space_state = ''
    while not(xml_space_state or root_reached):
        if node.nodeType == Node.ELEMENT_NODE:
            xml_space_state = node.getAttributeNS(xml.dom.XML_NAMESPACE, 'space')
            if xml_space_state not in valid_values: xml_space_state = ''
        parent_node = node.parentNode
        if not (parent_node and parent_node.nodeType == Node.ELEMENT_NODE):
            root_reached = 1
        node = parent_node
    return xml_space_state


def GetAllNs(node):
    #The xml namespace is implicit
    nss = {'xml': XML_NAMESPACE}
    if node.nodeType == Node.ATTRIBUTE_NODE and node.ownerElement:
        return GetAllNs(node.ownerElement)
    if node.nodeType == Node.ELEMENT_NODE:
        if node.namespaceURI:
            nss[node.prefix] = node.namespaceURI
        for attr in node.attributes.values():
            if attr.namespaceURI == XMLNS_NAMESPACE:
                nss[attr.localName] = attr.value
            elif attr.namespaceURI:
                nss[attr.prefix] = attr.namespaceURI
    if node.parentNode:
        #Inner NS/Prefix mappings take precedence over outer ones
        parent_nss = GetAllNs(node.parentNode)
        parent_nss.update(nss)
        nss = parent_nss
    return nss


#FIXME: this dict is a small memory leak: a splay tree that rotates out
#out of the tree would be perfect.
#g_splitNames = {}
def SplitQName(qname):
    """
    Input a QName according to XML Namespaces 1.0
    http://www.w3.org/TR/REC-xml-names
    Return the name parts according to the spec
    In the case of namespace declarations the tuple returned
    is (prefix, 'xmlns')
    Note that this won't hurt users since prefixes and local parts starting
    with "xml" are reserved, but it makes ns-aware builders easier to write
    """
    #sName = g_splitNames.get(qname)
    sName = None
    if sName == None:
        index = string.find(qname, ':')
        if index == -1:
            #Note: we could gain a tad more performance by interning 'xmlns'
            if qname == 'xmlns':
                sName = ('', 'xmlns')
            else:
                sName = ('', qname)
        else:
            (part1, part2) = (qname[:index], qname[index+1:])
            if part1 == 'xmlns':
                sName = (part2, 'xmlns')
            else:
                sName = (part1, part2)
        #g_splitNames[qname] = sName
    return sName


def SeekNss(node, nss=None):
    '''traverses the tree to seek an approximate set of defined namespaces'''
    nss = nss or {}
    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.namespaceURI:
                nss[child.prefix] = child.namespaceURI
            for attr in child.attributes.values():
                if attr.namespaceURI == XMLNS_NAMESPACE:
                    nss[attr.localName] = attr.value
            SeekNss(child, nss)
    return nss

