########################################################################
#
# File Name:            HTMLHeadElement
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLHeadElement.html
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

class HTMLHeadElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="HEAD"):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_profile(self):
        return self.getAttribute("PROFILE")

    def _set_profile(self, value):
        self.setAttribute("PROFILE", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "profile" : _get_profile
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "profile" : _set_profile
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

