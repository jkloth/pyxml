########################################################################
#
# File Name:            HTMLLinkElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLLinkElement.py.html
#
# History:
# $Log: HTMLLinkElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.19  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.18  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.17  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.16  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.15  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.13  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.12  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.11  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.10  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
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

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.Node import Node

rwattrs = ('disabled', 'charSet', 'href', 'hrefLang', 'media', 'rel', 'rev', 'target', 'type')

class HTMLLinkElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='LINK'):
        HTMLElement.__init__(self, ownerDocument, "LINK", nodeName)

    def _get_disabled(self):
        if self.getAttributeNode('DISABLED'):
            return 1
        return 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED','')
        else:
            self.removeAttribute('DISABLED')

    def _get_charSet(self):
        return self.getAttribute('CHARSET')

    def _set_charSet(self,charset):
        self.setAttribute('CHARSET',charset)

    def _get_href(self):
        return self.getAttribute('HREF')

    def _set_href(self,href):
        self.setAttribute('HREF',href)

    def _get_hrefLang(self):
        return self.getAttribute('HREFLANG')

    def _set_hrefLang(self,hreflang):
        self.setAttribute('HREFLANG',hreflang)

    def _get_media(self):
        return self.getAttribute('MEDIA')

    def _set_media(self,media):
        self.setAttribute('MEDIA',media)

    def _get_rel(self):
        return self.getAttribute('REL')

    def _set_rel(self,rel):
        self.setAttribute('REL',rel)

    def _get_rev(self):
        return self.getAttribute('REV')

    def _set_rev(self,rev):
        self.setAttribute('REV',rev)

    def _get_target(self):
        return self.getAttribute('TARGET')

    def _set_target(self,target):
        self.setAttribute('TARGET',target)

    def _get_type(self):
        return self.getAttribute('TYPE')

    def _set_type(self,typ):
        self.setAttribute('TYPE',typ)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'disabled'      : _get_disabled, 
         'charSet'       : _get_charSet, 
         'href'          : _get_href, 
         'hrefLang'      : _get_hrefLang, 
         'media'         : _get_media, 
         'rel'           : _get_rel, 
         'rev'           : _get_rev, 
         'target'        : _get_target, 
         'type'          : _get_type, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'disabled'      : _set_disabled, 
         'charSet'       : _set_charSet, 
         'href'          : _set_href, 
         'hrefLang'      : _set_hrefLang, 
         'media'         : _set_media, 
         'rel'           : _set_rel, 
         'rev'           : _set_rev, 
         'target'        : _set_target, 
         'type'          : _set_type, 
      }) 

    # Create the read-only list of attributes 
    _readOnlyAttrs = [] 
    for attr in HTMLElement._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

#--- (end HTMLLinkElement.py) ---
