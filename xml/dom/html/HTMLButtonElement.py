########################################################################
#
# File Name:            HTMLButtonElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLButtonElement.py.html
#
# History:
# $Log: HTMLButtonElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
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
# Revision 1.15  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.13  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.12  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.11  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
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


from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement
from xml.dom.Node import Node
import string

rwattrs = ('accessKey', 'disabled', 'name', 'tabIndex', 'value')
rattrs = ('type', 'form')

class HTMLButtonElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='BUTTON'):
        HTMLFormBasedElement.__init__(self, ownerDocument, 'BUTTON', nodeName)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accessKey):
        self.setAttribute('ACCESSKEY',accessKey)

    def _get_disabled(self):
        if self.getAttributeNode('DISABLED'):
            return 1
        return 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED','')
        else:
            self.removeAttribute('DISABLED')

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_tabIndex(self):
        rt = self.getAttribute('TABINDEX')
        if rt != None:
            return string.atoi(rt)
        return -1

    def _set_tabIndex(self,tabIndex):
        self.setAttribute('TABINDEX',str(tabIndex))

    def _get_type(self):
        return self.getAttribute('TYPE')
    
    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    def _get_form(self):
        return HTMLFormBasedElement.getForm(self)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'type'          : _get_type, 
         'form'          : _get_form, 
         'accessKey'     : _get_accessKey, 
         'disabled'      : _get_disabled, 
         'name'          : _get_name, 
         'tabIndex'      : _get_tabIndex, 
         'value'         : _get_value, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'accessKey'     : _set_accessKey, 
         'disabled'      : _set_disabled, 
         'name'          : _set_name, 
         'tabIndex'      : _set_tabIndex, 
         'value'         : _set_value, 
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

#--- (end HTMLButtonElement.py) ---
