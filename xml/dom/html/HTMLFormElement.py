#
# File Name:            HTMLFormElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLFormElement.py.html
#
# History:
# $Log: HTMLFormElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.20  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.19  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.18  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.16  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.15  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.14  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.13  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.12  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
#
# Revision 1.11  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.10  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import ext
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.html.HTMLCollection import HTMLCollection

rwattrs = ('name', 'acceptCharset', 'action', 'encType', 'method', 'target')
rattrs = ('elements', 'length')

class HTMLFormElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName=''):
        HTMLElement.__init__(self, ownerDocument, "FORM", nodeName)

    def _get_elements(self):
       #Make a collection of control elements
       nl = self.getElementsByTagName('*')
       l = []
       for child in nl:
           if child.tagName in [
               'BUTTON'
               ,'FIELDSET'
               ,'INPUT'
               ,'ISINDEX'
               ,'LABEL'
               ,'LEGEND'
               ,'OBJECT'
               ,'SELET'
               ,'TEXTAREA'
               ]:                        
               l.append(child)
       return implementation._4dom_createHTMLCollection(l)

    def _get_length(self):
        return self._get_elements().length

    def _get_name(self):
           return self.getAttribute('NAME')

    def _set_name(self,name):
           self.setAttribute('NAME',name)

    def _get_acceptCharset(self):
           return self.getAttribute('ACCEPTCHARSET')

    def _set_acceptCharset(self,acceptcharset):
           self.setAttribute('ACCEPTCHARSET',acceptcharset)

    def _get_action(self):
           return self.getAttribute('ACTION')

    def _set_action(self,action):
           self.setAttribute('ACTION',action)

    def _get_encType(self):
           return self.getAttribute('ENCTYPE')

    def _set_encType(self,enctype):
           self.setAttribute('ENCTYPE',enctype)

    def _get_method(self):
           return self.getAttribute('METHOD')

    def _set_method(self,method):
           self.setAttribute('METHOD',method)

    def _get_target(self):
           return self.getAttribute('TARGET')

    def _set_target(self,target):
           self.setAttribute('TARGET',target)

    def submit(self):
           pass

    def reset(self):
           pass

########################################################################

#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'elements'      : _get_elements, 
         'length'        : _get_length, 
         'name'          : _get_name, 
         'acceptCharset' : _get_acceptCharset, 
         'action'        : _get_action, 
         'encType'       : _get_encType, 
         'method'        : _get_method, 
         'target'        : _get_target, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'name'          : _set_name, 
         'acceptCharset' : _set_acceptCharset, 
         'action'        : _set_action, 
         'encType'       : _set_encType, 
         'method'        : _set_method, 
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

#--- (end HTMLFormElement.py) ---
