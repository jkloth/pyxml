########################################################################
#
# File Name:            HTMLOListElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLOListElement.html
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

class HTMLOListElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="OL"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_compact(self):
        return self.hasAttribute("COMPACT")

    def _set_compact(self, value):
        if value:
            self.setAttribute("COMPACT", None)
        else:
            self.removeAttribute("COMPACT")

    def _get_start(self):
        value = self.getAttribute("START")
        if value:
            return int(value)
        return 0

    def _set_start(self, value):
        self.setAttribute("START", str(value))

    def _get_type(self):
        return self.getAttribute("TYPE")

    def _set_type(self, value):
        self.setAttribute("TYPE", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "compact" : _get_compact,
        "start" : _get_start,
        "type" : _get_type
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "compact" : _set_compact,
        "start" : _set_start,
        "type" : _set_type
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

