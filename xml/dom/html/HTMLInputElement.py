########################################################################
#
# File Name:            HTMLInputElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLInputElement.py.html
#
# History:
# $Log: HTMLInputElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.27  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.26  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.25  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
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
# Revision 1.17  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.16  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.15  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.14  1999/08/29 04:08:00  uche
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

rwattrs = ('defaultValue', 'defaultChecked', 'accept', 'accessKey', 'align', 'alt', 'checked', 'disabled', 'maxLength', 'name', 'readOnly', 'size', 'src', 'tabIndex', 'useMap', 'value')
rattrs = ('type', 'form')

class HTMLInputElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='INPUT'):
        HTMLFormBasedElement.__init__(self, ownerDocument, "INPUT", nodeName)

    def _get_defaultValue(self):
        return self.getAttribute('DEFAULTVALUE')

    def _set_defaultValue(self, defaultValue):
        return self.setAttribute('DEFAULTVALUE', defaultValue)

    def _get_defaultChecked(self):
        return self._get_type() in ['RADIO','CHEKBOX'] and self.getAttributeNode('DEFAULTCHECKED') and 1 or 0

    def _set_defaultChecked(self, defaultChecked):
        if self._get_type() in ['RADIO','CHECKBOX'] and defaultChecked:
            self.setAttribute('DEFAULTCHECKED', '')
        else:
            self.removeAttribute('DEFAULTCHECKED')

    def _get_accept(self):
        return self.getAttribute('ACCEPT')

    def _set_accept(self,accept):
        self.setAttribute('ACCEPT',accept)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accessKey):
        self.setAttribute('ACCESSKEY',accessKey)

    def _get_align(self):
        return self.getAttribute('ALIGN')

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_alt(self):
        return self.getAttribute('ALT')

    def _set_alt(self,alt):
        self.setAttribute('ALT',alt)

    def _get_checked(self):
        return self._get_type() in ['RADIO','CHEKBOX'] and self.getAttributeNode('CHECKED') and 1 or 0

    def _set_checked(self,checked):
        if self._get_type() in ['RADIO','CHECKBOX']:
            if checked:
                self.setAttribute('CHECKED', '')
            else:
                self.removeAttribute('CHECKED')

    def _get_disabled(self):
        return self.getAttributeNode('DISABLED') and 1 or 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', '')
        else:
            self.removeAttribute('DISABLED')

    def _get_maxLength(self):
        if self._get_type() in ['TEXT','PASSWORD']:
            rt = self.getAttribute('MAXLENGTH')
        if rt != '':
            return string.atoi(rt)
        return -1;

    def _set_maxLength(self,maxLength):
        if self._get_type() in ['TEXT','PASSWORD']:
            self.setAttribute('MAXLENGTH',str(maxLength))

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_readOnly(self):
        if self._get_type() in ['TEXT','PASSWORD']:
            if self.getAttributeNode('READONLY'):
                return 1
        return 0

    def _set_readOnly(self,readOnly):
        if self._get_type() in ['TEXT','PASSWORD']:
            if readOnly:
                self.setAttribute('READONLY', '')
            else:
                self.removeAttribute('READONLY')

    def _get_size(self):
        return self.getAttribute('SIZE')

    def _set_size(self,size):
        self.setAttribute('SIZE',size)

    def _get_src(self):
        if self._get_type() == 'IMAGE':
            return self.getAttribute('SRC')
        return ''

    def _set_src(self,src):
        if self._get_type() == 'IMAGE':
            self.setAttribute('SRC',src)

    def _get_tabIndex(self):
        rt = self.getAttribute('TABINDEX')
        if rt != '':
            return string.atoi(rt)
        return -1

    def _set_tabIndex(self,tabIndex):
        self.setAttribute('TABINDEX',str(tabIndex))

    def _get_type(self):
        return string.upper(self.getAttribute('TYPE'))

    def _get_useMap(self):
        return self.getAttribute('USEMAP')

    def _set_useMap(self,useMap):
        self.setAttribute('USEMAP',useMap)

    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    def blur(self):
        pass

    def focus(self):
        pass

    def select(self):
        pass

    def click(self):
        pass

    def _get_form(self):
        return HTMLFormBasedElement.getForm(self)

    def cloneNode(self, deep, node=None, newOwner = None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement('INPUT');
            else:
                node = newOwner.createElement('INPUT')
        node = HTMLFormBasedElement.cloneNode(self,deep,node)
        node._set_defaultValue(self._get_defaultValue())
        node._set_defaultChecked(self._get_defaultChecked())
        return node


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'type'          : _get_type, 
         'form'          : _get_form, 
         'defaultValue'  : _get_defaultValue, 
         'defaultChecked' : _get_defaultChecked, 
         'accept'        : _get_accept, 
         'accessKey'     : _get_accessKey, 
         'align'         : _get_align, 
         'alt'           : _get_alt, 
         'checked'       : _get_checked, 
         'disabled'      : _get_disabled, 
         'maxLength'     : _get_maxLength, 
         'name'          : _get_name, 
         'readOnly'      : _get_readOnly, 
         'size'          : _get_size, 
         'src'           : _get_src, 
         'tabIndex'      : _get_tabIndex, 
         'useMap'        : _get_useMap, 
         'value'         : _get_value, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'defaultValue'  : _set_defaultValue, 
         'defaultChecked' : _set_defaultChecked, 
         'accept'        : _set_accept, 
         'accessKey'     : _set_accessKey, 
         'align'         : _set_align, 
         'alt'           : _set_alt, 
         'checked'       : _set_checked, 
         'disabled'      : _set_disabled, 
         'maxLength'     : _set_maxLength, 
         'name'          : _set_name, 
         'readOnly'      : _set_readOnly, 
         'size'          : _set_size, 
         'src'           : _set_src, 
         'tabIndex'      : _set_tabIndex, 
         'useMap'        : _set_useMap, 
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

#--- (end HTMLInputElement.py) ---
