########################################################################
#
# File Name:            Printer.py
#
# Documentation:        http://docs.4suite.com/4DOM/Printer.py.html
#
# History:
# $Log: Printer.py,v $
# Revision 1.5  2000/09/28 06:54:13  loewis
# Don't try to decode Unicode objects.
#
# Revision 1.4  2000/09/27 23:45:25  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.36  2000/09/27 22:25:12  uogbuji
# Dom printer updates for embryonic Py 2.0 compatability
#
# Revision 1.35  2000/09/25 21:43:56  uogbuji
# Doc and other packaging fixes
#
# Revision 1.34  2000/09/22 21:56:13  uogbuji
# Add output encoding support to printer
#
# Revision 1.33  2000/09/21 23:47:41  uogbuji
# Dom fixes: Alex F and Nico
#
# Revision 1.32  2000/09/19 20:24:00  uogbuji
# Buncha DOM fixes: namespaces, printing, etc.
# Add Alex F's problem reports to Dom/test_suite/problems
#
# Revision 1.31  2000/09/15 22:10:33  molson
# Removed isHtml reference
#
# Revision 1.30  2000/09/15 18:21:21  molson
# Fixed minor import bugs
#
# Revision 1.29  2000/09/11 08:35:44  uogbuji
# Fix output translation... again.
#
# Revision 1.28  2000/09/10 22:56:46  uogbuji
# Minor fixes
#
# Revision 1.27  2000/09/09 00:43:20  uogbuji
# Fix illegal character checks
# Printer fixes
#
# Revision 1.26  2000/09/09 00:22:33  uogbuji
# undo cogbuji's erroneous commit
#
# Revision 1.24  2000/09/05 05:28:07  uogbuji
# small fixes
#
# Revision 1.23  2000/09/04 22:53:57  uogbuji
# bug-fix
#
# Revision 1.22  2000/09/04 00:14:39  uogbuji
# Make Printer smarter about multiply-declared namespaces
#
# Revision 1.21  2000/08/29 21:07:06  uogbuji
# Fix xsl:strip and preserve-space
#
# Revision 1.20  2000/08/29 02:26:52  uogbuji
# Fix silly attribute bug
#
# Revision 1.19  2000/08/28 08:31:41  uogbuji
# Optimization and some bug-fixes to printer
#
# Revision 1.18  2000/08/28 06:34:46  uogbuji
# bug fixes
#
# Revision 1.17  2000/08/27 20:07:19  cogbuji
# minor bug fixes to Printer
#
# Revision 1.16  2000/08/26 00:47:06  uogbuji
# Bug fixes
# Add some IEEE 754 pseudo-support
#
# Revision 1.15  2000/08/25 23:32:49  uogbuji
# Fix bugs where xmlns is introduced erroneously by xsl:copy-element and unnecessarily duplicated in Printer
#
# Revision 1.14  2000/08/17 06:31:08  uogbuji
# Update SplitQName to simplify usage
# Fix namespace declaration namespaces acc to May DOM CR
#
# Revision 1.13  2000/07/13 23:09:14  uogbuji
# Printer and reader fixes
#
# Revision 1.12  2000/07/13 19:47:25  uogbuji
# Use wstring for encodings: much broader support
#
# Revision 1.11  2000/07/12 05:29:52  molson
# Modified to use only the DOM interface
#
# Revision 1.10  2000/07/09 19:02:20  uogbuji
# Begin implementing Events
# bug-fixes
#
# Revision 1.9  2000/07/03 02:12:53  jkloth
#
# fixed up/improved cloneNode
# changed Document to handle DTS as children
# fixed miscellaneous bugs
#
# Revision 1.8  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.7  2000/06/05 14:56:45  uogbuji
# Improve XSLT stage test
# Add proper UTF-8 and ISO-8859-1 encoding support
# Improve XPath stringvalue for number
#
# Revision 1.6  2000/05/24 18:39:20  jkloth
# Added default single-line element support to (Pretty)Print
#
# Revision 1.5  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.4  2000/05/10 00:51:00  uogbuji
# Resurrect fixes to HTML reader and printer.
#
# Revision 1.3  2000/05/04 00:35:53  pweinstein
# Changing Ft.Dom.Html to xml.dom.html
#
# Revision 1.2  2000/04/27 19:08:49  jkloth
# fixed imports for xml-sig
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.46  2000/04/19 17:31:51  uogbuji
# Minor fixes to Printer UTF8 handling
# Added Eivind Tagseth's patch for reader/HtmlLib.py
#
# Revision 1.45  2000/04/19 03:59:44  uogbuji
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
# Revision 1.44  2000/03/13 07:05:14  molson
# Fixed bug in Pretty Print of plain elements
#
# Revision 1.43  2000/03/06 03:32:36  uche
# Complete wrapping of XSLT exceptions
# Add Syntax/Semantic exception support to XPattern parser
# Fix UTF-8 printing in DOM
# Fix memory leak with variables and parameters and RTFs in XSLT
# Bug-fixes
#
# Revision 1.42  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.41  2000/02/21 05:56:35  molson
# Fixed an ugly bug in the printing of attributes
#
# Revision 1.40  2000/02/18 16:23:08  uche
# More HTML white-space fixes
# Implemented xsl:number
# bug-fixes
#
# Revision 1.39  2000/02/17 15:02:28  uche
# Fix whitespace issues in printer.
#
# Revision 1.38  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.37  1999/12/27 07:07:03  uche
# Added Evaluate, Compile and CreateContext for XPath API
# Added template priority
# Updated XSL builtins, including mode support
# Removed extra spacing about attribute printing
# Fixed many bugs
#
# Revision 1.36  1999/12/18 22:54:51  uche
# Fix Namespaces to Match DOM Level 2 spec.
# Bug-fixes.
#
# Revision 1.35  1999/12/17 23:24:11  uche
# Began testing using xsl-list messages and fixed many bugs consequently.
#
# Revision 1.34  1999/12/16 20:22:25  molson
# Fixed some bugs
#
# Revision 1.33  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.32  1999/12/10 18:48:48  uche
# Added Copyright files to all packages
# Added HTML pseudo-SAX engine for 4XSLT
# Added xsl:output
# Various bug-fixes.
#
# Revision 1.31  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.30  1999/11/19 01:32:41  uche
# Python/DOM binding changes.
#
# Revision 1.29  1999/11/18 09:30:02  uche
# Python/DOM binding update.
#
# Revision 1.28  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.27  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
#
# Revision 1.26  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.25  1999/09/14 14:46:57  uche
# Remove &quot; from text escaping.
# Update changelog.
#
# Revision 1.24  1999/09/10 22:12:38  uche
# Added treewalker test
# Fixed serious problems with PrettyPrint
#
# Revision 1.23  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.22  1999/09/08 23:54:07  uche
# Add machinery for updated DOM Level 2 Iterators and Filters (untested)
#
# Revision 1.21  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
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
    import codecs                     #will fail on 1.5
    from types import UnicodeType
    def utf8_to_code(text, encoding):
        encoder = codecs.lookup(encoding)[0]       # encode,decode,reader,writer
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
    apos_count = string.find(characters, "'")
    quot_count = string.find(characters, '"')
    if apos_count > quot_count:
        delimiter = '"'
        new_chars = string.replace(characters, '"', '&quot;')
    else:
        delimiter = "'"
        new_chars = string.replace(characters, "'", '&apos;')
    #FIXME: There's more to normalization
    #Convert attribute new-lines to character entity
    new_chars = re.sub('\n', '&#10;', new_chars)
    return new_chars, delimiter


#Note: UCS-2 only for now
def TranslateCdata(characters, encoding='UTF-8', prev_chars='', markupSafe=0):
    if not characters:
        return ''
    if not markupSafe:
        new_string, num_subst = re.subn(
            g_cdataCharPattern,
            lambda m, d=g_charToEntity: d[m.group()],
            characters
            )
        if prev_chars[-2:] == ']]' and characters[0] == '>':
            new_string = '&gt;' + new_string[1:]
    else:
        new_string = characters
    #Note: use decimal char entity rep because some browsers are broken
    #FIXME: This will bomb for high characters.  Should, for instance, detect
    #The UTF-8 for 0xFFFE and put out &#xFFFE;
    new_string, num_subst = re.subn(XML_ILLEGAL_CHAR_PATTERN, lambda m: '&#%i;'%ord(m.group()), new_string)
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

    def visitDocument(self, node):
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

