########################################################################
#
# File Name:            HTMLElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLElement.py.html
#
# History:
# $Log: HTMLElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.24  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.23  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.22  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.21  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.20  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.18  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.17  2000/02/10 06:22:27  molson
# Fixed bugs
#
# Revision 1.16  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.15  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
#
# Revision 1.14  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.13  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
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


from xml.dom.Element import Element
from xml.dom.Node import Node

rwattrs = ('ID',
           'title',
           'lang',
           'dir',
           'className'
           )

class HTMLElement(Element):

    def __init__(self, ownerDocument, tagName, nodeName):
        Element.__init__(self, ownerDocument, nodeName, '', '',nodeName)
        self.__dict__['tagName'] = tagName

    def _get_ID(self):
        return self.getAttribute('ID')
    
    def _set_ID(self,ID):
        self.setAttribute('ID',ID)

    def _get_title(self):
        return self.getAttribute('TITLE')

    def _set_title(self,title):
        self.setAttribute('TITLE',title)

    def _get_lang(self):
        return self.getAttribute('LANG')

    def _set_lang(self,lang):
        self.setAttribute('LANG',lang)

    def _get_dir(self):
        return self.getAttribute('DIR')

    def _set_dir(self,dir):
        self.setAttribute('DIR',dir)

    def _get_className(self):
        return self.getAttribute('CLASSNAME')

    def _set_className(self,className):
        self.setAttribute('CLASSNAME',className)

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = self.ownerDocument.createElement(self.nodeName)
            else:
                node = newOwner.createElement(self.nodeName)
        return Element.cloneNode(self, deep, node)

#    def _4dom_validateNode(self, newNode):
#        if self.ownerDocument != newNode.ownerDocument:
#            trace("Validate failed, wrong document error")
#            raise DOMException(WRONG_DOCUMENT_ERR)                                           

 #=== BEGIN COMPUTED ATTRIBUTES ===
    ### Attribute Access Mappings ### 

    from xml.dom.Element import Element 

    _readComputedAttrs = Element._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'ID'            : _get_ID, 
         'title'         : _get_title, 
         'lang'          : _get_lang, 
         'dir'           : _get_dir, 
         'className'     : _get_className, 
      }) 

    _writeComputedAttrs = Element._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'ID'            : _set_ID, 
         'title'         : _set_title, 
         'lang'          : _set_lang, 
         'dir'           : _set_dir, 
         'className'     : _set_className, 
      }) 

    # Create the read-only list of attributes 
    _readOnlyAttrs = [] 
    for attr in Element._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

#--- (end HTMLElement.py) ---
