########################################################################
#
# File Name:            DOMImplementation.py
#
# Documentation:        http://docs.4suite.com/4DOM/DOMImplementation.py.html
#
# History:
# $Log: DOMImplementation.py,v $
# Revision 1.3  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.29  2000/09/15 22:38:54  jkloth
# Removed tabs
#
# Revision 1.28  2000/09/15 18:21:21  molson
# Fixed minor import bugs
#
# Revision 1.27  2000/09/14 06:42:25  jkloth
# Fixed circular import errors
#
# Revision 1.26  2000/09/07 15:11:34  molson
# Modified to abstract import
#
# Revision 1.25  2000/08/29 19:29:06  molson
# Fixed initial parameters
#
# Revision 1.24  2000/07/09 19:02:20  uogbuji
# Begin implementing Events
# bug-fixes
#
# Revision 1.23  2000/07/03 02:12:52  jkloth
#
# fixed up/improved cloneNode
# changed Document to handle DTS as children
# fixed miscellaneous bugs
#
# Revision 1.22  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.21  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.20  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.19  2000/01/26 05:53:31  uche
# Fix AVTs
# Implement optimization by delaying and not repeating parser invocation
# Completed error-message framework
# NaN --> None, hopefully temporarily
#
# Revision 1.18  1999/12/10 18:48:48  uche
# Added Copyright files to all packages
# Added HTML pseudo-SAX engine for 4XSLT
# Added xsl:output
# Various bug-fixes.
#
# Revision 1.17  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.16  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.15  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.14  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.13  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.12  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.11  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
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
