########################################################################
#
# File Name:            HTMLTableSectionElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableSectionElement.py.html
#
# History:
# $Log: HTMLTableSectionElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
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

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import string
from xml.dom import implementation
from xml.dom.Node import Node
from xml.dom.html.HTMLElement import HTMLElement

rwattrs = ('align', 'ch', 'chOff', 'vAlign')
rattrs = ('rows',)

class HTMLTableSectionElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName):
        HTMLElement.__init__(self, ownerDocument, string.upper(nodeName), nodeName)

    def _get_rows(self):
        rows = []
        #children = self.getChildNodes()
        #for ctr in range(children.getLength()):
        #   child = children.item(ctr)
        for child in self.childNodes:
            if child.tagName == 'TR':
                rows.append(child)
        return implementation._4dom_createHTMLCollection(rows)

    def insertRow(self,index):
        if index < 0:
            return None
        rows = self._get_rows()
        tr = None
        if len(rows) == index:
            tr = self.ownerDocument.createElement('TR')
            self.appendChild(tr)
        elif len(rows) > index:
            tr = self.ownerDocument.createElement('TR')
            self.insertBefore(tr, rows[index])
        else:
            for ctr in range(len(rows),index+1):
                tr = self.ownerDocument.createElement('TR')
                self.appendChild(tr)
        return tr

    def deleteRow(self,index):
        if index < 0:
            return
        rows = self._get_rows()
        if len(rows) > index:
            rows[index].parentNode.removeChild(rows[index])

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

    def _get_vAlign(self):
        return self.getAttribute('VALIGN')

    def _set_vAlign(self,valign):
        self.setAttribute('VALIGN',valign)

#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

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
    _readOnlyAttrs = [] 
    for attr in HTMLElement._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

#--- (end HTMLTableSectionElement.py) ---
