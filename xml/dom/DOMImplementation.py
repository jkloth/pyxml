########################################################################
#
# File Name:            DOMImplementation.py
#
# Documentation:        http://docs.4suite.com/4DOM/DOMImplementation.py.html
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string

#At this level we only support XML
FEATURES_MAP = {'XML':2.0,
        'TRAVERSAL':2.0,
        'EVENTS':2.0,
        'MUTATIONEVENTS':2.0
        }

class DOMImplementation:
    def __init__(self):
        self.__mods = {}
        pass

    def hasFeature(self, feature, version=''):
        import string
        featureVersion = FEATURES_MAP.get(string.upper(feature))
        if featureVersion:
            if version and float(version) != featureVersion:
                return 0
            return 1
        return 0

    def createDocumentType(self, qualifiedName, publicId, systemId):
        from xml.dom import DocumentType
        dt = DocumentType.DocumentType(qualifiedName,
                                       self._4dom_createNamedNodeMap(),
                                       self._4dom_createNamedNodeMap(),
                                       publicId,
                                       systemId)
        return dt

    def createDocument(self, namespaceURI, qualifiedName, doctype):
        from xml.dom import Document
        doc = Document.Document(doctype)
        if qualifiedName:
            el = doc.createElementNS(namespaceURI, qualifiedName)
            doc.appendChild(el)
        return doc

    def _4dom_createNodeList(self,list=None):
        if list is None:
            list = []
        from xml.dom import NodeList
        nl = NodeList.NodeList(list)
        return nl

    def _4dom_createNamedNodeMap(self, owner=None):
        from xml.dom import NamedNodeMap
        nnm = NamedNodeMap.NamedNodeMap(owner)
        return nnm


    #This function is defined to abstract imports
    def _4dom_fileImport(self,file,package="xml.dom"):
        mod_map = self.__mods.get(package)
        if mod_map:
            if mod_map.has_key(file):
                return mod_map[file]
        else:
            self.__mods[package] = {}
        mod = __import__(package or file, globals(), locals(), [file])
        if file:
            mod = getattr(mod,file)
        self.__mods[package][file] = mod
        return mod

implementation = DOMImplementation()
