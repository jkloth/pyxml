########################################################################
#
# File Name:            CharacterData.py
#
# Documentation:        http://docs.4suite.com/4DOM/CharacterData.py.html
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

DOMException = dom.DOMException
INDEX_SIZE_ERR = dom.INDEX_SIZE_ERR
SYNTAX_ERR = dom.SYNTAX_ERR

import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]

class CharacterData(Node):
    def __init__(self, ownerDocument, data):
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeValue'] = data
        self.__dict__['__length'] = len(data)

    ### Attribute Methods ###

    def _get_data(self):
        return self.__dict__['__nodeValue']

    def _set_data(self, data):
        if data != None and type(data) not in g_stringTypes:
            raise DOMException(SYNTAX_ERR)
        old_value = self.__dict__['__nodeValue']
        self.__dict__['__nodeValue'] = data
        self.__dict__['__length'] = len(data)
        self._4dom_fireMutationEvent('DOMCharacterDataModified',
                                     prevValue=old_value,
                                     newValue=data)        

    def _get_length(self):
        return self.__dict__['__length']

    ### Methods ###

    def substringData(self, offset, count):
        if count < 0 or offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR);
        return self.data[int(offset):int(offset+count)]

    def appendData(self, arg):
        if type(arg) not in g_stringTypes:
            raise DOMException(SYNTAX_ERR)
        old_value = self.__dict__['__nodeValue']
        self._set_data(self.data + arg)
        self._4dom_fireMutationEvent('DOMCharacterDataModified',
                                     prevValue=old_value,
                                     newValue=self.__dict__['__nodeValue'])
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return
        
    def insertData(self, offset, arg):
        if type(arg) not in g_stringTypes:
            raise DOMException(SYNTAX_ERR)
        if offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR)
        st = self.__dict__['__nodeValue']
        old_value = st
        st = st[:int(offset)] + arg + st[int(offset):]
        self._set_data(st)
        self._4dom_fireMutationEvent('DOMCharacterDataModified',
                                     prevValue=old_value,
                                     newValue=st)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def deleteData(self, offset, count):
        if count < 0 or offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR);
        old_value = self.__dict__['__nodeValue']
        st = self.data[:int(offset)] + self.data[int(offset+count):]
        self._set_data(st);
        self._4dom_fireMutationEvent('DOMCharacterDataModified',
                                     prevValue=old_value,
                                     newValue=st)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        return

    def replaceData(self, offset, count, arg):  
        if type(arg) not in g_stringTypes:
            raise DOMException(SYNTAX_ERR)
        #Really a delete, then an insert
        self.deleteData(offset, count)
        if (offset+count) >= self.__dict__['__length']:
            self.appendData(arg);
        else:
            self.insertData(offset, arg);
        return

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.data
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({
        'length':_get_length,
        'data':_get_data
        })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        'data':_set_data
        })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Node._readOnlyAttrs + _readComputedAttrs.keys())
