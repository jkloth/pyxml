########################################################################
#
# File Name:            Printer.py
#
# Documentation:        http://docs.4suite.com/4DOM/Printer.py.html
#
# History:
# $Log: Printer.py,v $
# Revision 1.3  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
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
from xml.dom import Node
from xml.dom.ext.Visitor import Visitor, WalkerInterface
from xml.dom import ext
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE, HTML_FORBIDDEN_END

g_xmlIllegalCharPattern = re.compile('[\x01-\x08\x0B-\x0D\x0E-\x1F\x80-\xFF]')
g_utf8TwoBytePattern = re.compile('([\xC0-\xC3])([\x80-\xBF])')
g_cdataCharPattern = re.compile('[&<\'\"]')
g_textCharPattern = re.compile('[&<]')
g_charToEntity = {
        '&': '&amp;',
        '<': '&lt;',
        "'": '&apos;',
        '"': '&quot;'
        }


def TranslateCdata(text, encoding='UTF-8'):
    encoding = string.upper(encoding)
    new_string, num_subst = re.subn(g_cdataCharPattern, lambda m, d=g_charToEntity: d[m.group()], text)
    #Convert attribute new-lines to character entity
    new_string = re.sub('\n', '&#10;', new_string)
    if encoding == 'UTF-8':
        pass
    elif encoding == 'ISO-8859-1':
        new_string, num_subst = re.subn(g_utf8TwoBytePattern, lambda m: chr(((int(ord(m.group(1))) & 0x03) << 6) | (int(ord(m.group(2))) & 0x3F)), new_string)
    else:
        raise Exception('Unsupported output encoding')
    #Note: use decimal char entity rep because some browsers are broken
    new_string, num_subst = re.subn(g_xmlIllegalCharPattern, lambda m: '&#%i;'%ord(m.group()), new_string)
    return new_string


def TranslateText(text, encoding='UTF-8'):
    encoding = string.upper(encoding)
    new_string, num_subst = re.subn(g_textCharPattern, lambda m, d=g_charToEntity: d[m.group()], text)
    if encoding == 'UTF-8':
        pass
    elif encoding == 'ISO-8859-1':
        new_string, num_subst = re.subn(g_utf8TwoBytePattern, lambda m: chr(((int(ord(m.group(1))) & 0x03) << 6) | (int(ord(m.group(2))) & 0x3F)), new_string)
    else:
        raise Exception('Unsupported output encoding')
    #Note: use decimal char entity rep because some browsers are broken
    new_string, num_subst = re.subn(g_xmlIllegalCharPattern, lambda m: '&#%i;'%ord(m.group()), new_string)
    return new_string


