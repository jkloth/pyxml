########################################################################
#
# File Name:            HtmlLib.py
#
# Documentation:        http://docs.4suite.com/4DOM/HtmlLib.py.html
#
"""
Components for reading HTML files using htmllib.py.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from sgmllib import SGMLParser
from xml.dom import Node
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
        newElement = self.ownerDoc.createElement(tag)
        #Add any attributes to the tag
        for attr in attrs:
            name,value = attr
            newElement.setAttribute(name,value)
        self.stack.append(newElement)

    def unknown_endtag(self, tag):
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


class Reader:
    def __init__(self):
        return

    def fromStream(self, stream, ownerDocument=None):
        p = HtmlToDomParser()
        d = p.toDom(stream.read(), ownerDocument)

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


########################## Deprecated ##############################

def FromHtmlStream(fp, ownerDocument=None):
    return Reader().fromStream(fp, ownerDocument)


def FromHtmlFile(fileName, ownerDocument=None):
    f = open(fileName,'r')
    r = Reader().fromStream(f, ownerDocument)
    f.close()
    return r


def FromHtmlUrl(url, ownerDocument=None):
    f = urllib.urlopen(url)
    r = Reader().fromStream(f, ownerDocument)
    f.close()
    return f


def FromHtml(text, ownerDocument=None):
    import cStringIO
    stream = cStringIO.StringIO(text)
    r = Reader().fromStream(stream, ownerDocument)
    stream.close
    return r

