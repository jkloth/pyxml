########################################################################
#
# File Name:            HTMLBRElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLBRElement.html
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

class HTMLBRElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="BR"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_clear(self):
        return string.capitalize(self.getAttribute("CLEAR"))

    def _set_clear(self, value):
        self.setAttribute("CLEAR", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "clear" : _get_clear
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "clear" : _set_clear
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

