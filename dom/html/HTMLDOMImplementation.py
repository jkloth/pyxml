########################################################################
#
# File Name:            implementation.py
#
# Documentation:        http://docs.4suite.com/4DOM/implementation.py.html
#
# History:
# $Log: HTMLDOMImplementation.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:51  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.11  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
#
# Revision 1.10  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.9  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.8  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.6  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.5  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.4  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.3  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.2  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.1  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.DOMImplementation import DOMImplementation

class HTMLDOMImplementation(DOMImplementation):

    def __init__(self):
        DOMImplementation.__init__(self)
    
    def createHTMLDocument(self, title):
        pass
        from xml.dom.html import HTMLDocument
        #from xml.dom.DocumentType import DocumentType
        doc = HTMLDocument.HTMLDocument()
        h = doc.createElement('HTML')
        doc.appendChild(h)
        doc._set_title(title)
        return doc

#Not in DOM HTML Level 2
#    def cloneImplementation(self):
#        imp = implementation(self.factory)
#   imp.feature = self.feature
#   imp.version = self.version
#   return imp

    def _4dom_createHTMLCollection(self,list=[]):
        pass
        from xml.dom.html import HTMLCollection
        hc = HTMLCollection.HTMLCollection(list)
        return hc
