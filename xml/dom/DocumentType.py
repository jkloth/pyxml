########################################################################
#
# File Name:            DocumentType.py
#
# Documentation:        http://docs.4suite.com/4DOM/DocumentType.py.html
#
# History:
# $Log: DocumentType.py,v $
# Revision 1.1  2000/06/06 01:36:05  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.14  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.13  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.12  1999/11/18 07:50:59  molson
# Added namespaces to Nodes
#
# Revision 1.11  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.10  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.9  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.8  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.7  1999/08/29 04:07:59  uche
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
from xml.dom import implementation


class DocumentType(Node):
    nodeType = Node.DOCUMENT_TYPE_NODE

    def __init__(self, name, entities, notations, publicId, systemId):
        Node.__init__(self, None, '', '', '')
        #Initialize defined member variables
        self.__dict__['__nodeName'] = name
        self.__dict__['__entities'] = entities
        self.__dict__['__notations'] = notations
        self.__dict__['__publicId'] = publicId;
        self.__dict__['__systemId'] = systemId;
        #FIXME: No idea what this actually is
        self.__dict__['__internalSubset'] = 'internalSubsetString'

    ### Attribute Methods ###

    def _get_name(self):
        return self.__dict__['__nodeName']

    def _get_entities(self):
        return self.__dict__['__entities']

    def _get_notations(self):
        return self.__dict__['__notations']

    def _get_publicId(self):
        return self.__dict__['__publicId']

    def _get_systemId(self):
        return self.__dict__['__systemId']

    def _get_internalSubset(self):
        return self.__dict__['__internalSubset']

    ### Overridden Methods ###

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = implementation.createDocumentType(self.name, self.publicId, self.systemId)
            else:
                node = implementation.createDocumentType(self.name, self.publicId, self.systemId)
                node._4dom_setOwnerDocument(newOwner)
        return Node.cloneNode(self, deep, node)

    ### Internal Methods ###

    # Behind the back setting of doctype's ownerDocument
    # Also sets the owner of the NamedNodeMaps
    def _4dom_setOwnerDocument(self, newOwner):
        self.__dict__['__ownerDocument'] = newOwner
        self.__dict__['__entities']._4dom_setOwnerDocument(newOwner)
        self.__dict__['__notations']._4dom_setOwnerDocument(newOwner)

    ### Attribute Access Mappings ###

    _readComputedAttrs = Node._readComputedAttrs.copy()
    _readComputedAttrs.update({'name':_get_name,
                               'entities':_get_entities,
                               'notations':_get_notations,
                               'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'internalSubset':_get_internalSubset
                               })


    _writeComputedAttrs = Node._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = Node._readOnlyAttrs
    for attr in _readComputedAttrs.keys():
        if not _writeComputedAttrs.has_key(attr):
            _readOnlyAttrs.append(attr)
