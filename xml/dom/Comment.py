########################################################################
#
# File Name:            Comment.py
#
# Documentation:        http://docs.4suite.com/4DOM/Comment.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')

CharacterData = implementation._4dom_fileImport('CharacterData').CharacterData
Node = implementation._4dom_fileImport('Node').Node

class Comment(CharacterData):
    nodeType = Node.COMMENT_NODE

    def __init__(self,ownerDocument,data):
        CharacterData.__init__(self, ownerDocument, data)
        self.__dict__['__nodename'] = '#comment'

    ### Overridden Methods ###

    def __repr__(self):
        st = "<Comment Node at %s: data = '%s%s'>" % (id(self)
                                                   ,self.data[:20]
                                                   ,(len(self.data) > 20 and "..." or "")
                                                   )
        return st
