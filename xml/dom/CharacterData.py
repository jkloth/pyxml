########################################################################
#
# File Name:            CharacterData.py
#
# Documentation:        http://docs.4suite.com/4DOM/CharacterData.py.html
#
# History:
# $Log: CharacterData.py,v $
# Revision 1.1  2000/06/06 01:36:04  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.21  2000/05/24 04:05:47  uogbuji
# fixed tab issues
# fixed nasty recursion bug in HtmlLib
#
# Revision 1.20  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.19  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.18  1999/11/18 08:03:24  molson
# Added Namespaces to Character Data
#
# Revision 1.17  1999/11/18 07:23:01  molson
# Removed factories
#
# Revision 1.16  1999/11/18 05:21:40  molson
# Modified CharacterData and all Derivitives to work with new interface
#
# Revision 1.15  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.14  1999/09/14 03:42:43  uche
# XXX -> FIXME
# Fix retrieval of attr values
#
# Revision 1.13  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.12  1999/08/31 14:45:51  molson
# Tested over the orb with Fnorb
#
# Revision 1.11  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Node import Node

from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR
from xml.dom import SYNTAX_ERR

class CharacterData(Node):
    def __init__(self, ownerDocument, data):
        Node.__init__(self, ownerDocument, '', '', '')
        self.__dict__['__nodeValue'] = data
        self.__dict__['__length'] = len(data)

    ### Attribute Methods ###

    def _get_data(self):
        return self.__dict__['__nodeValue']

    def _set_data(self, data):
        if data != None and type(data) != type(''):
            raise DOMException(SYNTAX_ERR)
        self.__dict__['__nodeValue'] = data
        self.__dict__['__length'] = len(data)

    def _get_length(self):
        return self.__dict__['__length']

    ### Methods ###

    def substringData(self, offset, count):
        if count < 0 or offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR);
        return self.data[int(offset):int(offset+count)]

    def appendData(self, arg):
        if type(arg) != type(''):
            raise DOMException(SYNTAX_ERR)
        self._set_data(self.data + arg)
        return
        
    def insertData(self, offset, arg):
        if type(arg) != type(''):
            raise DOMException(SYNTAX_ERR)
        if offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR)
        st = self.__dict__['__nodeValue']
        st = st[:int(offset)] + arg + st[int(offset):]
        self._set_data(st)
        return

    def deleteData(self, offset, count):
        if count < 0 or offset < 0 or offset >= self.__dict__['__length']:
            raise DOMException(INDEX_SIZE_ERR);
        st = self.data[:int(offset)] + self.data[int(offset+count):]
        self._set_data(st);
        return

    def replaceData(self, offset, count, arg):  
        if type(arg) != type(''):
            raise DOMException(SYNTAX_ERR)
        #Really a delete, then an insert
        self.deleteData(offset, count)
        if (offset+count) >= self.__dict__['__length']:
            self.appendData(arg);
        else:
            self.insertData(offset, arg);
        return

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'length':_get_length,
                               'data':_get_data
                       })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({'data':_set_data
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = Node._readOnlyAttrs
    for attr in _readComputedAttrs.keys():
        if not _writeComputedAttrs.has_key(attr):
            _readOnlyAttrs.append(attr)
