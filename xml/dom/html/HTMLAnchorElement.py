########################################################################
#
# File Name:            HTMLAnchorElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLAnchorElement.html
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

class HTMLAnchorElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="A"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_accessKey(self):
        return self.getAttribute("ACCESSKEY")

    def _set_accessKey(self, value):
        self.setAttribute("ACCESSKEY", value)

    def _get_charset(self):
        return self.getAttribute("CHARSET")

    def _set_charset(self, value):
        self.setAttribute("CHARSET", value)

    def _get_coords(self):
        return self.getAttribute("COORDS")

    def _set_coords(self, value):
        self.setAttribute("COORDS", value)

    def _get_href(self):
        return self.getAttribute("HREF")

    def _set_href(self, value):
        self.setAttribute("HREF", value)

    def _get_hreflang(self):
        return self.getAttribute("HREFLANG")

    def _set_hreflang(self, value):
        self.setAttribute("HREFLANG", value)

    def _get_name(self):
        return self.getAttribute("NAME")

    def _set_name(self, value):
        self.setAttribute("NAME", value)

    def _get_rel(self):
        return self.getAttribute("REL")

    def _set_rel(self, value):
        self.setAttribute("REL", value)

    def _get_rev(self):
        return self.getAttribute("REV")

    def _set_rev(self, value):
        self.setAttribute("REV", value)

    def _get_shape(self):
        return string.capitalize(self.getAttribute("SHAPE"))

    def _set_shape(self, value):
        self.setAttribute("SHAPE", value)

    def _get_tabIndex(self):
        value = self.getAttribute("TABINDEX")
        if value:
            return int(value)
        return 0

    def _set_tabIndex(self, value):
        self.setAttribute("TABINDEX", str(value))

    def _get_target(self):
        return self.getAttribute("TARGET")

    def _set_target(self, value):
        self.setAttribute("TARGET", value)

    def _get_type(self):
        return self.getAttribute("TYPE")

    def _set_type(self, value):
        self.setAttribute("TYPE", value)

    ### Methods ###

    def blur(self):
        pass

    def focus(self):
        pass

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "accessKey" : _get_accessKey,
        "charset" : _get_charset,
        "coords" : _get_coords,
        "href" : _get_href,
        "hreflang" : _get_hreflang,
        "name" : _get_name,
        "rel" : _get_rel,
        "rev" : _get_rev,
        "shape" : _get_shape,
        "tabIndex" : _get_tabIndex,
        "target" : _get_target,
        "type" : _get_type
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "accessKey" : _set_accessKey,
        "charset" : _set_charset,
        "coords" : _set_coords,
        "href" : _set_href,
        "hreflang" : _set_hreflang,
        "name" : _set_name,
        "rel" : _set_rel,
        "rev" : _set_rev,
        "shape" : _set_shape,
        "tabIndex" : _set_tabIndex,
        "target" : _set_target,
        "type" : _set_type
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

