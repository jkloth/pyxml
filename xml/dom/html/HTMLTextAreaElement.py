########################################################################
#
# File Name:            HTMLTextAreaElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLTextAreaElement.py.html
#
# History:
# $Log: HTMLTextAreaElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.22  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
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
# Revision 1.17  2000/03/15 21:34:25  uche
# Last-minute packaging fixes
# Major fixes to SortDocOrder: ahndle document() function and attr wrappers
# Other fixes
#
# Revision 1.16  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.15  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.14  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.13  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.12  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
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
import string

rwattrs = ('defaultValue', 'accessKey', 'cols', 'disabled', 'name', 'readOnly', 'rows', 'tabIndex')
rattrs = ('type', 'form')

class HTMLTextAreaElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='TEXTAREA'):
        HTMLFormBasedElement.__init__(self, ownerDocument, "TEXTAREA", nodeName)

    def _get_defaultValue(self):
        return self.getAttribute('DEFAULTVALUE')

    def _set_defaultValue(self, defaultValue):
        return self.setAttribute('DEFAULTVALUE', defaultValue)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accessKey):
        self.setAttribute('ACCESSKEY',accessKey)

    def _get_cols(self):
        rt = self.getAttribute('COLS')
        if rt != '':
            return string.atoi(rt)
        return -1

    def _set_cols(self,cols):
        self.setAttribute('COLS',str(cols))

    def _get_disabled(self):
        if self.getAttributeNode('DISABLED'):
            return 1
        return 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', '')
        else:
            self.removeAttribute('DISABLED')

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_readOnly(self):
        if self.getAttributeNode('READONLY'):
            return 1
        else:
            return 0

    def _set_readOnly(self,readOnly):
        if readOnly:
            self.setAttribute('READONLY', '')
        else:
            self.removeAttribute('READONLY')

    def _get_rows(self):
        rt = self.getAttribute('ROWS')
        if rt != '':
            return string.atoi(rt)
        return -1

    def _set_rows(self,rows):
        self.setAttribute('ROWS',str(rows))

    def _get_tabIndex(self):
        rt = self.getAttribute('TABINDEX')
        if rt != '':
            return string.atoi(rt)
        return -1

    def _set_tabIndex(self,tabIndex):
        self.setAttribute('TABINDEX',str(tabIndex))

    def _get_type(self):
        return self.getAttribute('TYPE')

    def blur(self):
        pass

    def focus(self):
        pass

    def select(self):
        pass

    def _get_form(self):
        return HTMLFormBasedElement.getForm(self)

    def cloneNode(self,deep,node=None,newOwner = None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement("TEXTAREA")
            else:
                node = newOwner.createElement("TEXTAREA")
        node = HTMLFormBasedElement.cloneNode(self,deep,node)
        node._set_defaultValue(self._get_defaultValue())
        return node

#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'type'          : _get_type, 
         'form'          : _get_form, 
         'defaultValue'  : _get_defaultValue, 
         'accessKey'     : _get_accessKey, 
         'cols'          : _get_cols, 
         'disabled'      : _get_disabled, 
         'name'          : _get_name, 
         'readOnly'      : _get_readOnly, 
         'rows'          : _get_rows, 
         'tabIndex'      : _get_tabIndex, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'defaultValue'  : _set_defaultValue, 
         'accessKey'     : _set_accessKey, 
         'cols'          : _set_cols, 
         'disabled'      : _set_disabled, 
         'name'          : _set_name, 
         'readOnly'      : _set_readOnly, 
         'rows'          : _set_rows, 
         'tabIndex'      : _set_tabIndex, 
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

#--- (end HTMLTextAreaElement.py) ---
