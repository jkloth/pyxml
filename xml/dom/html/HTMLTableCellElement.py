########################################################################
#
# File Name:            HTMLTableCellElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableCellElement.py.html
#
# History:
# $Log: HTMLTableCellElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.24  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.23  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.22  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.21  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.20  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.18  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.17  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.16  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.15  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.14  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.13  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.12  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.11  1999/08/29 04:08:00  uche
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
from xml.dom import ext

rwattrs = ('cellIndex', 'abbr', 'align', 'axis', 'bgColor', 'ch', 'chOff', 'colSpan', 'headers', 'height', 'noWrap', 'rowSpan', 'scope', 'vAlign', 'width')

class HTMLTableCellElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='TD'):
        HTMLElement.__init__(self, ownerDocument, string.upper(nodeName), nodeName)

    def _get_cellIndex(self):
        #We need to find the TR we are in
        if self.parentNode == None:
            return -1
        cells = self.parentNode._get_cells()
        return cells.index(self)

    def _set_cellIndex(self,index):
        #FIXME: not clear how to implement this.
        pass

    def _get_abbr(self):
        return self.getAttribute('ABBR')

    def _set_abbr(self,abbr):
        self.setAttribute('ABBR',abbr)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_axis(self):
        return self.getAttribute('AXIS')

    def _set_axis(self,axis):
        self.setAttribute('AXIS',axis)

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self,bgcolor):
        self.setAttribute('BGCOLOR',bgcolor)

    def _get_ch(self):
        return self.getAttribute('CH')

    def _set_ch(self,ch):
        self.setAttribute('CH',ch)

    def _get_chOff(self):
        return self.getAttribute('CHOFF')

    def _set_chOff(self,choff):
        self.setAttribute('CHOFF',choff)

    def _get_colSpan(self):
        return int(self.getAttribute('COLSPAN'))

    def _set_colSpan(self,colspan):
        self.setAttribute('COLSPAN',str(colspan))

    def _get_headers(self):
        return self.getAttribute('HEADERS')

    def _set_headers(self,headers):
        self.setAttribute('HEADERS',headers)

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_noWrap(self):
        return (self.getAttributeNode('NOWRAP') and 1) or 0

    def _set_noWrap(self,nowrap):
        if nowrap:
            self.setAttribute('NOWRAP', '')
        else:
            self.removeAttribute('NOWRAP')

    def _get_rowSpan(self):
        return int(self.getAttribute('ROWSPAN'))

    def _set_rowSpan(self,rowspan):
        self.setAttribute('ROWSPAN',str(rowspan))

    def _get_scope(self):
        return self.getAttribute('SCOPE')

    def _set_scope(self,scope):
        self.setAttribute('SCOPE',scope)

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
         'cellIndex'     : _get_cellIndex, 
         'abbr'          : _get_abbr, 
         'align'         : _get_align, 
         'axis'          : _get_axis, 
         'bgColor'       : _get_bgColor, 
         'ch'            : _get_ch, 
         'chOff'         : _get_chOff, 
         'colSpan'       : _get_colSpan, 
         'headers'       : _get_headers, 
         'height'        : _get_height, 
         'noWrap'        : _get_noWrap, 
         'rowSpan'       : _get_rowSpan, 
         'scope'         : _get_scope, 
         'vAlign'        : _get_vAlign, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'cellIndex'     : _set_cellIndex, 
         'abbr'          : _set_abbr, 
         'align'         : _set_align, 
         'axis'          : _set_axis, 
         'bgColor'       : _set_bgColor, 
         'ch'            : _set_ch, 
         'chOff'         : _set_chOff, 
         'colSpan'       : _set_colSpan, 
         'headers'       : _set_headers, 
         'height'        : _set_height, 
         'noWrap'        : _set_noWrap, 
         'rowSpan'       : _set_rowSpan, 
         'scope'         : _set_scope, 
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

#--- (end HTMLTableCellElement.py) ---
