########################################################################
#
# File Name:            HTMLTableSectionElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableSectionElement.py.html
#
# History:
# $Log: HTMLTableSectionElement.py,v $
# Revision 1.4  2000/09/27 23:45:26  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.27  2000/08/03 23:30:28  jkloth
# Cleaned up TraceOut stuff
# Fixed small bugs
#
# Revision 1.26  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
#
# Revision 1.25  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.24  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.23  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.22  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.21  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.19  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.18  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.17  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.16  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.15  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.14  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.13  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.12  1999/08/29 04:08:00  uche
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
from xml.dom import implementation
from xml.dom.html.HTMLElement import HTMLElement

class HTMLTableSectionElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_ch(self):
        return self.getAttribute('CHAR')

    def _set_ch(self,char):
        self.setAttribute('CHAR',char)

    def _get_chOff(self):
        return self.getAttribute('CHAROFF')

    def _set_chOff(self,offset):
        self.setAttribute('CHAROFF',offset)

    def _get_rows(self):
        rows = []
        for child in self.childNodes:
            if child.tagName == 'TR':
                rows.append(child)
        return implementation._4dom_createHTMLCollection(rows)

    def _get_vAlign(self):
        return string.capitalize(self.getAttribute('VALIGN'))

    def _set_vAlign(self,valign):
        self.setAttribute('VALIGN',valign)

    ### Methods ###

    def deleteRow(self,index):
        rows = self._get_rows()
        if index < 0 or index > len(rows):
            raise DOMException(INDEX_SIZE_ERR)
        rows[index].parentNode.removeChild(rows[index])

    def insertRow(self,index):
        rows = self._get_rows()
        if index < 0 or index >= len(rows):
            raise DOMException(INDEX_SIZE_ERR)
        rows = self._get_rows()
        newRow = self.ownerDocument.createElement('TR')
        if index == len(rows):
            ref = None
        else:
            ref = rows[index]
        return self.insertBefore(newRow, ref)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'rows'          : _get_rows,
         'align'         : _get_align,
         'ch'            : _get_ch,
         'chOff'         : _get_chOff,
         'vAlign'        : _get_vAlign,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'align'         : _set_align,
         'ch'            : _set_ch,
         'chOff'         : _set_chOff,
         'vAlign'        : _set_vAlign,
      })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
