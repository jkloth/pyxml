########################################################################
#
# File Name:            HTMLIFrameElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLIFrameElement.py.html
#
# History:
# $Log: HTMLIFrameElement.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:53  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.19  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
#
# Revision 1.18  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.17  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.16  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.15  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.14  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.12  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.11  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.10  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.9  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.8  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import string
from xml.dom.html.HTMLElement import HTMLElement

class HTMLIFrameElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName="IFRAME"):
        HTMLElement.__init__(self, ownerDocument, nodeName)
        self.__content = None

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute("ALIGN"))

    def _set_align(self, value):
        self.setAttribute("ALIGN", value)

    def _get_contentDocument(self):
        if not self.__content:
            source = self._get_src()
            import os.path
            ext = os.path.splitext(source)
            if string.find(ext, 'htm') > 0:
                from xml.dom.ext.reader import HtmlLib
                self.__content = HtmlLib.FromHtmlUrl(source)
            elif string.lower(ext) == '.xml':
                from xml.dom.ext.reader import Sax2
                self.__content = Sax2.FromXmlUrl(source)
        return self.__content

    def _get_frameBorder(self):
        return string.capitalize(self.getAttribute("FRAMEBORDER"))

    def _set_frameBorder(self, value):
        self.setAttribute("FRAMEBORDER", value)

    def _get_height(self):
        return self.getAttribute("HEIGHT")

    def _set_height(self, value):
        self.setAttribute("HEIGHT", value)

    def _get_longDesc(self):
        return self.getAttribute("LONGDESC")

    def _set_longDesc(self, value):
        self.setAttribute("LONGDESC", value)

    def _get_marginHeight(self):
        return self.getAttribute("MARGINHEIGHT")

    def _set_marginHeight(self, value):
        self.setAttribute("MARGINHEIGHT", value)

    def _get_marginWidth(self):
        return self.getAttribute("MARGINWIDTH")

    def _set_marginWidth(self, value):
        self.setAttribute("MARGINWIDTH", value)

    def _get_name(self):
        return self.getAttribute("NAME")

    def _set_name(self, value):
        self.setAttribute("NAME", value)

    def _get_scrolling(self):
        return string.capitalize(self.getAttribute("SCROLLING"))

    def _set_scrolling(self, value):
        self.setAttribute("SCROLLING", value)

    def _get_src(self):
        return self.getAttribute("SRC")

    def _set_src(self, value):
        self.setAttribute("SRC", value)

    def _get_Width(self):
        return self.getAttribute("WIDTH")

    def _set_Width(self, value):
        self.setAttribute("WIDTH", value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update({
        "align" : _get_align,
        "contentDocument" : _get_contentDocument,
        "frameBorder" : _get_frameBorder,
        "height" : _get_height,
        "longDesc" : _get_longDesc,
        "marginHeight" : _get_marginHeight,
        "marginWidth" : _get_marginWidth,
        "name" : _get_name,
        "scrolling" : _get_scrolling,
        "src" : _get_src,
        "Width" : _get_Width
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        "align" : _set_align,
        "frameBorder" : _set_frameBorder,
        "height" : _set_height,
        "longDesc" : _set_longDesc,
        "marginHeight" : _set_marginHeight,
        "marginWidth" : _set_marginWidth,
        "name" : _set_name,
        "scrolling" : _set_scrolling,
        "src" : _set_src,
        "Width" : _set_Width
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())

