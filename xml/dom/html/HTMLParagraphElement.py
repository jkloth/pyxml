########################################################################
#
# File Name:            HTMLParagraphElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLParagraphElement.html
#

### This file is automatically generated by GenerateHtml.py.
### DO NOT EDIT!

"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom.html.HTMLElement import HTMLElement

class HTMLParagraphElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="P"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute("ALIGN"))

    def _set_align(self, value):
        self.setAttribute("ALIGN", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "align" : _get_align
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "align" : _set_align
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

