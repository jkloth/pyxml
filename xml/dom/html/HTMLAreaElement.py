########################################################################
#
# File Name:            HTMLAreaElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLAreaElement.py.html
#
# History:
# $Log: HTMLAreaElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.20  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.19  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.18  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.17  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.15  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.14  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.13  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.12  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.11  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.10  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.9  1999/08/29 04:08:00  uche
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


rwattrs = ('accessKey', 'alt', 'coords', 'href', 'noHref', 'shape', 'tabIndex', 'target')

import string
class HTMLAreaElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='AREA'):
        HTMLElement.__init__(self, ownerDocument, 'AREA', nodeName)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accessKey):
        self.setAttribute('ACCESSKEY',accessKey)

    def _get_alt(self):
        return self.getAttribute('ALT')

    def _set_alt(self,alt):
        self.setAttribute('ALT',alt)

    def _get_coords(self):
        return self.getAttribute('COORDS')

    def _set_coords(self,coords):
        self.setAttribute('COORDS',coords)

    def _get_href(self):
        return self.getAttribute('HREF')

    def _set_href(self,href):
        self.setAttribute('HREF',href)

    def _get_noHref(self):
        return self.getAttributeNode('NOHREF') and 1 or 0

    def _set_noHref(self,noHref):
        if noHref:
            self.setAttribute('NOHREF', '')
        else:
            self.removeAttribute('NOHREF')

    def _get_shape(self):
        return self.getAttribute('SHAPE')

    def _set_shape(self,shape):
        self.setAttribute('SHAPE',shape)

    def _get_tabIndex(self):
        rt = self.getAttribute('TABINDEX')
        if rt != '':
            return string.atoi(rt)
        return -1

    def _set_tabIndex(self,tabIndex):
        self.setAttribute('TABINDEX',str(tabIndex))

    def _get_target(self):
        return self.getAttribute('TARGET')

    def _set_target(self,target):
        self.setAttribute('TARGET',target)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'accessKey'     : _get_accessKey, 
         'alt'           : _get_alt, 
         'coords'        : _get_coords, 
         'href'          : _get_href, 
         'noHref'        : _get_noHref, 
         'shape'         : _get_shape, 
         'tabIndex'      : _get_tabIndex, 
         'target'        : _get_target, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'accessKey'     : _set_accessKey, 
         'alt'           : _set_alt, 
         'coords'        : _set_coords, 
         'href'          : _set_href, 
         'noHref'        : _set_noHref, 
         'shape'         : _set_shape, 
         'tabIndex'      : _set_tabIndex, 
         'target'        : _set_target, 
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

#--- (end HTMLAreaElement.py) ---
