########################################################################
#
# File Name:            HTMLMetaElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLMetaElement.html
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

class HTMLMetaElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="META"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_content(self):
        return self.getAttribute("CONTENT")

    def _set_content(self, value):
        self.setAttribute("CONTENT", value)

    def _get_httpEquiv(self):
        return self.getAttribute("HTTP-EQUIV")

    def _set_httpEquiv(self, value):
        self.setAttribute("HTTP-EQUIV", value)

    def _get_name(self):
        return self.getAttribute("NAME")

    def _set_name(self, value):
        self.setAttribute("NAME", value)

    def _get_scheme(self):
        return self.getAttribute("SCHEME")

    def _set_scheme(self, value):
        self.setAttribute("SCHEME", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "content" : _get_content,
        "httpEquiv" : _get_httpEquiv,
        "name" : _get_name,
        "scheme" : _get_scheme
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "content" : _set_content,
        "httpEquiv" : _set_httpEquiv,
        "name" : _set_name,
        "scheme" : _set_scheme
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

