########################################################################
#
# File Name:            HTMLTableElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTableElement.py.html
#
# History:
# $Log: HTMLTableElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
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

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom import ext
import string

rwattrs = ('caption', 'tHead', 'tFoot', 'align', 'bgColor', 'border', 'cellPadding', 'cellSpacing', 'frame', 'rules', 'summary', 'width')
rattrs = ('rows', 'tBodies')

class HTMLTableElement(HTMLElement):

    """
    Operations follow the DOM spec, and the 4.0 DTD for TABLE
    <!ELEMENT TABLE (CAPTION?,(COL? | COLGROUP?),THEAD?,TFOOT?,TBODY+)>
    """
    def __init__(self, ownerDocument, nodeName='TABLE'):
        HTMLElement.__init__(self, ownerDocument, "TABLE", nodeName)
    
    def _get_caption(self):
        hc = self.getElementsByTagName('CAPTION')
        if hc.length == 0:
            return None;
        return hc.item(0)

    def _set_caption(self,capt):
        hc = self.getElementsByTagName('CAPTION')
        if hc.length == 0:
            #The caption is first
            first = self.firstChild
            if first == None:
                self.appendChild(capt)
            else:
                self.insertBefore(capt, first)
        else:
            self.replaceChild(capt, hc[0])

    def _get_tHead(self):
        hc = self.getElementsByTagName('THEAD')
        if hc.length == 0:
            return None
        return hc[0]

    def _set_tHead(self,thead):
        old = self._get_tHead()
        if old:
            self.replaceChild(thread,old)
        else:
            #We need to put the new Thead in the correct spot
            #Look for a body
            hc = self.getElementsByTagName('BODY')
            if hc.length != 0:
                #Insert before the first body
                self.insertBefore(thead, hc[0])
                return
            #No body
            nodes = self.childNodes
            for node in nodes:
                if node.tagName not in ['CAPTION','COL','COLGROUP']:
                    #This is where we go
                    if node.nextSibling != None:
                        self.insertBefore(thread, node.nextSibling)
                        return
            #This where it goes
            self.appendChild(thead)


    def _get_tFoot(self):
        hc = self.getElementsByTagName('TFOOT')
        if hc.length == 0:
            return None
        return hc[0]

    def _set_tFoot(self,tfoot):
        old = self._get_tFoot()
        if old == None:
            #TFoot always goes last
            self.appendChild(tfoot)
        else:
            self.replaceChild(tfoot, old)

    def _get_rows(self):
        rows = []
        tHead = self._get_tHead()
        if tHead != None:
            row  = tHead._get_rows()
            for child in row:
                rows.append(child)
        tBodies = self._get_tBodies()
        for tb in tBodies:
            row = tb._get_rows()
            for r in row:
                rows.append(r) 
        tFoot = self._get_tFoot()
        if tFoot != None:
            row  = tFoot._get_rows()
            for child in row:
                rows.append(child)
        return implementation._4dom_createHTMLCollection(rows)

    def _get_tBodies(self):
        bodies = []
        children = self.childNodes
        for child in children:
            if child.tagName == 'TBODY':
                bodies.append(child)
        return implementation._4dom_createHTMLCollection(bodies)

    def createTHead(self):
        #Create a new THead if one does not exist
        thead = self._get_tHead()
        if not thead:
            thead = self.ownerDocument.createElement('THEAD')
            #Override the node name
            self._set_tHead(thead)
        return thead

    def deleteTHead(self):
        thead = self._get_tHead()
        if thead != None:
            self.removeChild(thead)

    def createTFoot(self):
        #Create s new TFoot if one does not exist
        tfoot = self._get_tFoot()
        if not tfoot:
            tfoot = self.ownerDocument.createElement('TFOOT')
            self._set_tFoot(tfoot)
        return tfoot

    def deleteTFoot(self):
        tfoot = self._get_tFoot()
        if tfoot:
            self.removeChild(tfoot)

    def createCaption(self):
        caption = self._get_caption()
        if not caption:
            caption = self.ownerDocument.createElement('CAPTION')
            self._set_caption(caption)
        return caption

    def deleteCaption(self):
        caption = self._get_caption()
        if caption:
            self.removeChild(caption)

    def insertRow(self,index):
        if index < 0:
            return
        tr = self.ownerDocument.createElement('TR')
        rows = self._get_rows()
        if rows.length == 0:
            #ADC: create a new body for them in which to insert the row
            body = self.ownerDocument.createElement('TBODY')
            tfoot = self._get_tFoot()
            if tfoot == None:
                self.appendChild(body)
            else:
                self.insertBefore(body, tfoot)
        if index == rows.length:
            if rows.length == 0:
                parent_node = self._get_tBodies()[0]
            else:
                lastTR = rows[-1]
                parent_node = lastTR.parentNode
            parent_node.appendChild(tr)         
        elif index > rows.length:
            #put it in the parent of the last row
            if rows.length == 0:
                parent_node = self._get_tBodies()[0]
            else:
                lastTR = rows[-1]
                parent_node = lastTR.parentNode
            #ADC: Pad the rows until we get to the desired index
            for i in range(rows.length, index+1):
                tr = self.ownerDocument.createElement('TR')
                parent_node.appendChild(tr)
        else:
            #zero based indexing
            currentRow = rows[index]
            #Put it before the current row
            currentRow.parentNode.insertBefore(tr, currentRow)
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

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self,bgcolor):
        self.setAttribute('BGCOLOR',bgcolor)

    def _get_border(self):
        return self.getAttribute('BORDER')

    def _set_border(self,border):
        self.setAttribute('BORDER',border)

    def _get_cellPadding(self):
        return self.getAttribute('CELLPADDING')

    def _set_cellPadding(self,cellpadding):
        self.setAttribute('CELLPADDING',cellpadding)

    def _get_cellSpacing(self):
        return self.getAttribute('CELLSPACING')

    def _set_cellSpacing(self,cellspacing):
        self.setAttribute('CELLSPACING',cellspacing)

    def _get_frame(self):
        return self.getAttribute('FRAME')

    def _set_frame(self,frame):
        self.setAttribute('FRAME',frame)

    def _get_rules(self):
        return self.getAttribute('RULES')

    def _set_rules(self,rules):
        self.setAttribute('RULES',rules)

    def _get_summary(self):
        return self.getAttribute('SUMMARY')

    def _set_summary(self,summary):
        self.setAttribute('SUMMARY',summary)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self,width):
        self.setAttribute('WIDTH',width)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

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
    _readOnlyAttrs = [] 
    for attr in HTMLElement._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

#--- (end HTMLTableElement.py) ---
