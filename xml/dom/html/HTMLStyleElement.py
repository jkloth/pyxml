########################################################################
#
# File Name:            HTMLStyleElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLStyleElement.html
#

### This file is automatically generated by GenerateHtml.py.
### DO NOT EDIT!

"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import Node
from xml.dom.html.HTMLElement import HTMLElement

class HTMLStyleElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="STYLE"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_disabled(self):
        return self.hasAttribute("DISABLED")

    def _set_disabled(self, value):
        if value:
            self.setAttribute("DISABLED", "DISABLED")
        else:
            self.removeAttribute("DISABLED")

    def _get_media(self):
        return self.getAttribute("MEDIA")

    def _set_media(self, value):
        self.setAttribute("MEDIA", value)

    def _get_type(self):
        return self.getAttribute("TYPE")

    def _set_type(self, value):
        self.setAttribute("TYPE", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "disabled" : _get_disabled,
        "media" : _get_media,
        "type" : _get_type
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "disabled" : _set_disabled,
        "media" : _set_media,
        "type" : _set_type
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

