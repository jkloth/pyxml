########################################################################
#
# File Name:            HTMLObjectElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLObjectElement.py.html
#
# History:
# $Log: HTMLObjectElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.22  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.21  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.20  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.19  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.17  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.16  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.15  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
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
# Revision 1.11  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement
from xml.dom.Node import Node

rwattrs = ('code', 'align', 'archive', 'border', 'codeBase', 'codeType', 'data', 'declare', 'height', 'hspace', 'standby', 'tabIndex', 'type', 'useMap', 'vspace', 'width')
rattrs = ('form',)

class HTMLObjectElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='OBJECT'):
        HTMLFormBasedElement.__init__(self, ownerDocument, "OBJECT", nodeName)

    def _get_form(self):
        return HTMLFormBasedElement.getForm(self)

    def _get_code(self):
        return self.getAttribute('CODE')

    def _set_code(self,code):
        self.setAttribute('CODE',code)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_archive(self):
        return self.getAttribute('ARCHIVE')

    def _set_archive(self,archive):
        self.setAttribute('ARCHIVE',archive)

    def _get_border(self):
        return self.getAttribute('BORDER')

    def _set_border(self,border):
        self.setAttribute('BORDER',border)

    def _get_codeBase(self):
        return self.getAttribute('CODEBASE')

    def _set_codeBase(self,codebase):
        self.setAttribute('CODEBASE',codebase)

    def _get_codeType(self):
        return self.getAttribute('CODETYPE')

    def _set_codeType(self,codetype):
        self.setAttribute('CODETYPE',codetype)

    def _get_data(self):
        return self.getAttribute('DATA')

    def _set_data(self,data):
        self.setAttribute('DATA',data)

    def _get_declare(self):
        return (self.getAttributeNode('DECLARE') and 1) or 0

    def _set_declare(self,declare):
        if declare:
            self.setAttribute('DECLARE', '')
        else:
            self.removeAttribute('DECLARE')

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_hspace(self):
        return self.getAttribute('HSPACE')

    def _set_hspace(self,hspace):
        self.setAttribute('HSPACE',hspace)

    def _get_standby(self):
        return self.getAttribute('STANDBY')

    def _set_standby(self,standby):
        self.setAttribute('STANDBY',standby)

    def _get_tabIndex(self):
        return int(self.getAttribute('TABINDEX'))

    def _set_tabIndex(self,tabindex):
        self.setAttribute('TABINDEX',str(tabindex))

    def _get_type(self):
        return self.getAttribute('TYPE')

    def _set_type(self,type):
        self.setAttribute('TYPE',type)

    def _get_useMap(self):
        return self.getAttribute('USEMAP')

    def _set_useMap(self,usemap):
        self.setAttribute('USEMAP',usemap)

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

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'form'          : _get_form, 
         'code'          : _get_code, 
         'align'         : _get_align, 
         'archive'       : _get_archive, 
         'border'        : _get_border, 
         'codeBase'      : _get_codeBase, 
         'codeType'      : _get_codeType, 
         'data'          : _get_data, 
         'declare'       : _get_declare, 
         'height'        : _get_height, 
         'hspace'        : _get_hspace, 
         'standby'       : _get_standby, 
         'tabIndex'      : _get_tabIndex, 
         'type'          : _get_type, 
         'useMap'        : _get_useMap, 
         'vspace'        : _get_vspace, 
         'width'         : _get_width, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'code'          : _set_code, 
         'align'         : _set_align, 
         'archive'       : _set_archive, 
         'border'        : _set_border, 
         'codeBase'      : _set_codeBase, 
         'codeType'      : _set_codeType, 
         'data'          : _set_data, 
         'declare'       : _set_declare, 
         'height'        : _set_height, 
         'hspace'        : _set_hspace, 
         'standby'       : _set_standby, 
         'tabIndex'      : _set_tabIndex, 
         'type'          : _set_type, 
         'useMap'        : _set_useMap, 
         'vspace'        : _set_vspace, 
         'width'         : _set_width, 
      }) 

    # Create the read-only list of attributes 
    _readOnlyAttrs = [] 
    for attr in HTMLFormBasedElement._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

#--- (end HTMLObjectElement.py) ---
