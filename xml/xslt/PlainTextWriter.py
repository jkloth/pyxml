########################################################################
#
# File Name:            PlainTextWriter.py
#
# Documentation:        http://docs.4suite.com/4XSLT/PlainTextWriter.py.html
#
"""
Implements a text output writer for XSLT processor output
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xslt import NullWriter
from xml.dom.ext.Printer import utf8_to_code

class PlainTextWriter(NullWriter.NullWriter):
    def __init__(self, outputParams, stream=None):
        NullWriter.NullWriter.__init__(self, outputParams, stream)
        self._mediaType = outputParams.mediaType or 'text/plain'
        self._encoding = outputParams.encoding
        
    def getMediaType(self):
        return self._mediaType
  
    def startDocument(self):
        return

    def endDocument(self):
        return
    
    def text(self, text, escapeOutput=1):
        if self._encoding:
            self._stream.write(utf8_to_code(text, self._encoding))
        else:
            # Defaults to UTF-8
            self._stream.write(text)
    
    def attribute(self, name, value, namespace=''):
        return

    def processingInstruction(self, target, data):
        return

    def comment(self, body):
        return

    def startElement(self, name, namespace='', extraNss=None):
        return

    def endElement(self, name):
        return
