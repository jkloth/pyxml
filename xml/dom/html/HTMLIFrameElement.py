########################################################################
#
# File Name:            HTMLIFrameElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLIFrameElement.py.html
#
# History:
# $Log: HTMLIFrameElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.18  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.17  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.16  2000/05/06 09:12:18  jkloth
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


from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.Node import Node

rwattrs = ('align', 'frameBorder', 'height', 'longDesc', 'marginHeight', 'marginWidth', 'scrolling', 'src', 'width')

class HTMLIFrameElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='IFRAME'):
        HTMLElement.__init__(self, ownerDocument, "IFRAME", nodeName)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_frameBorder(self):
        return self.getAttribute('FRAMEBORDER')

    def _set_frameBorder(self,frameborder):
        self.setAttribute('FRAMEBORDER',frameborder)

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_longDesc(self):
        return self.getAttribute('LONGDESC')

    def _set_longDesc(self,longdesc):
        self.setAttribute('LONGDESC',longdesc)

    def _get_marginHeight(self):
        return self.getAttribute('MARGINHEIGHT')

    def _set_marginHeight(self,marginheight):
        self.setAttribute('MARGINHEIGHT',marginheight)

    def _get_marginWidth(self):
        return self.getAttribute('MARGINWIDTH')

    def _set_marginWidth(self,marginwidth):
        self.setAttribute('MARGINWIDTH',marginwidth)

    def _get_scrolling(self):
        return self.getAttribute('SCROLLING')

    def _set_scrolling(self,scrolling):
        self.setAttribute('SCROLLING',scrolling)

    def _get_src(self):
        return self.getAttribute('SRC')

    def _set_src(self,src):
        self.setAttribute('SRC',src)

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
         'frameBorder'   : _get_frameBorder, 
         'height'        : _get_height, 
         'longDesc'      : _get_longDesc, 
         'marginHeight'  : _get_marginHeight, 
         'marginWidth'   : _get_marginWidth, 
         'scrolling'     : _get_scrolling, 
         'src'           : _get_src, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'align'         : _set_align, 
         'frameBorder'   : _set_frameBorder, 
         'height'        : _set_height, 
         'longDesc'      : _set_longDesc, 
         'marginHeight'  : _set_marginHeight, 
         'marginWidth'   : _set_marginWidth, 
         'scrolling'     : _set_scrolling, 
         'src'           : _set_src, 
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

#--- (end HTMLIFrameElement.py) ---
