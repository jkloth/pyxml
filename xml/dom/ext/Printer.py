########################################################################
#
# File Name:            Printer.py
#
# Documentation:        http://docs.4suite.com/4DOM/Printer.py.html
#
"""
The printing sub-system.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, re
from xml.dom.Node import Node
from xml.dom.ext.Visitor import Visitor, WalkerInterface
from xml.dom import ext, XMLNS_NAMESPACE
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE, HTML_FORBIDDEN_END

ILLEGAL_LOW_CHARS = '[\x01-\x08\x0B-\x0C\x0E-\x1F]'
SURROGATE_BLOCK = '[\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF]'
ILLEGAL_HIGH_CHARS = '\xEF\xBF[\xBE\xBF]'
#Note: Prolly fuzzy on this, but it looks as if characters from the surrogate block are allowed if in scalar form, which is encoded in UTF8 the same was as in surrogate block form
XML_ILLEGAL_CHAR_PATTERN = re.compile('%s|%s'%(ILLEGAL_LOW_CHARS, ILLEGAL_HIGH_CHARS))

g_utf8TwoBytePattern = re.compile('([\xC0-\xC3])([\x80-\xBF])')
g_cdataCharPattern = re.compile('[&<]|]]>')
g_charToEntity = {
        '&': '&amp;',
        '<': '&lt;',
        ']]>': ']]&gt;',
        }

try:
    #The following stanza courtesy Martin von Loewis
    import codecs # Python 1.5 only
    from types import UnicodeType
    def utf8_to_code(text, encoding):
        encoder = codecs.lookup(encoding)[0] # encode,decode,reader,writer
        if type(text) is not UnicodeType:
            text = unicode(text, "utf-8")
        return encoder(text)[0] # result,size
except ImportError:
    def utf8_to_code(text, encoding):
        encoding = string.upper(encoding)
        if encoding == 'UTF-8':
            return text
        from xml.unicode.iso8859 import wstring
        wstring.install_alias('ISO-8859-1', 'ISO_8859-1:1987')
        #Note: Pass through to wstrop.  This means we don't play nice and
        #Escape characters that are not in the target encoding.
        ws = wstring.from_utf8(text)
        text = ws.encode(encoding)
        #This version would skip all untranslatable chars: see wstrop.c
        #text = ws.encode(encoding, 1)
        return text


def TranslateCdataAttr(characters):
    '''Handles normalization and some intelligence about quoting'''
    if not characters:
        return '', "'"
    if "'" in characters:
        delimiter = '"'
        new_chars = re.sub('"', '&quot;', characters)
    else:
        delimiter = "'"
        new_chars = re.sub("'", '&apos;', characters)
    #FIXME: There's more to normalization
    #Convert attribute new-lines to character entity
    # characters is possibly shorter than new_chars (no entities)
    if "\n" in characters:
        new_chars = re.sub('\n', '&#10;', new_chars)
    return new_chars, delimiter


#Note: UCS-2 only for now
def TranslateCdata(characters, encoding='UTF-8', prev_chars='', markupSafe=0):
    if not characters:
        return ''
    if not markupSafe:
        if g_cdataCharPattern.search(characters):
            new_string = g_cdataCharPattern.subn(
                lambda m, d=g_charToEntity: d[m.group()],
                characters)[0]
        else:
            new_string = characters
        if prev_chars[-2:] == ']]' and characters[0] == '>':
            new_string = '&gt;' + new_string[1:]
    else:
        new_string = characters
    #Note: use decimal char entity rep because some browsers are broken
    #FIXME: This will bomb for high characters.  Should, for instance, detect
    #The UTF-8 for 0xFFFE and put out &#xFFFE;
    if XML_ILLEGAL_CHAR_PATTERN.search(new_string):
        new_string = XML_ILLEGAL_CHAR_PATTERN.subn(
            lambda m: '&#%i;' % ord(m.group()),
            new_string)[0]
    new_string = utf8_to_code(new_string, encoding)
    return new_string


class PrintVisitor(Visitor):
    def __init__(self, stream, encoding, nsHints=None):
        self._namespaces = [{}]
        self._nsHints = nsHints or {}
        self.stream = stream
        self.encoding = encoding
        return

    def visit(self, node):
        nodeType = node.nodeType

        if node.nodeType == Node.ELEMENT_NODE:
            return self.visitElement(node)

        elif node.nodeType == Node.ATTRIBUTE_NODE:
            return self.visitAttr(node)

        elif node.nodeType == Node.TEXT_NODE:
            return self.visitText(node)

        elif node.nodeType == Node.CDATA_SECTION_NODE:
            return self.visitCDATASection(node)

        elif node.nodeType == Node.ENTITY_REFERENCE_NODE:
            return self.visitEntityReference(node)

        elif node.nodeType == Node.ENTITY_NODE:
            return self.visitEntity(node)

        elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            return self.visitProcessingInstruction(node)

        elif node.nodeType == Node.COMMENT_NODE:
            return self.visitComment(node)

        elif node.nodeType == Node.DOCUMENT_NODE:
            return self.visitDocument(node)

        elif node.nodeType == Node.DOCUMENT_TYPE_NODE:
            return self.visitDocumentType(node)

        elif node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            return self.visitDocumentFragment(node)

        elif node.nodeType == Node.NOTATION_NODE:
            return self.visitNotation(node)

        # It has a node type, but we don't know how to handle it
        raise "Unknown node type: Node=" + str(node)

    def visitNodeList(self, node, exclude=None):
        for curr in node:
            if exclude and exclude == curr:
                continue
            self.visit(curr)
        return

    def visitNamedNodeMap(self, node):
        for item in node.values():
            self.visit(item)
        return

    def visitAttr(self, node):
        if node.namespaceURI == XMLNS_NAMESPACE:
            return
        if hasattr(node.ownerDocument,'isHtml') and node.ownerDocument.isHtml() and len(node.childNodes) == 0:
            st = ' ' + node.name
        else:
            text = TranslateCdata(node.value, self.encoding)
            text, delimiter = TranslateCdataAttr(text)
            st = " %s=%s%s%s" % (node.name, delimiter, text, delimiter)
        self.stream.write(st)
        return

    def visitProlog(self):
        self.stream.write("<?xml version='1.0' encoding='%s'?>" % (self.encoding or 'UTF-8'))

    def visitDocument(self, node):
        if not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml():
            self.visitProlog()
        if node.doctype != None:
            self.visit(node.doctype)
        self.visitNodeList(node.childNodes, exclude=node.doctype)
        return

    def visitDocumentFragment(self, node):
        self.visitNodeList(node.childNodes)
        return

    def visitElement(self, node):
        #FIXME: Borrow opt from Sax2
        self._namespaces.append(self._namespaces[-1].copy())
        self.stream.write('<' + node.tagName)
        if not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml():
            st = ''
            nss = ext.GetAllNs(node)
            if self._nsHints:
                self._nsHints.update(nss)
                nss = self._nsHints
                self._nsHints = {}
            del nss['xml']
            for prefix in nss.keys():
                if not self._namespaces[-1].has_key(prefix) or self._namespaces[-1][prefix] != nss[prefix]:
                    if prefix:
                        st = st + ' xmlns:' + prefix + "='" + nss[prefix] + "'"
                    else:
                        st = st + ' xmlns' + "='" + nss[prefix] + "'"
                self._namespaces[-1][prefix] = nss[prefix]
            self.stream.write(st)
        self.visitNamedNodeMap(node.attributes)
        if len(node.childNodes):
            self.stream.write('>')
            self.visitNodeList(node.childNodes)
            if not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml() or (node.tagName not in HTML_FORBIDDEN_END):
                self.stream.write('</' + node.tagName + '>')
        elif not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml():
            self.stream.write('/>')
        elif node.tagName not in HTML_FORBIDDEN_END:
            self.stream.write('></' + node.tagName + '>')
        else:
            self.stream.write('>')
        del self._namespaces[-1]
        return

    def visitText(self, node):
        self.stream.write(TranslateCdata(node.data, self.encoding))

    def visitDocumentType(self, node):
        if node.systemId != '':
            self.__emptyReturn = 0
            self.stream.write("<!DOCTYPE " + node.name)
            if node.publicId != '':
                self.stream.write(' PUBLIC "' + node.publicId + '"')
            self.stream.write(' SYSTEM "' + node.systemId + '" ')
            if node.entities.length or node.notations.length:
                self.stream.write('[')
                self.visitNamedNodeMap(node.entities)
                self.visitNamedNodeMap(node.notations)
                self.stream.write(']')
            self.stream.write('>')
        return

    def visitEntity(self, node):
        st = "<!ENTITY %s "%(node.nodeName)
        if (node.publicId):
            st = st + "PUBLIC %s "%(node.publicId)
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        if (node.notationName):
            st = st + "NDATA %s "%(node.notationName)
        self.stream.write(st + '>')
        return

    def visitNotation(self, node):
        st = "<!NOTATION %s "%(node.nodeName)
        if (node.publicId):
            st = st + "PUBLIC %s "%(node.publicId)
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        self.stream.write(st + '>')
        return

    def visitCDATASection(self, node):
        self.stream.write('<![CDATA[')
        self.stream.write(node.data)
        self.stream.write(']]>')
        return

    def visitComment(self, node):
        self.stream.write('<!--')
        self.stream.write(node.data)
        self.stream.write('-->')
        return

    def visitEntityReference(self, node):
        self.stream.write('&')
        self.stream.write(node.nodeName)
        self.stream.write(';')
        return

    def visitProcessingInstruction(self, node):
        self.stream.write('<?')
        self.stream.write(node.target + ' ')
        self.stream.write(node.data)
        self.stream.write('?>')
        return


class PrettyPrintVisitor(PrintVisitor):
    def __init__(self, stream, encoding, indent, width, plainElements, nsHints=None):
        self.encoding = encoding
        self._indent = indent
        self._depth = 0
        self._width = width
        self._plainElements = plainElements
        self._printPlain = 0
        self._prevNodeIsText = 0
        self._emptyReturn = 0
        self._namespaces = [{}]
        self._nsHints = nsHints or {}
        self.stream = stream
        return

    def visitProlog(self):
        PrintVisitor.visitProlog(self)
        self.stream.write("\n")

    def visitElement(self, node):
        if self._printPlain:
            PrintVisitor.visitElement(self, node)
            return
        self._namespaces.append(self._namespaces[-1].copy())
        if node.tagName in self._plainElements:
            #We don't want to insert whitespace into any flagged element
            #FIXME: handle xml:preserve?
            return self.visitPlainElement(node)
        if self._prevNodeIsText or self._emptyReturn:
            self._prevNodeIsText = 0
            self._emptyReturn = 0
            self.stream.write('<' + node.tagName)
        else:
            self.stream.write('\n' + self._indent*self._depth + '<' + node.tagName)
        if not hasattr(node.ownerDocument,"isXml") or node.ownerDocument.isXml():
            st = ''
            nss = ext.GetAllNs(node)
            if self._nsHints:
                self._nsHints.update(nss)
                nss = self._nsHints
                self._nsHints = {}
            del nss['xml']
            for prefix in nss.keys():
                if not self._namespaces[-1].has_key(prefix) or self._namespaces[-1][prefix] != nss[prefix]:
                    if prefix:
                        st = st + ' xmlns:' + prefix + "='" + nss[prefix] + "'"
                    else:
                        st = st + ' xmlns' + "='" + nss[prefix] + "'"
                self._namespaces[-1][prefix] = nss[prefix]
            self.stream.write(st)
        self.visitNamedNodeMap(node.attributes)
        #st = string.rstrip(st)
        st = ''
        if len(node.childNodes):
            self.stream.write('>')
            self._depth = self._depth + 1
            self.visitNodeList(node.childNodes)
            self._depth = self._depth - 1
            if not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml() or (node.tagName not in HTML_FORBIDDEN_END):
                if self._prevNodeIsText:
                    self._prevNodeIsText = 0
                    self.stream.write('</' + node.tagName + '>')
                else:
                    self.stream.write('\n' + self._indent*self._depth + '</' + node.tagName + '>')
        elif not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml():
            self.stream.write('/>')
        elif node.tagName not in HTML_FORBIDDEN_END:
            self.stream.write('></' + node.tagName + '>')
        else:
            self.stream.write('>')
        del self._namespaces[-1]
        return

    def visitPlainElement(self, node):
        self._printPlain = 1
        if self._prevNodeIsText or self._emptyReturn:
            self._prevNodeIsText = 0
            self._emptyReturn = 0
            self.stream.write('<' + node.tagName + ' ')
        else:
            self.stream.write('\n' + self._indent*self._depth + '<' + node.tagName + ' ')
        self.visitNamedNodeMap(node.attributes)
        if len(node.childNodes):
            self.stream.write('>')
            self._depth = self._depth + 1
            self.visitNodeList(node.childNodes)
            self._depth = self._depth - 1
            if self._prevNodeIsText:
                self._prevNodeIsText = 0
                self.stream.write('</' + node.tagName + '>')
            else:
                self.stream.write('\n' + self._depth*self._indent + '</' + node.tagName + '>')
        elif not hasattr(node.ownerDocument,'isXml') or node.ownerDocument.isXml():
            self.stream.write('/>')
        elif node.tagName not in HTML_FORBIDDEN_END:
            self.stream.write('></' + node.tagName + '>')
        else:
            self.stream.write('>')
        self._printPlain = 0
        return

    def visitText(self, node):
        self._prevNodeIsText = 1
        return PrintVisitor.visitText(self, node)

    def visitDocumentType(self, node):
        self._emptyReturn = 1
        return PrintVisitor.visitDocumentType(self, node)



class PrintWalker(WalkerInterface):
    def __init__(self, visitor, startNode):
        WalkerInterface.__init__(self, visitor)
        self.start_node = startNode
        return

    def step(self):
        """There is really no step to printing.  It prints the whole thing"""
        self.visitor.visit(self.start_node)
        return

    def run(self):
        return self.step()

