########################################################################
#
# File Name:            HTMLMetaElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLMetaElement.py.html
#
# History:
# $Log: HTMLMetaElement.py,v $
# Revision 1.1  2000/06/06 01:36:08  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.16  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.15  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.14  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.13  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.11  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.10  2000/05/03 23:38:16  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.9  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.8  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.7  1999/08/29 04:08:00  uche
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

rwattrs = ('content', 'httpEquiv', 'scheme')

class HTMLMetaElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='META'):
        HTMLElement.__init__(self, ownerDocument, "META", nodeName)

    def _get_content(self):
        return self.getAttribute('CONTENT')

    def _set_content(self,content):
        self.setAttribute('CONTENT',content)

    def _get_httpEquiv(self):
        return self.getAttribute('HTTP-EQUIV')

    def _set_httpEquiv(self,http_equiv):
        self.setAttribute('HTTP-EQUIV',http_equiv)

    def _get_scheme(self):
        return self.getAttribute('SCHEME')

    def _set_scheme(self,scheme):
        self.setAttribute('SCHEME',scheme)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLElement import HTMLElement 

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'content'       : _get_content, 
         'httpEquiv'     : _get_httpEquiv, 
         'scheme'        : _get_scheme, 
      }) 

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'content'       : _set_content, 
         'httpEquiv'     : _set_httpEquiv, 
         'scheme'        : _set_scheme, 
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

#--- (end HTMLMetaElement.py) ---
