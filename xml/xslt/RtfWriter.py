########################################################################
#
# File Name:            RtfWriter.py
#
# Documentation:        http://docs.4suite.com/4XSLT/RtfWriter.py.html
#

"""
A special, simple writer for capturing result-tree fragments
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, os
from xml.xslt import XSL_NAMESPACE
from xml.xpath import Util
try:
    from Ft.Lib import pDomlette
    createElement = pDomlette.Element
    createAttribute = pDomlette.Attribute
    def createProcessingInstruction(doc, target, data):
        pi = pDomlette.ProcessingInstruction(doc)
        pi.target = target
        pi.data = data
        return pi
    def createComment(doc, data):
        comment = pDomlette.Comment(doc)
        comment.data = data
        return comment

except ImportError:
    from xml.dom import minidom
    def createElement(doc, namespace, localName, prefix):
        if prefix:
            qname = prefix+':'+localName
        else:
            qname = localName
        e = minidom.Element(qname, namespace, prefix, localName)
        e.ownerDoc = doc
        return e
    def createAttribute(doc, namespace, localName, prefix):
        if prefix:
            qname = prefix+':'+localName
        else:
            qname = localName
        return doc.createAttributeNS(namespace, qname)
    def createProcessingInstruction(doc, target, data):
        return doc.createProcessingInstruction(target,data)
    def createComment(doc, data):
        return doc.createComment(data)

from xml.dom.ext import SplitQName
from xml.dom import Node, XMLNS_NAMESPACE

class RtfWriter:
    def __init__(self, outputParams, ownerDoc):
        self.__ownerDoc = ownerDoc
        self.__root = ownerDoc.createDocumentFragment()
        self.__nodeStack = [self.__root]
        self.__currElement = None
        self.__outputParams = outputParams

    def getResult(self):
        return self.__root

    def startElement(self, name, namespace='', extraNss=None):
        extraNss = extraNss or {}
        prefix, localName = SplitQName(name)
        new_element = createElement(self.__ownerDoc, namespace,
                                    localName, prefix)
        self.__nodeStack.append(new_element)
        for prefix in extraNss.keys():
            if prefix:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns:'+prefix,
                                           extraNss[prefix])
            else:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns',
                                           extraNss[prefix])
        return

    def endElement(self, name):
        new_element = self.__nodeStack[-1]
        del self.__nodeStack[-1]
        self.__nodeStack[-1].appendChild(new_element)
        return

    def text(self, text, escapeOutput=1):
        new_text = self.__ownerDoc.createTextNode(text)
        new_text.data = text
        self.__nodeStack[-1].appendChild(new_text)
        return

    def attribute(self, name, value, namespace=''):
        prefix, localName = SplitQName(name)
        attr = createAttribute(self.__ownerDoc, namespace, localName,
                               prefix)
        attr.value = value
        if self.__nodeStack[-1].nodeType == Node.ELEMENT_NODE:
            self.__nodeStack[-1].attributes[(namespace, localName)] = attr
        else:
            #Document-fragment parent
            self.__nodeStack[-1].appendChild(attr)
        return

    def processingInstruction(self, target, data):
        pi = createProcessingInstruction(self.__ownerDoc, target, data)
        self.__nodeStack[-1].appendChild(pi)
        return

    def comment(self, data):
        comment = createComment(self.__ownerDoc, data)
        self.__nodeStack[-1].appendChild(comment)
        return