class PrintVisitor(Visitor):
    def __init__(self):
        self.__namespaces = [{}]

    def visit(self, node):
        #call the appropriate method
        try:
            interface_name = ext.NodeTypeToClassName(node.nodeType)
        except AttributeError:
            if hasattr(node, "getNamedItem"):
                interface_name = "NamedNodeMap"
            else:
                interface_name = "NodeList"
        st = eval("self.visit%s(node)"%(interface_name))
        return st

    def visitNode(self, node):
        return self.visit(node.childNodes)

    def visitNodeList(self, node):
        st = ""
        for curr in node:
            st = st + self.visit(curr)
        return st

    def visitNamedNodeMap(self, node):
        st = ''
        for item in node:
            st = st + self.visit(item) + ' '
        if st and st[-1] == ' ':
            st = st[:-1]
        return st

    def visitAttr(self, node):
        name_parts = ext.SplitQName(node.nodeName)
        if name_parts == ('', 'xmlns') or name_parts[0] == 'xmlns':
            return ''
        if node.ownerDocument.isHtml() and len(node.childNodes) == 0:
            st = node.nodeName
        else:
            st = "%s='%s'" % (node.nodeName, TranslateCdata(node.value))
        return st

    def visitDocument(self, node):
        if node.doctype != None:
            st = self.visit(node.doctype)
        else:
            st = ""
        st = st + self.visitNode(node)
        return st

    def visitDocumentFragment(self, node):
        return self.visit(node.childNodes)

    def visitElement(self, node):
        self.__namespaces.append(self.__namespaces[-1].copy())
        st = "<%s " % (node.tagName)
        if node.ownerDocument.isXml():
            nss = ext.GetAllNs(node)
            del nss['xml']
        else:
            nss = {}
        for prefix in nss.keys():
            if not self.__namespaces[-1].has_key(prefix) or self.__namespaces[-1][prefix] != nss[prefix]:
                if prefix:
                    st = st + 'xmlns:' + prefix + " = '" + nss[prefix] + "' "
                else:
                    st = st + 'xmlns' + " = '" + nss[prefix] + "' "
            self.__namespaces[-1][prefix] = nss[prefix]
        st = st + self.visit(node.attributes)
        st = string.rstrip(st)
        if len(node.childNodes):
            st = st + '>'
            st = st + self.visitNode(node)
            if node.ownerDocument.isXml() or (node.tagName not in HTML_FORBIDDEN_END):
                st = st + '</%s>' % (node.tagName)
        elif node.ownerDocument.isXml():
            st = st + '/>'
        elif node.tagName not in HTML_FORBIDDEN_END:
            st = st + '></%s>' % (node.tagName)
        else:
            st = st + '>'
        del self.__namespaces[-1]
        return st

    def visitText(self, node):
        return TranslateText(node.data)

    def visitDocumentType(self, node):
        st = ''
        if node.systemId != '':
            st = "<!DOCTYPE %s" % (node.name)
            if node.publicId != '':
                st = st + ' PUBLIC "%s" ' % node.publicId
            st = st + ' SYSTEM "%s" ' % node.systemId
            if node.entities.length or node.notations.length:
                st = st + "[" + self.visit(node.entities) + self.visit(node.notations) + "]"
            st = st + ">"
        return st

    def visitEntity(self, node):
        st = "<!ENTITY %s "%(node.nodeName)
        if (node.publicId):
            st = st + "PUBLIC %s "%(node.publicId)
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        if (node.notationName):
            st = st + "NDATA %s "%(node.notationName)
        return st + ">"

    def visitNotation(self, node):
        st = "<!NOTATION %s "%(node.nodeName)
        if (node.publicId):
            st = st + "PUBLIC %s "%(node.publicId)
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        return st + ">"

    def visitCDATASection(self, node):
        return "<![CDATA[%s]]>" % (node.data)

    def visitComment(self, node):
        return "<!--%s-->" % (node.data)

    def visitEntityReference(self, node):
        return "&%s;"%(node.nodeName)

    def visitProcessingInstruction(self, node):
        return "<?%s %s?>" % (node.target, node.data)


