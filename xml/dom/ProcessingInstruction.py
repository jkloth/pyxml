########################################################################
#
# File Name:            ProcessingInstruction.py
#
# Documentation:        http://docs.4suite.com/4DOM/ProcessingInstruction.py.html
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
