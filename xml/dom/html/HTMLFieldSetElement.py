########################################################################
#
# File Name:            HTMLFieldSetElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLFieldSetElement.py.html
#
# History:
# $Log: HTMLFieldSetElement.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.17  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.16  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.14  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.13  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.12  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.11  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
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

class HTMLFieldSetElement(HTMLFormBasedElement):

    def __init__(self, ownerDocument, nodeName='FIELDSET'):
        HTMLFormBasedElement.__init__(self, ownerDocument, 'FIELDSET', nodeName)

    def _get_form(self):
        return HTMLFormBasedElement._get_form(self)


#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.html.HTMLFormBasedElement import HTMLFormBasedElement 

    _readComputedAttrs = HTMLFormBasedElement._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
      }) 

    _writeComputedAttrs = HTMLFormBasedElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
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

#--- (end HTMLFieldSetElement.py) ---