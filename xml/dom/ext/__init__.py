########################################################################
#
# File Name:            __init__.py
#
# Documentation:        http://docs.4suite.com/4DOM/__init__.py.html
#
# History:
# $Log: __init__.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.11  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.10  2000/05/24 18:03:39  uogbuji
# Fix bugs and name inconsistencies
# Convert extensions doc to XML
#
# Revision 1.9  2000/05/24 04:05:47  uogbuji
# fixed tab issues
# fixed nasty recursion bug in HtmlLib
#
# Revision 1.8  2000/05/14 01:56:46  uogbuji
# Fix XPath parser problems
# Fix ft:node-set
# General bug-fixes
#
# Revision 1.7  2000/05/11 22:58:44  uogbuji
# iVarious bug-fixes
# Update borrowed to new imports
#
# Revision 1.6  2000/05/10 01:54:49  uogbuji
# repaired indentation
#
# Revision 1.5  2000/05/10 00:51:00  uogbuji
# Resurrect fixes to HTML reader and printer.
#
# Revision 1.4  2000/05/06 03:14:05  molson
# Fixed import errors
#
# Revision 1.3  2000/05/04 00:35:53  pweinstein
# Changing Ft.Dom.Html to xml.dom.html
#
# Revision 1.2  2000/05/02 04:30:26  jkloth
# Minor bug fixes
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.52  2000/04/19 03:59:44  uogbuji
# A flurry, plethora, profusion, plurality and parade of changes
# Fix minor bugs in Sax, restored support for provided documents to Sax2
# Bug-fixes to translate, etca in XPath
# Bug-fixes to stripping, HTML printing, etc in DOM
# Add node-set and match extension functions
# Split Processor into processor and writer classes
# Implement SaxWriter (similar to previous) and new TextWriter
# Implement disable-output-escaping
# Add many tests to suite
#
# Revision 1.51  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.50  2000/02/18 16:23:08  uche
# More HTML white-space fixes
# Implemented xsl:number
# bug-fixes
#
# Revision 1.49  2000/02/17 15:02:28  uche
# Fix whitespace issues in printer.
#
# Revision 1.48  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.47  1999/12/24 20:05:01  uche
# Fix nasty HTML bugs
# Add namespace-alias support
# Add some XSLT test files
#
# Revision 1.46  1999/12/18 22:54:51  uche
# Fix Namespaces to Match DOM Level 2 spec.
# Bug-fixes.
#
# Revision 1.45  1999/12/16 23:16:37  uche
# Fix erroneous stripping in StripXml
# Remove print statements
# Allow StripXml to handle namespaces properly
#
# Revision 1.44  1999/12/16 22:42:03  uche
# Various bug-fixes
# Renamed Process.py according to our custom for exes.
#
# Revision 1.43  1999/12/15 17:32:10  uche
# Many bug-fixes.
#
# Revision 1.42  1999/12/15 07:54:14  molson
# Fixed minor bugs
#
# Revision 1.41  1999/12/07 07:39:58  molson
# Added a rudimentery GetAllNS
#
# Revision 1.40  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.39  1999/11/19 01:59:51  molson
# Fixed Release node
#
# Revision 1.38  1999/11/19 01:32:41  uche
# Python/DOM binding changes.
#
# Revision 1.37  1999/11/18 09:30:02  uche
# Python/DOM binding update.
#
# Revision 1.36  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.35  1999/09/10 02:12:19  uche
# Added TreeWalker implementation.
# Fixes to NodeIterator (runs all the way through the test suite now)
#
# Revision 1.34  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.33  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


"""Some Helper functions: 4DOM-specific Extensions to the DOM"""

import sys,string

import xml.dom
from xml.dom.Node import Node
from xml.dom.NodeIterator import NodeIterator
from xml.dom.NodeFilter import NodeFilter
from xml.dom import XML_NAMESPACE
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE

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


def Print(root, stream=sys.stdout):
    if not isinstance(root, Node):
        return
    from xml.dom.ext import Printer
    visitor = Printer.PrintVisitor()
    st = Printer.PrintWalker(visitor, root).run()
    stream.write(st)
    return


def PrettyPrint(
        root,
        stream=sys.stdout,
        indent='  ',
        width=80,
        preserveElements=None
    ):
    if not isinstance(root, Node):
        return
    from xml.dom.ext import Printer
    preserveElements = preserveElements or []
    if root.ownerDocument.isHtml():
        #We don't want to insert any whitespace into HTML inline elements
        preserveElements = preserveElements + HTML_4_TRANSITIONAL_INLINE
    visitor = Printer.PrettyPrintVisitor(
        indent,
        width,
        preserveElements
        )
    stream.write(Printer.PrintWalker(visitor, root).run())
    return


def ReleaseNode(node):
    cn = node.childNodes[:]
    for child in cn:
        if child.nodeType == Node.ELEMENT_NODE:
            ReleaseNode(child)
        node.removeChild(child)

    if node.nodeType == Node.ELEMENT_NODE:
        for attr in node.attributes:
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
        for attr in node.attributes:
            if attr.namespaceURI:
                nss[attr.prefix] = attr.namespaceURI
            else:
                if attr.prefix == 'xmlns':
                    nss[attr.localName] = attr.value
                if not attr.prefix and attr.localName == 'xmlns':
                    nss[''] = attr.value
    if node.parentNode:
        #Inner NS/Prefix mappings take precedence over outer ones
        parent_nss = GetAllNs(node.parentNode)
        parent_nss.update(nss)
        nss = parent_nss
    return nss


def SplitQName(qname):
    name_parts = string.splitfields(qname, ':')
    if len(name_parts) == 1:
        return ('', name_parts[0])
    elif len(name_parts) == 2:
        return (name_parts[0], name_parts[1])
    else:
        return ('', string.joinfields(name_parts, ':'))

