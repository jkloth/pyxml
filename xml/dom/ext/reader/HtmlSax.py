########################################################################
#
# File Name:            HtmlSax.py
#
# Documentation:        http://docs.4suite.com/4DOM/HtmlSax.py.html
#
#
"""
Components for reading HTML files from a SAX-like producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, string, cStringIO
import xml.dom.ext
from xml.dom import Entity, DocumentType, Document
from xml.dom import DocumentType, Document
from xml.dom.Node import Node
from xml.dom import implementation


class HtmlDomGenerator:
    def __init__(self, doc=None, keepAllWs=0):
        """
        If None is passed in as the doc, set up an empty document to act
        as owner and also add all elements to this document
        """
        if doc == None:
            self.__ownerDoc = implementation.createHTMLDocument('')
            de = self.__ownerDoc.documentElement
            self.__ownerDoc.removeChild(de)
            xml.dom.ext.ReleaseNode(de)
            self.__rootNode = self.__ownerDoc
        else:
            self.__ownerDoc = doc
            #Create a docfrag to hold all the generated nodes.
            self.__rootNode = self.__ownerDoc.createDocumentFragment()

        #Set up the stack which keeps track of the nesting of DOM nodes.
        self.__nodeStack = []
        self.__nodeStack.append(self.__rootNode)
        self.__keepAllWs = keepAllWs
        self.__currText = ''

    def getRootNode(self):
        self.__completeTextNode()
        return self.__rootNode

    def __completeTextNode(self):
        if self.__currText:
            new_text = self.__ownerDoc.createTextNode(self.__currText)
            self.__nodeStack[-1].appendChild(new_text)
            self.__currText = ''

    #Overridden DocumentHandler methods
    def startElement(self, name, attribs):
        self.__completeTextNode()
        new_element = self.__ownerDoc.createElement(name)

        for curr_attrib_key in attribs.keys():
            new_element.setAttribute(curr_attrib_key, attribs[curr_attrib_key])
        self.__nodeStack.append(new_element)

    def endElement(self, name):
        self.__completeTextNode()
        new_element = self.__nodeStack[-1]
        del self.__nodeStack[-1]
        self.__nodeStack[-1].appendChild(new_element)

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        Remember that a Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self.__keepAllWs and self.__nodeStack[-1].nodeType !=  Node.DOCUMENT_NODE:
            self.__currText = self.__currText + ch[start:start+length]

    def characters(self, ch, start, length):
        self.__currText = self.__currText + ch[start:start+length]


    #Overridden ErrorHandler methods
    #def warning(self, exception):
    #   raise exception

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception


