########################################################################
#
# File Name:            HTMLTableColElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableColElement.py.html
#
# History:
# $Log: HTMLTableColElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.18  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.17  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.16  2000/05/06 09:12:19  jkloth
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

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import string
from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.Node import Node

rwattrs = ('align', 'ch', 'chOff', 'span', 'vAlign', 'width')

class HTMLTableColElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='COL'):
        HTMLElement.__init__(self, ownerDocument, string.upper(nodeName), nodeName)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_ch(self):
        return self.getAttribute('CH')

    def _set_ch(self,ch):
        self.setAttribute('CH',ch)

    def _get_chOff(self):
        return self.getAttribute('CHOFF')

    def _set_chOff(self,choff):
        self.setAttribute('CHOFF',choff)

    def _get_span(self):
        return int(self.getAttribute('SPAN'))

    def _set_span(self,span):
        self.setAttribute('SPAN',str(span))

    def _get_vAlign(self):
        return self.getAttribute('VALIGN')

    def _set_vAlign(self,valign):
        self.setAttribute('VALIGN',valign)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self,width):
        self.setAttribute('WIDTH',width)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'align'         : _get_align, 
         'ch'            : _get_ch, 
         'chOff'         : _get_chOff, 
         'span'          : _get_span, 
         'vAlign'        : _get_vAlign, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'align'         : _set_align, 
         'ch'            : _set_ch, 
         'chOff'         : _set_chOff, 
         'span'          : _set_span, 
         'vAlign'        : _set_vAlign, 
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

#--- (end HTMLTableColElement.py) ---
