########################################################################
#
# File Name:            HTMLImageElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLImageElement.py.html
#
# History:
# $Log: HTMLImageElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.20  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.19  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.18  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.17  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.16  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.14  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.13  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.12  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.11  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
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

rwattrs = ('lowSrc', 'align', 'alt', 'border', 'height', 'hspace', 'isMap', 'longDesc', 'src', 'useMap', 'vspace', 'width')

class HTMLImageElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='IMG'):
        HTMLElement.__init__(self, ownerDocument, "IMG", nodeName)

    def _get_lowSrc(self):
        return self.getAttribute('LOWSRC')

    def _set_lowSrc(self,lowsrc):
        self.setAttribute('LOWSRC',lowsrc)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_alt(self):
        return self.getAttribute('ALT')

    def _set_alt(self,alt):
        self.setAttribute('ALT',alt)

    def _get_border(self):
        return self.getAttribute('BORDER')

    def _set_border(self,border):
        self.setAttribute('BORDER',border)

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_hspace(self):
        return self.getAttribute('HSPACE')

    def _set_hspace(self,hspace):
        self.setAttribute('HSPACE',hspace)

    def _get_isMap(self):
        return (self.getAttributeNode('ISMAP') and 1) or 0

    def _set_isMap(self,ismap):
        if ismap:
            self.setAttribute('ISMAP', '1')
        else:
            self.removeAttribute('ISMAP')

    def _get_longDesc(self):
        return self.getAttribute('LONGDESC')

    def _set_longDesc(self,longdesc):
        self.setAttribute('LONGDESC',longdesc)

    def _get_src(self):
        return self.getAttribute('SRC')

    def _set_src(self,src):
        self.setAttribute('SRC',src)

    def _get_useMap(self):
        return self.getAttribute('USEMAP')

    def _set_useMap(self,usemap):
        self.setAttribute('USEMAP',usemap)

    def _get_vspace(self):
        return self.getAttribute('VSPACE')

    def _set_vspace(self,vspace):
        self.setAttribute('VSPACE',vspace)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self,width):
        self.setAttribute('WIDTH',width)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'lowSrc'        : _get_lowSrc, 
         'align'         : _get_align, 
         'alt'           : _get_alt, 
         'border'        : _get_border, 
         'height'        : _get_height, 
         'hspace'        : _get_hspace, 
         'isMap'         : _get_isMap, 
         'longDesc'      : _get_longDesc, 
         'src'           : _get_src, 
         'useMap'        : _get_useMap, 
         'vspace'        : _get_vspace, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'lowSrc'        : _set_lowSrc, 
         'align'         : _set_align, 
         'alt'           : _set_alt, 
         'border'        : _set_border, 
         'height'        : _set_height, 
         'hspace'        : _set_hspace, 
         'isMap'         : _set_isMap, 
         'longDesc'      : _set_longDesc, 
         'src'           : _set_src, 
         'useMap'        : _set_useMap, 
         'vspace'        : _set_vspace, 
         'width'         : _set_width, 
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

#--- (end HTMLImageElement.py) ---
