########################################################################
#
# File Name:            HTMLOptionElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLOptionElement.py.html
#
# History:
# $Log: HTMLOptionElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.28  2000/05/24 18:48:11  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.27  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.26  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.25  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.23  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.22  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.21  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.20  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
#
# Revision 1.19  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.18  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.17  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.16  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.15  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
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

rwattrs = ('defaultSelected', 'disabled', 'label', 'selected', 'value')
rattrs = ('text', 'index',)

class HTMLOptionElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='OPTION'):
        HTMLFormBasedElement.__init__(self, ownerDocument, "OPTION", nodeName)

    def _get_defaultSelected(self):
        return self.getAttributeNode('DEFAULTSELECTED') and 1 or 0

    def _set_defaultSelected(self, selected):
        if selected:
            self.setAttribute('DEFAULTSELECTED', '')
        else:
            self.removeAttribute('DEFAULTSELECTED')

    def _get_text(self):
        #Actually return our text from our first child
        #Just in case
        self.normalize()
        if self.childNodes.length == 0:
            return ''
        return self.childNodes[0].data

    def _get_index(self):
        p = self.parentNode
        if p.tagName != 'SELECT':
            return -1
        options = p._get_options()
        for ctr in range(options.length):
            if options.item(ctr) == self:
                return ctr
        return -1

    def _get_disabled(self):
        return self.getAttributeNode('DISABLED') and 1 or 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', '')
        else:
            self.removeAttribute('DISABLED')

    def _get_label(self):
        return self.getAttribute('LABEL')

    def _set_label(self,label):
        self.setAttribute('LABEL',label)

    def _get_selected(self):
        if self.getAttributeNode('SELECTED'):
            return 1
        return 0    

    def _set_selected(self,selc):
        if selc:
            self.setAttribute('SELECTED', '')
        else:
            self.removeAttribute('SELECTED')

    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    def _get_form(self):
        return HTMLFormBasedElement._get_form(self)

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement("OPTION")
            else:
                node = newOwner.createElement("OPTION")
        node = HTMLFormBasedElement.cloneNode(self,deep,node)
        return node


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'text'          : _get_text, 
         'index'         : _get_index, 
         'defaultSelected' : _get_defaultSelected, 
         'disabled'      : _get_disabled, 
         'label'         : _get_label, 
         'selected'      : _get_selected, 
         'value'         : _get_value, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'defaultSelected' : _set_defaultSelected, 
         'disabled'      : _set_disabled, 
         'label'         : _set_label, 
         'selected'      : _set_selected, 
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

#--- (end HTMLOptionElement.py) ---
