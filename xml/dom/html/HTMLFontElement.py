########################################################################
#
# File Name:            HTMLFontElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLFontElement.html
#

### This file is automatically generated by GenerateHtml.py.
### DO NOT EDIT!

"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom.Node import Node
from xml.dom.html.HTMLElement import HTMLElement

class HTMLFontElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="FONT"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_color(self):
        return self.getAttribute("COLOR")

    def _set_color(self, value):
        self.setAttribute("COLOR", value)

    def _get_face(self):
        return self.getAttribute("FACE")

    def _set_face(self, value):
        self.setAttribute("FACE", value)

    def _get_size(self):
        return self.getAttribute("SIZE")

    def _set_size(self, value):
        self.setAttribute("SIZE", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "color" : _get_color,
        "face" : _get_face,
        "size" : _get_size
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "color" : _set_color,
        "face" : _set_face,
        "size" : _set_size
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

