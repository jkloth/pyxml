########################################################################
#
# File Name:            CDATASection.py
#
# Documentation:        http://docs.4suite.com/4DOM/CDATASection.py.html
#
"""
Implementation of DOM Level 2 CDATASection interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Text = implementation._4dom_fileImport('Text').Text

class CDATASection(Text):
    nodeType = dom.Node.CDATA_SECTION_NODE

    def __init__(self, ownerDocument, data):
        Text.__init__(self, ownerDocument, data)
        self.__dict__['__nodeName'] = "#cdata-section"

    ### Overridden Methods ###

    def __repr__(self):
        return "<CDATA Section at %s: data = '%s%s'>" % (
            id(self)
            ,self.data[:20]
            ,(len(self.data) > 20 and "..." or "")
            )


