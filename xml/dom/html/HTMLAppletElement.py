########################################################################
#
# File Name:            HTMLAppletElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLAppletElement.py.html
#
# History:
# $Log: HTMLAppletElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
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
# Revision 1.11  2000/05/03 23:38:15  pweinstein
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


rwattrs = ('align',
           'alt',
           'archive',
           'code',
           'codeBase',
           'height',
           'hspace',
           'object',
           'vspace',
           'width'
           )

class HTMLAppletElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='APPLET'):
        HTMLElement.__init__(self, ownerDocument, 'APPLET', nodeName)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_alt(self):
        return self.getAttribute('ALT')

    def _set_alt(self,alt):
        self.setAttribute('ALT',alt)

    def _get_archive(self):
        return self.getAttribute('ARCHIVE')

    def _set_archive(self,archive):
        self.setAttribute('ARCHIVE',archive)

    def _get_code(self):
        return self.getAttribute('CODE')

    def _set_code(self,code):
        self.setAttribute('CODE',code)

    def _get_codeBase(self):
        return self.getAttribute('CODEBASE')

    def _set_codeBase(self,codeBase):
        self.setAttribute('CODEBASE',codeBase)

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_hspace(self):
        return self.getAttribute('HSPACE')

    def _set_hspace(self,hspace):
        self.setAttribute('HSPACE',hspace)

    def _get_object(self):
        return self.getAttribute('OBJECT')

    def _set_object(self,object):
        self.setAttribute('OBJECT',object)

    def _get_vspace(self):
        return self.getAttribute('VSPACE')

    def _set_vspace(self,vspace):
        self.setAttribute('VSPACE',vspace)

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
         'alt'           : _get_alt, 
         'archive'       : _get_archive, 
         'code'          : _get_code, 
         'codeBase'      : _get_codeBase, 
         'height'        : _get_height, 
         'hspace'        : _get_hspace, 
         'object'        : _get_object, 
         'vspace'        : _get_vspace, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'align'         : _set_align, 
         'alt'           : _set_alt, 
         'archive'       : _set_archive, 
         'code'          : _set_code, 
         'codeBase'      : _set_codeBase, 
         'height'        : _set_height, 
         'hspace'        : _set_hspace, 
         'object'        : _set_object, 
         'vspace'        : _set_vspace, 
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

#--- (end HTMLAppletElement.py) ---
