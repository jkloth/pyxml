########################################################################
#
# File Name:            HTMLAnchorElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLAnchorElement.py.html
#
# History:
# $Log: HTMLAnchorElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.19  2000/05/24 17:54:18  molson
# Fixed tab errors
#
# Revision 1.18  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.17  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.16  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.14  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.13  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.12  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.11  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.10  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
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

rwattrs = (
    'accessKey',
    'charset',
    'coords',
    'href',
    'hreflang',
    'name',
    'rel',
    'rev',
    'tabIndex',
    'shape',
    'target',
    'type'
    )

class HTMLAnchorElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='A'):
        HTMLElement.__init__(self, ownerDocument, 'A', nodeName)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accesskey):
        self.setAttribute('ACCESSKEY',accesskey)

    def _get_charset(self):
        return self.getAttribute('CHARSET')

    def _set_charset(self,charset):
        self.setAttribute('CHARSET',charset)

    def _get_coords(self):
        return self.getAttribute('COORDS')

    def _set_coords(self,coords):
        self.setAttribute('COORDS',coords)

    def _get_href(self):
        return self.getAttribute('HREF')

    def _set_href(self,href):
        self.setAttribute('HREF',href)

    def _get_hreflang(self):
        return self.getAttribute('HREFLANG')

    def _set_hreflang(self,hreflang):
        self.setAttribute('HREFLANG',hreflang)

    def _get_rel(self):
        return self.getAttribute('REL')

    def _set_rel(self,rel):
        self.setAttribute('REL',rel)

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_rev(self):
        return self.getAttribute('REV')

    def _set_rev(self,rev):
        self.setAttribute('REV',rev)

    def _get_shape(self):
        return self.getAttribute('SHAPE')

    def _set_shape(self,shape):
        self.setAttribute('SHAPE',shape)

    def _get_tabIndex(self):
        return int(self.getAttribute('TABINDEX'))

    def _set_tabIndex(self,tabindex):
        self.setAttribute('TABINDEX',str(tabindex))

    def _get_target(self):
        return self.getAttribute('TARGET')

    def _set_target(self,target):
        self.setAttribute('TARGET',target)

    def _get_type(self):
        return self.getAttribute('TYPE')

    def _set_type(self,type):
        self.setAttribute('TYPE',type)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'accessKey'     : _get_accessKey, 
         'charset'       : _get_charset, 
         'coords'        : _get_coords, 
         'href'          : _get_href, 
         'hreflang'      : _get_hreflang, 
         'name'          : _get_name, 
         'rel'           : _get_rel, 
         'rev'           : _get_rev, 
         'tabIndex'      : _get_tabIndex, 
         'shape'         : _get_shape, 
         'target'        : _get_target, 
         'type'          : _get_type, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'accessKey'     : _set_accessKey, 
         'charset'       : _set_charset, 
         'coords'        : _set_coords, 
         'href'          : _set_href, 
         'hreflang'      : _set_hreflang, 
         'name'          : _set_name, 
         'rel'           : _set_rel, 
         'rev'           : _set_rev, 
         'tabIndex'      : _set_tabIndex, 
         'shape'         : _set_shape, 
         'target'        : _set_target, 
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

#--- (end HTMLAnchorElement.py) ---
