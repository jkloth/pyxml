########################################################################
#
# File Name:            HTMLScriptElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLScriptElement.py.html
#
# History:
# $Log: HTMLScriptElement.py,v $
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
# Revision 1.15  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
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
# Revision 1.11  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.10  1999/08/29 04:08:00  uche
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
from xml.dom import implementation
from xml.dom.Node import Node
from xml.dom import ext

rwattrs = ('text', 'charset', 'defer', 'src', 'type')

class HTMLScriptElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='SCRIPT'):
        HTMLElement.__init__(self, ownerDocument, "SCRIPT", nodeName)

    def _get_text(self):
        self.normalize()
        #Get first text node
        for node in self.childNodes:
            if node.nodeType == Node.TEXT_NODE:
                return node.data
        return ''

    def _set_text(self,text):
        t = self.ownerDocument.createTextNode(text)
        for child in self.childNodes:
            self.removeChild(child)
        self.appendChild(t)

    def _get_charset(self):
        return self.getAttribute('CHARSET')

    def _set_charset(self,charset):
        self.setAttribute('CHARSET',charset)

    def _get_defer(self):
        if self.getAttributeNode('DEFER'):
            return 1
        return 0

    def _set_defer(self,defer):
        if defer:
            self.setAttribute('DEFER', '')
        else:
            self.removeAttribute('DEFER')

    def _get_src(self):
        return self.getAttribute('SRC')

    def _set_src(self,src):
        self.setAttribute('SRC',src)

    def _get_type(self):
        return self.getAttribute('TYPE')

    def _set_type(self,type):
        self.setAttribute('TYPE',type)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'text'          : _get_text, 
         'charset'       : _get_charset, 
         'defer'         : _get_defer, 
         'src'           : _get_src, 
         'type'          : _get_type, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'text'          : _set_text, 
         'charset'       : _set_charset, 
         'defer'         : _set_defer, 
         'src'           : _set_src, 
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

#--- (end HTMLScriptElement.py) ---
