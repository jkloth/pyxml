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

import os, urllib
from xml.dom.ext import reader, ReleaseNode
from xml.dom import Node

import Sgmlop

class Reader(reader.Reader):
    def __init__(self):
        self.parser = Sgmlop.HtmlParser()

    def fromStream(self, stream, ownerDoc=None, charset=''):
        self.parser.initParser()
        self.parser.initState(ownerDoc, charset)
        self.parser.parse(stream)
        frag = self.parser.rootNode

        if ownerDoc is None:
            for child in frag.childNodes:
                if child.nodeType == Node.ELEMENT_NODE and child.tagName == 'HTML':
                    # Use the created document
                    doc = frag.ownerDocument
                    break
            else:
                doc = None
        else:
            doc = ownerDoc

        if doc:
            while doc.firstChild:
                # Empty out the document
                node = doc.removeChild(doc.firstChild)
                ReleaseNode(node)
                
            # Convert to a document
            while frag.firstChild:
                child = frag.firstChild
                if child.nodeType != Node.TEXT_NODE:
                    # Skip top-level text nodes
                    doc.appendChild(child)
                else:
                    frag.removeChild(child)
        return doc or frag

    def fromUri(self, uri, ownerDoc=None, charset=''):
        stream = reader.BASIC_RESOLVER.resolve(uri)
        try:
            return self.fromStream(stream, ownerDoc, charset)
        finally:
            stream.close()

    def fromString(self, str, ownerDoc=None, charset=''):
        stream = reader.StrStream(str)
        try:
            return self.fromStream(stream, ownerDoc, charset)
        finally:
            stream.close()

########################## Deprecated ##############################

def FromHtmlStream(fp, ownerDoc=None, charset=''):
    return Reader().fromStream(fp, ownerDoc, charset)


def FromHtmlFile(fileName, ownerDoc=None, charset=''):
    return Reader().fromUri(fileName, ownerDoc, charset)


def FromHtmlUrl(url, ownerDoc=None, charset=''):
    return Reader().fromUri(url, ownerDoc, charset)


def FromHtml(text, ownerDoc=None, charset=''):
    return Reader().fromString(text, ownerDoc, charset)

