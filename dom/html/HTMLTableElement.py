########################################################################
#
# File Name:            HTMLTableElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableElement.py.html
#
# History:
# $Log: HTMLTableElement.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:53  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.31  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
#
# Revision 1.30  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.29  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.28  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.27  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.26  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.24  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.23  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.22  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.21  2000/02/10 06:22:27  molson
# Fixed bugs
#
# Revision 1.20  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.19  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
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

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR
from xml.dom import implementation
import string

class HTMLTableElement(HTMLElement):
    """
    Operations follow the DOM spec, and the 4.0 DTD for TABLE
    <!ELEMENT TABLE (CAPTION?, (COL*|COLGROUP*), THEAD?, TFOOT?, TBODY+)>
    """
    def __init__(self, ownerDocument, nodeName='TABLE'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self,bgcolor):
        self.setAttribute('BGCOLOR',bgcolor)

    def _get_border(self):
        return self.getAttribute('BORDER')

    def _set_border(self,border):
        self.setAttribute('BORDER',border)

    def _get_caption(self):
        nl = self.getElementsByTagName('CAPTION')
        if len(nl):
            return nl[0]
        return None

    def _set_caption(self,capt):
        nl = self.getElementsByTagName('CAPTION')
        if len(nl):
            self.replaceChild(capt, nl[0])
        else:
            #The caption should be first
            first = self.firstChild
            if not first:
                self.insertBefore(capt, first)
            else:
                self.appendChild(capt)

    def _get_cellPadding(self):
        return self.getAttribute('CELLPADDING')

    def _set_cellPadding(self,cellpadding):
        self.setAttribute('CELLPADDING',cellpadding)

    def _get_cellSpacing(self):
        return self.getAttribute('CELLSPACING')

    def _set_cellSpacing(self,cellspacing):
        self.setAttribute('CELLSPACING',cellspacing)

    def _get_frame(self):
        return string.capitalize(self.getAttribute('FRAME'))

    def _set_frame(self,frame):
        self.setAttribute('FRAME',frame)

    def _get_rows(self):
        rows = []
        tHead = self._get_tHead()
        if tHead:
            hc = tHead._get_rows()
            rows = rows + hc
        tBodies = self._get_tBodies()
        for tb in tBodies:
            hc = tb._get_rows()
            rows = rows + hc
        tFoot = self._get_tFoot()
        if tFoot:
            hc  = tFoot._get_rows()
            for row in hc:
                rows.append(row)
        return implementation._4dom_createHTMLCollection(rows)

    def _get_rules(self):
        return string.capitalize(self.getAttribute('RULES'))

    def _set_rules(self,rules):
        self.setAttribute('RULES',rules)

    def _get_summary(self):
        return self.getAttribute('SUMMARY')

    def _set_summary(self,summary):
        self.setAttribute('SUMMARY',summary)

    def _get_tBodies(self):
        bodies = []
        children = self.childNodes
        for child in children:
            if child.tagName == 'TBODY':
                bodies.append(child)
        return implementation._4dom_createHTMLCollection(bodies)

    def _get_tFoot(self):
        children = self.childNodes
        for child in children:
            if child.tagName == 'TFOOT':
                return child
        return None

    def _set_tFoot(self, newFooter):
        oldFooter = self._get_tFoot()
        if not footer:
            # TFoot goes after THead
            ref = None
            child = self.firstChild
            while not ref and child:
                if child.tagName == 'THEAD':
                    ref = child.nextSibling
                elif child.tagName == 'TBODY':
                    ref = child
                child = child.nextSibling
            self.insertBefore(newFooter, ref)
        else:
            self.replaceChild(newFooter, oldFooter)

    def _get_tHead(self):
        children = self.childNodes
        for child in children:
            if child.tagName == 'THEAD':
                return child
        return None

    def _set_tHead(self, newHead):
        oldHead = self._get_tHead()
        if oldHead:
            self.replaceChild(newHead, oldHead)
        else:
            # We need to put the new Thead in the correct spot
            # Look for a TFOOT or a TBODY
            ref = None
            child = self.firstChild
            while not ref and child:
                if child.tagName = 'TFOOT':
                    ref = child
                elif child.tagName = 'TBODY':
                    ref = child
                elif child.tagName in ['COL','COLGROUP']:
                    name = child.tagName
                    child = child.nextSibling
                    while child.tagName == name:
                        child = child.nextSibling
                    ref = child
                elif child.tagName == 'CAPTION':
                    ref = child.nextSibling
            self.insertBefore(newHead, ref)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self,width):
        self.setAttribute('WIDTH',width)

    ### Methods ###

    def createCaption(self):
        #Create a new CAPTION if one does not exist
        caption = self._get_caption()
        if not caption:
            caption = self.ownerDocument.createElement('CAPTION')
            self._set_caption(caption)
        return caption

    def createTHead(self):
        #Create a new THEAD if one does not exist
        thead = self._get_tHead()
        if not thead:
            thead = self.ownerDocument.createElement('THEAD')
            self._set_tHead(thead)
        return thead

    def createTFoot(self):
        #Create a new TFOOT if one does not exist
        tfoot = self._get_tFoot()
        if not tfoot:
            tfoot = self.ownerDocument.createElement('TFOOT')
            self._set_tFoot(tfoot)
        return tfoot

    def deleteCaption(self):
        caption = self._get_caption()
        if caption:
            self.removeChild(caption)

    def deleteRow(self,index):
        rows = self._get_rows()
        if index < 0 or index >= len(rows):
            pass
            raise DOMException(INDEX_SIZE_ERR)
        rows[index].parentNode.removeChild(rows[index])

    def deleteTHead(self):
        thead = self._get_tHead()
        if thead != None:
            self.removeChild(thead)

    def deleteTFoot(self):
        tfoot = self._get_tFoot()
        if tfoot:
            self.removeChild(tfoot)

    def insertRow(self,index):
        rows = self._get_rows()
        if index < 0 or index > len(rows):
            pass
            raise DOMException(INDEX_SIZE_ERR)
        newRow = self.ownerDocument.createElement('TR')
        if not rows:
            # An empty table, create a body in which to insert the row
            body = self.ownerDocument.createElement('TBODY')
            # The body is the last element according to DTD
            self.appendChild(body)
            parent = body
            ref = None
        elif index == len(rows):
            parent = rows[-1].parentNode
            ref = None
        else:
            ref = rows[index]
            parent = ref.parentNode
        return parent.insertBefore(newRow, ref)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({ 
         'rows'          : _get_rows, 
         'tBodies'       : _get_tBodies, 
         'caption'       : _get_caption, 
         'tHead'         : _get_tHead, 
         'tFoot'         : _get_tFoot, 
         'align'         : _get_align, 
         'bgColor'       : _get_bgColor, 
         'border'        : _get_border, 
         'cellPadding'   : _get_cellPadding, 
         'cellSpacing'   : _get_cellSpacing, 
         'frame'         : _get_frame, 
         'rules'         : _get_rules, 
         'summary'       : _get_summary, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'caption'       : _set_caption, 
         'tHead'         : _set_tHead, 
         'tFoot'         : _set_tFoot, 
         'align'         : _set_align, 
         'bgColor'       : _set_bgColor, 
         'border'        : _set_border, 
         'cellPadding'   : _set_cellPadding, 
         'cellSpacing'   : _set_cellSpacing, 
         'frame'         : _set_frame, 
         'rules'         : _set_rules, 
         'summary'       : _set_summary, 
         'width'         : _set_width, 
      }) 

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
