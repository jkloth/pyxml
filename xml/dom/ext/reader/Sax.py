########################################################################
#
# File Name:            Sax.py
#
# Documentation:        http://docs.4suite.com/4DOM/Sax.py.html
#
# History:
# $Log: Sax.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.3  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.2  2000/04/27 19:08:50  jkloth
# fixed imports for xml-sig
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.12  2000/04/19 03:59:44  uogbuji
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
# Revision 1.11  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.10  2000/01/03 23:50:25  uche
# Implemented xsl:sort
# Many bug-fixes and additions
#
# Revision 1.9  1999/12/18 22:54:51  uche
# Fix Namespaces to Match DOM Level 2 spec.
# Bug-fixes.
#
# Revision 1.8  1999/12/18 08:28:50  uche
# Fix SAX for default namespaces.
# Correct namespaces in XSLT context to read from stylesheet rather than XML source.
#
# Revision 1.7  1999/12/10 18:48:48  uche
# Added Copyright files to all packages
# Added HTML pseudo-SAX engine for 4XSLT
# Added xsl:output
# Various bug-fixes.
#
# Revision 1.6  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
#
# Revision 1.5  1999/11/19 02:13:23  uche
# Python/DOM binding update.
#
# Revision 1.4  1999/11/19 01:32:41  uche
# Python/DOM binding changes.
#
# Revision 1.3  1999/11/18 09:30:02  uche
# Python/DOM binding update.
#
# Revision 1.2  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.1  1999/09/26 00:14:31  uche
# Added the reader ext module to supersede Builder.  Made the appropriate conversions to other 4Suite components.
#
#
#
"""
Components for reading XML files from a SAX producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import sys, string, cStringIO
from xml.sax import saxlib, saxexts, drivers
from xml.dom import Entity, DocumentType, Document
from xml.dom import DocumentType, Document
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom.ext import SplitQName


class XmlDomGenerator(saxlib.HandlerBase):
    def __init__(self, doc=None, keepAllWs=0):
        """
        If None is passed in as the doc, set up an empty document to act
        as owner and also add all elements to this document
        """
        if doc == None:
            dt = implementation.createDocumentType('', '', '')
            self.__ownerDoc = implementation.createDocument('', None, dt)
            self.__ownerDoc.__dict__['_4dom_isNsAware'] = 0
            self.__rootNode = self.__ownerDoc
        else:
            self.__ownerDoc = doc
            self.__ownerDoc.__dict__['_4dom_isNsAware'] = 0
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

    #Overridden DTDHandler methods
    def notationDecl (self, name, publicId, systemId):
        new_notation = self.__ownerDoc.createNotation(self.__ownerDoc,  publicId, systemId, name)
        self.__ownerDoc.documentType.notations.setNamedItem(new_notation)

    def unparsedEntityDecl (self, publicId, systemId, notationName):
        new_notation = implementation.createEntity(self.__ownerDoc,  publicId, systemId, notationName)
        self.__ownerDoc.documentType.entities.setNamedItem(new_notation)

    #Overridden DocumentHandler methods
    def processingInstruction (self, target, data):
        self.__completeTextNode()
        p = self.__ownerDoc.createProcessingInstruction(target,data);
        self.__nodeStack[-1].appendChild(p)

    def startElement(self, name, attribs):
        pass
        self.__completeTextNode()
        new_element = self.__ownerDoc.createElement(name)

        for curr_attrib_key in attribs.keys():
            pass
            new_element.setAttribute(
                curr_attrib_key,
                attribs[curr_attrib_key]
                )
        self.__nodeStack.append(new_element)

    def endElement(self, name):
        self.__completeTextNode()
        new_element = self.__nodeStack[-1]
        del self.__nodeStack[-1]
        self.__nodeStack[-1].appendChild(new_element)

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        A Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        #if self.__keepAllWs and self.__nodeStack[-1].nodeType == Node.DOCUMENT_NODE:
        if self.__keepAllWs:
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


def FromXmlStream(stream,
                  ownerDocument=None,
                  validate=0,
                  keepAllWs=0,
                  catName=None,
                  saxHandlerClass=XmlDomGenerator):
    #Create an XML DOM from SAX events
    parser = (validate and saxexts.XMLValParserFactory.make_parser()) or  saxexts.XMLParserFactory.make_parser()
    if catName:
        #set up the catalog, if there is one
        from xml.parsers.xmlproc import catalog
        cat_handler = catalog.SAX_catalog(catName, catalog.CatParserFactory())
        parser.setEntityResolver(cat_handler)
    handler = saxHandlerClass(ownerDocument, keepAllWs)
    parser.setDocumentHandler(handler)
    parser.setDTDHandler(handler)
    parser.setErrorHandler(handler)

    parser.parseFile(stream)
    return handler.getRootNode()

def FromXml(str,
            ownerDocument=None,
            validate=0,
            keepAllWs=0,
            catName=None,
            saxHandlerClass=XmlDomGenerator):
    fp = cStringIO.StringIO(str)
    rv = FromXmlStream(fp,ownerDocument,validate,keepAllWs,catName,saxHandlerClass)
    return rv

def FromXmlFile(fileName,
                ownerDocument=None,
                validate=0,
                keepAllWs=0,
                catName=None,
                saxHandlerClass=XmlDomGenerator):
    fp = open(fileName, 'r')
    rv = FromXmlStream(fp,ownerDocument,validate,keepAllWs,catName,saxHandlerClass)
    fp.close()
    return rv

def FromXmlUrl(url,
               ownerDocument=None,
               validate=0,
               keepAllWs=0,
               catName=None,
               saxHandlerClass=XmlDomGenerator):
    import urllib
    fp = urllib.urlopen(url)
    rv = FromXmlStream(fp,ownerDocument,validate,keepAllWs,catName,saxHandlerClass)
    fp.close()
    return rv