class PrettyPrintVisitor(Visitor):
    def __init__(self, indent, width, plainElements):
        self.__indent = indent
        self.__depth = 0
        self.__width = width
        self.__plainElements = plainElements
        self.__printPlain = 0
        self.__plainPrinter = PrintVisitor()
        self.__prevNodeIsText = 0
        self.__emptyReturn = 0
        self.__namespaces = [{}]

    def visit(self, node):
        #call the appropriate method
        try:
            class_name = ext.NodeTypeToClassName(node.nodeType)
        except AttributeError:
            if hasattr(node, "getNamedItem"):
                class_name = "NamedNodeMap"
            else:
                class_name = "NodeList"

        if self.__printPlain:
            func = getattr(self.__plainPrinter,'visit%s'%class_name)
        else:
            func = getattr(self,'visit%s'%class_name)
        st = func(node)
        return st

    def visitNode(self, node):
        return self.visit(node.childNodes)

    def visitNodeList(self, node):
        st = ""
        for n in node:
            st = st + self.visit(n)
        return st

    def visitNamedNodeMap(self, node):
        st = ''
        for item in node:
            st = st + self.visit(item) + ' '
        if st and st[-1] == ' ':
            st = st[:-1]
        return st

    def visitAttr(self, node):
        name_parts = ext.SplitQName(node.nodeName)
        if name_parts == ('', 'xmlns') or name_parts[0] == 'xmlns':
            return ''
        if node.ownerDocument.isHtml() and len(node.childNodes) == 0:
            st = node.nodeName
        else:
            st = "%s='%s'" % (node.nodeName, TranslateCdata(node.value))
        return st

    def visitDocument(self, node):
        #if node.docType != None:
        #    st = self.visit(node.docType)
        #else:
        #    st = ""
        st = self.visitNode(node)
        return st

    def visitDocumentFragment(self,node):
        return self.visit(node.childNodes)

    def visitElement(self, node):
        self.__namespaces.append(self.__namespaces[-1].copy())
        if node.tagName in self.__plainElements:
            #We don't want to insert whitespace into any flagged element
            #FIXME: handle xml:preserve?
            return self.visitPlainElement(node)
        if self.__prevNodeIsText or self.__emptyReturn:
            self.__prevNodeIsText = 0
            self.__emptyReturn = 0
            st = "<%s " % (node.tagName)
        else:
            st = "\n%s<%s " % (self.__indent*self.__depth, node.tagName)
        if node.ownerDocument.isXml():
            nss = ext.GetAllNs(node)
            del nss['xml']
        else:
            nss = {}
        for prefix in nss.keys():
            if not self.__namespaces[-1].has_key(prefix) or self.__namespaces[-1][prefix] != nss[prefix]:
                if prefix:
                    st = st + 'xmlns:' + prefix + " = '" + nss[prefix] + "' "
                else:
                    st = st + 'xmlns' + " = '" + nss[prefix] + "' "
            self.__namespaces[-1][prefix] = nss[prefix]
        st = st + self.visit(node.attributes)
        st = string.rstrip(st)
        if len(node.childNodes):
            st = st + '>'
            self.__depth = self.__depth + 1
            st = st + self.visitNode(node)
            self.__depth = self.__depth - 1
            if node.ownerDocument.isXml() or (node.tagName not in HTML_FORBIDDEN_END):
                if self.__prevNodeIsText:
                    self.__prevNodeIsText = 0
                    st = st + '</%s>' % (node.tagName)
                else:
                    st = st + '\n%s</%s>' % (self.__depth*self.__indent, node.tagName)
        elif node.ownerDocument.isXml():
            st = st + '/>'
        elif node.tagName not in HTML_FORBIDDEN_END:
            st = st + '></%s>' % (node.tagName)
        else:
            st = st + '>'
        del self.__namespaces[-1]
        return st

    def visitPlainElement(self, node):
        self.__printPlain = 1
        if self.__prevNodeIsText or self.__emptyReturn:
            self.__prevNodeIsText = 0
            self.__emptyReturn = 0
            st = "<%s " % (node.tagName)
        else:
            st = "\n%s<%s " % (self.__indent*self.__depth, node.tagName)
        st = st + self.visit(node.attributes)
        st = string.rstrip(st)
        if len(node.childNodes):
            st = st + '>'
            self.__depth = self.__depth + 1
            st = st + self.visitNode(node)
            self.__depth = self.__depth - 1
            if self.__prevNodeIsText:
                self.__prevNodeIsText = 0
                st = st + '</%s>' % (node.tagName)
            else:
                st = st + '\n%s</%s>' % (self.__depth*self.__indent, node.tagName)
        elif node.ownerDocument.isXml():
            st = st + '/>'
        elif node.tagName not in HTML_FORBIDDEN_END:
            st = st + '></%s>' % (node.tagName)
        else:
            st = st + '>'
        self.__printPlain = 0
        return st

    def visitText(self, node):
        self.__prevNodeIsText = 1
        return TranslateText(node.data)

    def visitDocumentType(self, node):
        st = ''
        self.__emptyReturn = 1
        if node.systemId != '':
            self.__emptyReturn = 0
            st = "<!DOCTYPE %s" % (node.name)
            if node.publicId != '':
                st = st + ' PUBLIC "%s" ' % node.publicId
            st = st + ' SYSTEM "%s" ' % node.systemId
            if node.entities.length or node.notations.length:
                st = st + "[" + self.visit(node.entities) + self.visit(node.notations) + "]"
            st = st + ">"
        return st

    def visitEntity(self, node):
        st = "<!ENTITY %s "%(node.nodeName)
        if (node.publicId()):
            st = st + "PUBLIC %s "%(node.publicId())
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        if (node.notationName):
            st = st + "NDATA %s "%(node.notationName)
        return st + ">"

    def visitNotation(self, node):
        st = "<!NOTATION %s "%(node.nodeName)
        if (node.publicId()):
            st = st + "PUBLIC %s "%(node.publicId())
        if (node.systemId):
            st = st + "SYSTEM %s "%(node.systemId)
        return st + ">"

    def visitCDATASection(self, node):
        return "<![CDATA[%s]]>" % (node.data)

    def visitComment(self, node):
        return "<!--%s-->\n" % (node.data)

    def visitProcessingInstruction(self, node):
        return "<?%s %s?>\n" % (node.target, node.data)

    def visitEntityReference(self, node):
        return "[Entity Refrence named %s]"%(node.nodeName)


class PrintWalker(WalkerInterface):
    def __init__(self, visitor, startNode):
        WalkerInterface.__init__(self, visitor)
        self.start_node = startNode
        return

    def step(self):
        """There is really no step to printing.  It prints the whole thing"""
        st = self.visitor.visit(self.start_node)
        return st

    def run(self):
        return self.step()


