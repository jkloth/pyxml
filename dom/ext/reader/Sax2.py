########################################################################
#
# File Name:            Sax2.py
#
# Documentation:        http://docs.4suite.com/4DOM/Sax2.py.html
#
# History:
# $Log: Sax2.py,v $
# Revision 1.1  2000/06/20 15:40:50  uche
# Initial revision
#
# Revision 1.6  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.5  2000/06/06 21:21:53  uogbuji
# Test and fix demos
# Improve parse error handling in XSLT
# Packaging and documentation
#
# Revision 1.4  2000/05/25 02:35:00  jkloth
# Moved Sax2Lib to eader directory
#
# Revision 1.3  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.2  2000/05/02 04:30:26  jkloth
# Minor bug fixes
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.15  2000/04/19 03:59:44  uogbuji
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
# Revision 1.14  2000/03/12 20:48:00  uche
# Fixed nasty attr namespace defaulting bug in Sax2
# Made DumpParseTree more readable
# Fix exception bug in XSLT
# Add Postgres QueryAdapter
#
# Revision 1.13  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.12  1999/12/27 07:07:03  uche
# Added Evaluate, Compile and CreateContext for XPath API
# Added template priority
# Updated XSL builtins, including mode support
# Removed extra spacing about attribute printing
# Fixed many bugs
#
# Revision 1.11  1999/12/18 22:54:51  uche
# Fix Namespaces to Match DOM Level 2 spec.
# Bug-fixes.
#
# Revision 1.10  1999/12/18 07:37:33  uche
# Fixed deault namespace problem in SAX2
# Updated documentation
# Changed TRACEOUT environment variables.
#
# Revision 1.9  1999/12/16 20:22:25  molson
# Fixed some bugs
#
# Revision 1.8  1999/12/15 07:54:14  molson
# Fixed minor bugs
#
# Revision 1.7  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.6  1999/12/10 18:48:48  uche
# Added Copyright files to all packages
# Added HTML pseudo-SAX engine for 4XSLT
# Added xsl:output
# Various bug-fixes.
#
# Revision 1.5  1999/12/07 08:12:31  molson
# Fixed errors in parser
#
# Revision 1.4  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
#
# Revision 1.3  1999/11/11 19:39:01  uche
# Add Error-Handling to Sax2 driver.
#
# Revision 1.2  1999/10/14 18:21:02  uche
# Fix Result Tree Fragment processing.
#
# Revision 1.1  1999/10/10 08:14:50  uche
# Added a SAX2 driver for reading XML -> DOM.
# Modified XSLT to use the SAX2 driver for its advanced capabilities.
# Added xsl-comment and xsl-copy, along with test harnesses.
# Modified URLs throughout the XSL to match the final version (yay! W3C finally got it right: no version in the bloody namespace, sheesh!)
# Added getNodeType and other basic operations to the node wrappers in XPath
# Added a new node type: NAMESPACE_NODE = 10000
#
#
#
"""
Components for reading XML files from a SAX2 producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import sys, string, cStringIO
from xml.sax import saxlib, saxexts
import Sax2Lib
from xml.dom import Entity, DocumentType, Document
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom.ext import SplitQName
from xml.dom import XML_NAMESPACE


class XmlDomGenerator(saxlib.HandlerBase,
                      Sax2Lib.LexicalHandler,
                      Sax2Lib.DTDDeclHandler,
                      Sax2Lib.NamespaceHandler):
    def __init__(self, doc=None, keepAllWs=0):
        self.__ownerDoc = None
        self.__rootNode = None
        #Set up the stack which keeps track of the nesting of DOM nodes.
        self.__nodeStack = []
        if doc:
            self.__ownerDoc = doc
            #Create a docfrag to hold all the generated nodes.
            self.__rootNode = self.__ownerDoc.createDocumentFragment()
            self.__nodeStack.append(self.__rootNode)
        self.__dt = None
        self.__xmlDecl = None
        self.__orphanedNodes = []
        self.__namespaces = [{'xml': XML_NAMESPACE}]
        self.__keepAllWs = keepAllWs
        self.__currText = ''

    def __initRootNode(self, docElementUri, docElementName):
        if not self.__dt:
            self.__dt = implementation.createDocumentType(docElementName,'','')
        self.__ownerDoc = implementation.createDocument(docElementUri, docElementName, self.__dt)
        dt_ix = self.__ownerDoc._4dom_getChildIndex(self.__dt)
        if self.__xmlDecl:
            decl_data = 'version="%s"' % (
                    self.__xmlDecl['version']
                    )
            if self.__xmlDecl['encoding']:
                decl_data = decl_data + ' encoding="%s"'%(
                    self.__xmlDecl['encoding']
                    )
            if self.__xmlDecl['standalone']:
                decl_data = decl_data + ' standalone="%s"'%(
                    self.__xmlDecl['standalone']
                    )
            xml_decl_node = self.__ownerDoc.createProcessingInstruction(
                'xml',
                decl_data
                )
            self.__ownerDoc.insertBefore(xml_decl_node, self.__ownerDoc.docType)
        before_doctype = 1
        for o_node in self.__orphanedNodes:
            if o_node[0] == 'pi':
                pi = self.__ownerDoc.createProcessingInstruction(
                    o_node[1],
                    o_node[2]
                    )
                if before_doctype:
                    self.__ownerDoc.insertBefore(pi, self.__dt)
                else:
                    self.__ownerDoc.appendChild(pi)
            elif o_node[0] == 'comment':
                comment = self.__ownerDoc.createComment(o_node[1])
                if before_doctype:
                    self.__ownerDoc.insertBefore(comment, self.__dt)
                else:
                    self.__ownerDoc.appendChild(comment)
            elif o_node[0] == 'doctype':
                before_doctype = 0
        self.__rootNode = self.__ownerDoc
        self.__nodeStack.append(self.__rootNode)

    def __completeTextNode(self):
        #Note some parsers don;t report ignorable white space properly 
        if self.__currText and len(self.__nodeStack) and self.__nodeStack[-1].nodeType != Node.DOCUMENT_NODE:
            new_text = self.__ownerDoc.createTextNode(self.__currText)
            self.__nodeStack[-1].appendChild(new_text)
        self.__currText = ''

    def getRootNode(self):
        self.__completeTextNode()
        return self.__rootNode

    #Overridden DocumentHandler methods
    def processingInstruction (self, target, data):
        if self.__rootNode:
            self.__completeTextNode()
            pi = self.__ownerDoc.createProcessingInstruction(target, data)
            self.__nodeStack[-1].appendChild(pi)
        else:
            self.__orphanedNodes.append(('pi', target, data))

    def startElement(self, name, attribs):
        pass
        self.__completeTextNode()
        self.__namespaces.append(self.__namespaces[-1].copy())
        for curr_attrib_key in attribs.keys():
            name_parts = SplitQName(curr_attrib_key)
            if name_parts == ('', 'xmlns'):
                self.__namespaces[-1][''] = attribs[curr_attrib_key]
            elif name_parts[0] == 'xmlns':
                self.__namespaces[-1][name_parts[1]] = attribs[curr_attrib_key]
        name_parts = SplitQName(name)

        pass

        if self.__ownerDoc:
            new_element = self.__ownerDoc.createElementNS(
                self.__namespaces[-1].has_key(name_parts[0]) and self.__namespaces[-1][name_parts[0]] or '',
                name
                )
        else:
            self.__initRootNode(
                self.__namespaces[-1].has_key(name_parts[0]) and self.__namespaces[-1][name_parts[0]] or '',
                name
                )
            new_element = self.__ownerDoc.documentElement

        for curr_attrib_key in attribs.keys():
            pass
            name_parts = SplitQName(curr_attrib_key)
            if name_parts == ('', 'xmlns') or name_parts[0] == 'xmlns':
                new_element.setAttributeNS(
                    '',
                    curr_attrib_key,
                    attribs[curr_attrib_key]
                    )
            else:
                name_parts = SplitQName(curr_attrib_key)
                if name_parts[0] and self.__namespaces[-1].has_key(name_parts[0]):
                    ns = self.__namespaces[-1][name_parts[0]]
                else:
                    ns = ''
                new_element.setAttributeNS(
                    ns,
                    curr_attrib_key,
                    attribs[curr_attrib_key]
                    )
        self.__nodeStack.append(new_element)

    def endElement(self, name):
        self.__completeTextNode()
        new_element = self.__nodeStack[-1]
        del self.__nodeStack[-1]
        del self.__namespaces[-1]
        if new_element != self.__ownerDoc.documentElement:
            self.__nodeStack[-1].appendChild(new_element)

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        A Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self.__keepAllWs and self.__nodeStack[-1].nodeType !=  Node.DOCUMENT_NODE:
            self.__currText = self.__currText + ch[start:start+length]

    def characters(self, ch, start, length):
        self.__currText = self.__currText + ch[start:start+length]

    #Overridden LexicalHandler methods
    def xmlDecl(self, version, encoding, standalone):
        self.__xmlDecl = {'version': version, 'encoding': encoding, 'standalone': standalone}

    def startDTD(self, doctype, publicID, systemID):
        if not self.__rootNode:
            self.__dt = implementation.createDocumentType(doctype, publicID, systemID)
            self.__orphanedNodes.append(('doctype'))
        else:
            raise 'Illegal DocType declaration'

    def comment(self, text):
        if self.__rootNode:
            self.__completeTextNode()
            new_comment = self.__ownerDoc.createComment(text)
            self.__nodeStack[-1].appendChild(new_comment)
        else:
            self.__orphanedNodes.append(('comment', text))

    def startCDATA(self):
        self.__completeTextNode()

    def endCDATA(self):
        #NOTE: this doesn't handle the error where endCDATA is called
        #Without corresponding startCDATA.  Is this a problem?
        if self.__currText:
            new_text = self.__ownerDoc.createCDATASection(self.__currText)
            self.__nodeStack[-1].appendChild(new_text)
            self.__currText = ''


    #Overridden DTDHandler methods
    def notationDecl (self, name, publicId, systemId):
        new_notation = self.__ownerDoc.getFactory().createNotation(self.__ownerDoc,  publicId, systemId, name)
        self.__ownerDoc.getDocumentType().getNotations().setNamedItem(new_notation)

    def unparsedEntityDecl (self, publicId, systemId, notationName):
        new_notation = self.__ownerDoc.getFactory().createEntity(self.__ownerDoc,  publicId, systemId, notationName)
        self.__ownerDoc.getDocumentType().getEntities().setNamedItem(new_notation)

    #Overridden ErrorHandler methods
    #FIXME: How do we handle warnings?

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
    rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName, saxHandlerClass)
    return rv

def FromXmlFile(fileName,
                ownerDocument=None,
                validate=0,
                keepAllWs=0,
                catName=None,
                saxHandlerClass=XmlDomGenerator):
    fp = open(fileName, 'r')
    rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName, saxHandlerClass)
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
    rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName, saxHandlerClass)
    fp.close()
    return rv

