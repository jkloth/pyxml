########################################################################
#
# File Name:            HTMLSelectElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLSelectElement.py.html
#
# History:
# $Log: HTMLSelectElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.32  2000/05/24 18:14:49  molson
# Fixed tab errors
#
# Revision 1.31  2000/05/06 09:12:19  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.30  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.28  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.27  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.26  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.25  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.24  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
#
# Revision 1.23  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.22  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.21  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.20  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.19  1999/08/29 04:08:00  uche
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
from xml.dom import implementation
import string

rwattrs = ('selectedIndex', 'value', 'disabled', 'multiple', 
            'name', 'size', 'tabIndex')
rattrs = ('type', 'length', 'options', 'form')

class HTMLSelectElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='SELECT'):
        HTMLFormBasedElement.__init__(self, ownerDocument, "SELECT", nodeName)

    def _get_type(self):
        return self.getAttribute('TYPE')

    #def _4dom_set_type(self, type):
    #    self.setAttribute('TYPE', type)

    def _get_selectedIndex(self):
        hc = self._get_options()
        for ctr in range(hc.length):
            node = hc.item(ctr)
            if node._get_selected() == 1:
                return ctr
        return -1

    def _set_selectedIndex(self,index):
        hc = self._get_options()
        if index < 0 or index >= hc.length:
            # XXX Should we raise an exception?
            return
        #Set them all to not selected
        for ctr in range(hc.length):
            node = hc.item(ctr)
            if ctr == index:
                node._set_selected(1)
            else:
                node._set_selected(0)

    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    def _get_length(self):
        return self._get_options()._get_length()
        
    def _get_options(self):
        children = self.getElementsByTagName('OPTION')
        options = implementation._4dom_createHTMLCollection(children)
        return options

    def _get_disabled(self):
        if self.getAttributeNode('DISABLED'):
            return 1
        return 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', '')
        else:
            self.removeAttribute('DISABLED')

    def _get_multiple(self):
        if self.getAttributeNode('MULTIPLE'):
            return 1
        return 0

    def _set_multiple(self,mult):
        if mult:
            self.setAttribute('MULTIPLE', '')
        else:
            self.removeAttribute('MULTIPLE')

    def _get_name(self):
        return self.getAttribute('NAME')
    
    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_size(self):
        rt = self.getAttribute('SIZE')
        if rt != None:
            return string.atoi(rt)
        return -1

    def _set_size(self,size):
        self.setAttribute('SIZE',str(size))

    def _get_tabIndex(self):
        return string.atoi(self.getAttribute('TABINDEX'))

    def _set_tabIndex(self,tabindex):
        self.setAttribute('TABINDEX',str(tabindex))

    def add(self,newElement,beforeElement):
        self.insertBefore(newElement,beforeElement)

    def remove(self,index):
        if index < 0 or index >= self._get_length:
            return
        hc = self._get_options()
        node = hc.item(index)
        self.removeChild(node)

    def _get_form(self):
        return HTMLFormBasedElement._get_form(self)

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement('SELECT')
            else:
                node = newOwner.createElement('SELECT')
        node.setAttribute('TYPE', self._get_type())
        return HTMLFormBasedElement.cloneNode(self,deep,node)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'type'          : _get_type, 
         'length'        : _get_length, 
         'options'       : _get_options, 
         'form'          : _get_form, 
         'selectedIndex' : _get_selectedIndex, 
         'value'         : _get_value, 
         'disabled'      : _get_disabled, 
         'multiple'      : _get_multiple, 
         'name'          : _get_name, 
         'size'          : _get_size, 
         'tabIndex'      : _get_tabIndex, 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'selectedIndex' : _set_selectedIndex, 
         'value'         : _set_value, 
         'disabled'      : _set_disabled, 
         'multiple'      : _set_multiple, 
         'name'          : _set_name, 
         'size'          : _set_size, 
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

#--- (end HTMLSelectElement.py) ---
