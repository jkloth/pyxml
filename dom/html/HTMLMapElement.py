########################################################################
#
# File Name:            HTMLMapElement.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLMapElement.py.html
#
# History:
# $Log: HTMLMapElement.py,v $
# Revision 1.1  2000/06/20 15:40:53  uche
# Initial revision
#
# Revision 1.21  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
#
# Revision 1.20  2000/05/24 18:48:10  molson
# Fixed the bl;oody tabs in HTML.  Damn you pico, damn you
#
# Revision 1.19  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.18  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.17  2000/05/05 19:58:12  pweinstein
# zdom/python xml-sig bake-0 conversion completed, tested with internal FT app (TT)
#
# Revision 1.16  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.14  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.13  2000/05/03 23:38:16  pweinstein
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
# Revision 1.9  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.8  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.Node import Node
from xml.dom import implementation

class HTMLMapElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='MAP'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_areas(self):
        rt =  self.getElementsByTagName('AREA')
        return implementation._4dom_createHTMLCollection(rt)

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
        'areas' : _get_areas,
        'name'  : _get_name
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({
        'name'  : _set_name
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
