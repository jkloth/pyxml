########################################################################
#
# File Name:            ProcessingInstruction.py
#
# Documentation:        http://docs.4suite.com/4DOM/ProcessingInstruction.py.html
#
# History:
# $Log: ProcessingInstruction.py,v $
# Revision 1.3  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.21  2000/09/07 15:11:34  molson
# Modified to abstract import
#
# Revision 1.20  2000/07/03 02:12:53  jkloth
#
# fixed up/improved cloneNode
# changed Document to handle DTS as children
# fixed miscellaneous bugs
#
# Revision 1.19  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.18  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.17  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.16  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.15  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.14  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.13  1999/09/09 17:03:42  molson
# Added __repr__ to all Core interfaces
#
# Revision 1.12  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.11  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.10  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

Node = implementation._4dom_fileImport('Node').Node

class ProcessingInstruction(Node):
    nodeType = Node.PROCESSING_INSTRUCTION_NODE

    def __init__(self,ownerDocument,target,data):
        Node.__init__(self,ownerDocument,'','','')
        self.__dict__['__nodeName'] = '#processing-instruction'
        self.__dict__['__target'] = target
        self.__dict__['__nodeValue'] = data

    def _get_target(self):
        return self.__dict__['__target']

    def _get_data(self):
        return self.__dict__['__nodeValue']

    def _set_data(self, newData):
        self.__dict__['__nodeValue'] = newData

    ### Overridden Methods ###

    def __repr__(self):
        return "<Processing Instruction at %s: target = '%s%s', data = '%s%s'>" % (
            id(self),
            self.target[:20],
            len(self.target) > 20 and "..." or "",
            self.data[:20],
            len(self.data) > 20 and "..." or ""
            )

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.target,
                self.data
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'target':_get_target,
                               'data':_get_data
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({'data':_set_data
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
