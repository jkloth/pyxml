########################################################################
#
# File Name:            HTMLTableRowElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableRowElement.py.html
#
# History:
# $Log: HTMLTableRowElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.28  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.27  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.26  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.25  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.24  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.22  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.21  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.20  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.19  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.18  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.17  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.16  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.15  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import implementation
from xml.dom.Node import Node
from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.html.HTMLTableSectionElement import HTMLTableSectionElement

rwattrs = ('cells', 'align', 'bgColor', 'ch', 'chOff', 'vAlign')
rattrs = ('rowIndex', 'sectionRowIndex')

class HTMLTableRowElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='TR'):
        HTMLElement.__init__(self, ownerDocument, "TR", nodeName)

    def _get_rowIndex(self):
        #Get our index in the table
        section = self.parentNode
        if section == None:
            return -1
        table = section.parentNode
        if table == None:
            return -1
        rows = table._get_rows()
        return rows.index(self)

    def _get_sectionRowIndex(self):
        section = self.parentNode
        if section == None:
            return -1
        rows = section._get_rows()
        return rows.index(self)

    def _get_cells(self):
        r = []
        #children = self.getChildNodes()
        #for ctr in range(children.getLength()):
        #   child = children.item(ctr)
        for child in self.childNodes:
            if child.tagName in ['TD','TH']:
                r.append(child)
        return implementation._4dom_createHTMLCollection(r)

    def _set_cells(self, new_cells):
        old_cells = self._get_cells()
        new_cells = new_cells
        for curr_cell in old_cells:
            self.removeChild(curr_cell)
            for curr_cell in new_cells:
                self.appendChild(curr_cell)

    def insertCell(self,index):
        if index < 0:
            return None
        td = None
        cells = self._get_cells()
        length = cells.length
        if cells.length == index:
            td = self.ownerDocument.createElement('TD');
            self.appendChild(td);
        elif cells.length > index:
            td = self.ownerDocument.createElement('TD')
            self.insertBefore(td, cells[index])
        else:
            #ADC: Pad the cells until we get to the desired index
            for i in range(cells.length, index+1):
                td = self.ownerDocument.createElement('TD')
                self.appendChild(td)
        return td

    def deleteCell(self,index):
        if index < 0:
            return
        cells = self._get_cells()
        if len(cells) > index:
            self.removeChild(cells[index])

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

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

    def _get_vAlign(self):
        return self.getAttribute('VALIGN')

    def _set_vAlign(self,valign):
        self.setAttribute('VALIGN',valign)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'rowIndex'      : _get_rowIndex, 
         'sectionRowIndex' : _get_sectionRowIndex, 
         'cells'         : _get_cells, 
         'align'         : _get_align, 
         'bgColor'       : _get_bgColor, 
         'ch'            : _get_ch, 
         'chOff'         : _get_chOff, 
         'vAlign'        : _get_vAlign, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'cells'         : _set_cells, 
         'align'         : _set_align, 
         'bgColor'       : _set_bgColor, 
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

#--- (end HTMLTableRowElement.py) ---
