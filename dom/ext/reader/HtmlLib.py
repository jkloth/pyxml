########################################################################
#
# File Name:            HtmlLib.py
#
# Documentation:        http://docs.4suite.com/4DOM/HtmlLib.py.html
#
# History:
# $Log: HtmlLib.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:50  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.10  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.9  2000/05/24 18:03:39  uogbuji
# Fix bugs and name inconsistencies
# Convert extensions doc to XML
#
# Revision 1.8  2000/05/24 04:05:47  uogbuji
# fixed tab issues
# fixed nasty recursion bug in HtmlLib
#
# Revision 1.7  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.6  2000/05/10 00:51:01  uogbuji
# Resurrect fixes to HTML reader and printer.
#
# Revision 1.5  2000/05/09 03:52:00  molson
# Fixed bug in creting a document
#
# Revision 1.4  2000/05/06 09:12:17  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.3  2000/05/06 05:43:56  jkloth
# fixed import error
#
# Revision 1.2  2000/04/27 19:08:50  jkloth
# fixed imports for xml-sig
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.6  2000/04/19 17:31:51  uogbuji
# Minor fixes to Printer UTF8 handling
# Added Eivind Tagseth's patch for reader/HtmlLib.py
#
# Revision 1.5  2000/03/07 17:47:10  uche
# Fixed bug reports by "Sebastian Jekutsch" <SJekutsch@TRIVIUM.DE>
#
# Revision 1.4  1999/12/24 20:05:01  uche
# Fix nasty HTML bugs
# Add namespace-alias support
# Add some XSLT test files
#
# Revision 1.3  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.2  1999/10/10 08:14:50  uche
# Added a SAX2 driver for reading XML -> DOM.
# Modified XSLT to use the SAX2 driver for its advanced capabilities.
# Added xsl-comment and xsl-copy, along with test harnesses.
# Modified URLs throughout the XSL to match the final version (yay! W3C finally got it right: no version in the bloody namespace, sheesh!)
# Added getNodeType and other basic operations to the node wrappers in XPath
# Added a new node type: NAMESPACE_NODE = 10000
#
# Revision 1.1  1999/09/26 00:14:31  uche
# Added the reader ext module to supersede Builder.  Made the appropriate conversions to other 4Suite components.
#
#
"""
Components for reading HTML files using htmllib.py.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import string
from sgmllib import SGMLParser
from xml.dom.Node import Node
from xml.dom.html import HTML_FORBIDDEN_END, HTML_OPT_END
from xml.dom import implementation


HTML_SINGLE_TAGS =  HTML_FORBIDDEN_END + HTML_OPT_END


class HtmlToDomParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self,1);
        self.stack = []
        self.ownerDoc = None

    def unknown_starttag(self,tag,attrs):
        #push this new element onto the stack
        #Fix the name
        pass
        newElement = self.ownerDoc.createElement(tag)
        #Add any attributes to the tag
        for attr in attrs:
            name,value = attr
            newElement.setAttribute(name,value)
        self.stack.append(newElement)

    def unknown_endtag(self, tag):
        pass
        #Pop the last element off the stack
        oldElement = self.stack[-1]
        tn = string.upper(tag)
        childList = []
                
        while (oldElement.tagName != tn and oldElement.tagName in HTML_SINGLE_TAGS):
            old_children = oldElement.childNodes
            tmpList = old_children[:]
            tmpList.reverse()
            childList = childList + tmpList
            childList.append(oldElement)
            del self.stack[-1]
            oldElement = self.stack[-1]

        #if oldElement.tagName != tn and oldElement.tagName in HTML_SINGLE_TAGS:
        #    raise "Invalid HTML: </" + tag + '>'

        if childList:
            childList.reverse()
            for c in childList:
                oldElement.appendChild(c)

        #Pop last entry
        del self.stack[-1]
        self.stack[-1].appendChild(oldElement)

    def handle_data(self, data):
        t = self.ownerDoc.createTextNode(data)
        self.handle_generic_node(t)

    def handle_comment(self, comment):
        c = self.ownerDoc.createComment(comment)
        self.handle_generic_node(c)

    def handle_generic_node(self, node):
        self.stack[-1].appendChild(node)                        

    def report_unbalanced(self, tag):
        print "Unbalanced tag"

    def toDom(self, st, ownerDoc=None):
        self.ownerDoc = ownerDoc
        if self.ownerDoc == None:
            self.ownerDoc = implementation.createHTMLDocument('')
        #Parse everythin into a DF
        self.stack = [self.ownerDoc.createDocumentFragment()]
        self.feed(st)
        self.close()
        return self.stack[0]


def FromHtmlStream(fp, ownerDocument=None):
    return FromHtml(fp.read(), ownerDocument)


def FromHtmlFile(fileName, ownerDocument=None):
    f = open(fileName,'r')
    rv = FromHtmlStream(f,ownerDocument)
    f.close()
    return rv


def FromHtmlUrl(url, ownerDocument=None):
    f = urllib.urlopen(url)
    rv = FromHtmlStream(f,ownerDocument)
    f.close()
    return rv


def FromHtml(str, ownerDocument=None):
    p = HtmlToDomParser()
    d = p.toDom(str,ownerDocument)

    #d is a DF
    #if ownerDocument != None or DF.childNodes() has a HTML tag put it in a document
    toDoc = None
    if ownerDocument != None:
        toDoc = ownerDocument
    else:
        children = d.childNodes
        for child in children:
            if child.nodeType == Node.ELEMENT_NODE and child.tagName == 'HTML':
                toDoc = p.ownerDoc
                break
    if toDoc:
        #Convert to a document
        for child in d.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and child.tagName == 'HTML':
                newNode = toDoc.importNode(child, 1)
                toDoc.replaceChild(newNode, toDoc.documentElement)
            elif child.nodeType != Node.TEXT_NODE:
                toDoc.appendChild(child)
        d = toDoc
    return d

