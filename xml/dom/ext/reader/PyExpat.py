########################################################################
#
# File Name:            PyExpat.py
#
# Documentation:        http://docs.4suite.com/4DOM/PyExpat.py.html
#
"""
Components for reading XML files from PyExpat (Python 1.6, 2.0 or from PyXML).
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, string, cStringIO
from xml.dom import Entity, DocumentType, Document
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom.ext import SplitQName, ReleaseNode
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE
from xml.dom import Element
from xml.dom import Attr

class Reader:
    def __init__(self):
        return

    def releaseNode(self, node):
        ReleaseNode(node)

    def initState(self, doc=None):
        self._ownerDoc = None
        self._rootNode = None
        #Set up the stack which keeps track of the nesting of DOM nodes.
        self._nodeStack = []
        if doc:
            self._ownerDoc = doc
            #Create a docfrag to hold all the generated nodes.
            self._rootNode = self._ownerDoc.createDocumentFragment()
            self._nodeStack.append(self._rootNode)
        self._dt = None
        self._xmlDecl = None
        self._orphanedNodes = []
        self._namespaces = {'xml': XML_NAMESPACE}
        self._namespaceStack = []
        self._keepAllWs = keepAllWs
        self._currText = ''
        return

    def initParser(self):
        self.parser=pyexpat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.characters
        self.parser.ProcessingInstructionHandler = self.processingInstruction
        self.parser.CommentHandler = self.comment
        self.parser.StartCdataSectionHandler = self.startCDATA
        self.parser.EndCdataSectionHandler = self.endCDATA
        self.parser.NotationDeclHandler = self.notationDecl
        self.parser.UnparsedEntityDeclHandler = self.unparsedEntityDecl
        return
    
    def fromStream(self, stream, doc=None, stripElements=None):
        if not self._override:
            self.initParser()
        self.initState(doc, stripElements)
        success = self.parser.ParseFile(stream)
        if not success:
            ReleaseNode(self._rootNode)
            ReleaseNode(self._ownerDoc)
            raise Ft.Lib.FtException(Ft.Lib.Error.XML_PARSE_ERROR, (self.parser.ErrorLineNumber, self.parser.ErrorColumnNumber, pyexpat.ErrorString(self.parser.ErrorCode)))
        self._completeTextNode()
        return self._rootNode or self._ownerDoc

    def fromUri(self, uri, doc=None, stripElements=None):
        if os.path.exists(uri):
            stream = open(uri)
        else:
            stream = urllib.urlopen(uri)
        rt = self.fromStream(stream, doc,stripElements)
        stream.close()
        return rt

    def _initRootNode(self, docElementUri, docElementName):
        if not self._dt:
            self._dt = implementation.createDocumentType(docElementName,'','')
        self._ownerDoc = implementation.createDocument(docElementUri, docElementName, self._dt)
        before_doctype = 1
        for o_node in self._orphanedNodes:
            if o_node[0] == 'pi':
                pi = self._ownerDoc.createProcessingInstruction(
                    o_node[1],
                    o_node[2]
                    )
                if before_doctype:
                    self._ownerDoc.insertBefore(pi, self._dt)
                else:
                    self._ownerDoc.appendChild(pi)
            elif o_node[0] == 'comment':
                comment = self._ownerDoc.createComment(o_node[1])
                if before_doctype:
                    self._ownerDoc.insertBefore(comment, self._dt)
                else:
                    self._ownerDoc.appendChild(comment)
            elif o_node[0] == 'doctype':
                before_doctype = 0
        self._rootNode = self._ownerDoc
        self._nodeStack.append(self._rootNode)
        return

    def _completeTextNode(self):
        #Note some parsers don;t report ignorable white space properly
        if self._currText and len(self._nodeStack) and self._nodeStack[-1].nodeType != Node.DOCUMENT_NODE:
            new_text = self._ownerDoc.createTextNode(self._currText)
            self._nodeStack[-1].appendChild(new_text)
        self._currText = ''
        return

    def processingInstruction (self, target, data):
        if self._rootNode:
            self._completeTextNode()
            pi = self._ownerDoc.createProcessingInstruction(target, data)
            self._nodeStack[-1].appendChild(pi)
        else:
            self._orphanedNodes.append(('pi', target, data))
        return

    def startElement(self, name, attribs):
        self._completeTextNode()
        old_nss = {}
        del_nss = []
        for curr_attrib_key, value in attribs.items():
            (prefix, local) = SplitQName(curr_attrib_key)
            if local == 'xmlns':
                if self._namespaces.has_key(prefix):
                    old_nss[prefix] = self._namespaces[prefix]
                else:
                    del_nss.append(prefix)
                if (prefix or value):
                    self._namespaces[prefix] = attribs[curr_attrib_key]
                else:
                    del self._namespaces[prefix]

        self._namespaceStack.append((old_nss, del_nss))
        (prefix, local) = SplitQName(name)
        nameSpace = self._namespaces.get(prefix, '')

        if self._ownerDoc:
            new_element = self._ownerDoc.createElementNS(
                nameSpace,
                (prefix and prefix + ':' +  local) or local
                )
        else:
            self._initRootNode(nameSpace, name)
            new_element = self._ownerDoc.documentElement

        for curr_attrib_key,curr_attrib_value in attribs.items():
            (prefix, local) = SplitQName(curr_attrib_key)
            if local == 'xmlns':
                namespace = XMLNS_NAMESPACE
                attr = self._ownerDoc.createAttributeNS(namespace,
                                                         local + ':' + prefix)
            else:
                namespace = prefix and self._namespaces.get(prefix, '') or ''
                attr = self._ownerDoc.createAttributeNS(namespace,
                                                         (prefix and prefix + ':' + local) or local)
            attr.value = curr_attrib_value
            new_element.setAttributeNodeNS(attr)
        self._nodeStack.append(new_element)
        return

    def endElement(self, name):
        self._completeTextNode()
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        old_nss, del_nss = self._namespaceStack[-1]
        del self._namespaceStack[-1]
        self._namespaces.update(old_nss)
        for prefix in del_nss:
            del self._namespaces[prefix]
        if new_element != self._ownerDoc.documentElement:
            self._nodeStack[-1].appendChild(new_element)
        return

    def characters(self, data):
        self._currText = self._currText + data
        return

    def startDTD(self, doctype, publicID, systemID):
        if not self._rootNode:
            self._dt = implementation.createDocumentType(doctype, publicID, systemID)
            self._orphanedNodes.append(('doctype'))
        else:
            raise 'Illegal DocType declaration'
        return

    def comment(self, text):
        if self._rootNode:
            self._completeTextNode()
            new_comment = self._ownerDoc.createComment(text)
            self._nodeStack[-1].appendChild(new_comment)
        else:
            self._orphanedNodes.append(('comment', text))
        return

    def startCDATA(self):
        self._completeTextNode()
        return

    def endCDATA(self):
        #NOTE: this doesn't handle the error where endCDATA is called
        #Without corresponding startCDATA.  Is this a problem?
        if self._currText:
            new_text = self._ownerDoc.createCDATASection(self._currText)
            self._nodeStack[-1].appendChild(new_text)
            self._currText = ''
        return

    def notationDecl(self, name, base, publicId, systemId):
        #FIXME: Base URI resolution?
        new_notation = self._ownerDoc.getFactory().createNotation(self._ownerDoc,  publicId, systemId, name)
        self._ownerDoc.getDocumentType().getNotations().setNamedItem(new_notation)
        return

    def unparsedEntityDecl(self, name, base, publicId, systemId,
                            notationName):
        #FIXME: Base URI resolution?
        new_notation = self._ownerDoc.getFactory().createEntity(self._ownerDoc,  publicId, systemId, notationName)
        self._ownerDoc.getDocumentType().getEntities().setNamedItem(new_notation)
        return

