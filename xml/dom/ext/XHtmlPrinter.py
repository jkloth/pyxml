import string
from xml.dom import ext, XMLNS_NAMESPACE

from xml.dom.ext import Printer
from xml.dom.Node import Node

class XHtmlPrintVisitor(Printer.PrintVisitor):

    def __init__(self, stream, encoding, indent, newLine):
        self._encoding = encoding
        self._indent = indent
        self._depth = 0
        self._newLine = newLine
        self._prevNodeIsText = 0
        self._stream = stream
        self._nssPrint = 1
        self._inPre = 0
        Printer.PrintVisitor.__init__(self,stream,encoding,None)
        return

    def visitDocument(self,node):
        self.visitProlog()
        self._stream.write(self._newLine)
        self._stream.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">')
        self._stream.write(self._newLine)
        Printer.PrintVisitor.visitDocument(self,node)
    


    def visitText(self,node):
        if not self._inPre and self._newLine:
            newData = string.strip(node.data)
            self._prevNodeIsText = len(newData) > 0.
            self.stream.write(Printer.TranslateCdata(newData, self.encoding))
        else:
            self._prevNodeIsText = 1
            Printer.PrintVisitor.visitText(self,node)


    def visitAttr(self, node):
        testFunc = 'visit%sAttr' % string.upper(node.nodeName)
        if hasattr(self,testFunc):
            func = getattr(self,testFunc)
            return apply(func,(node,))

        if node.namespaceURI == XMLNS_NAMESPACE:
            return
        text = Printer.TranslateCdata(node.value, self.encoding)
        text, delimiter = Printer.TranslateCdataAttr(text)
        st = " %s=%s%s%s" % (string.lower(node.name), delimiter, text, delimiter)
        self.stream.write(st)
        return


    def visitElement(self, node):
        testFunc = 'visit%sElement' % string.upper(node.nodeName)
        if hasattr(self,testFunc):
            func = getattr(self,testFunc)
            return apply(func,(node,))

        if self._prevNodeIsText:
            self._prevNodeIsText = 0
            self.stream.write('<' + string.lower(node.localName))
        else:
            self.stream.write(self._newLine + self._indent*self._depth + '<' + string.lower(node.localName))
        if self._nssPrint:
            self._nssPrint = 0
            self.stream.write(" xmlns = 'http://www.w3.org/1999/xhtml'")

        self.visitNamedNodeMap(node.attributes)
        st = ''
        if len(node.childNodes):
            self.stream.write('>')
            self._depth = self._depth + 1
            self.visitNodeList(node.childNodes)
            self._depth = self._depth - 1
            if self._prevNodeIsText:
                self._prevNodeIsText = 0
                self.stream.write('</' + string.lower(node.localName) + '>')
            else:
                self.stream.write(self._newLine + self._indent*self._depth + '</' + string.lower(node.localName) + '>')
        else:
            self.stream.write('/>')
        return
