
# An adapter for Java DOM implementations that makes it possible to
# access them through the same interface as the Python DOM
# implementation.
#
# $Id: javadom.py,v 1.1 2000/05/17 14:09:01 lars Exp $

# For now based on Sun's Java Project X.

# Todo:
# - implement remaining Python parts of NodeList and NamedNodeMap
# - more 4DOM-like interface? support _get_* ?
# - make a test suite
# - support more DOM implementations
#   - find a scheme for doing this
# - support level 2
# - get rid of FIXMEs

import string

def filetourl(file):
    # A Python port of James Clark's fileToURL from XMLTest.java.
    from java.io import File
    from java.net import URL
    from java.lang import System
    
    file = File(file).getAbsolutePath()
    sep = System.getProperty("file.separator")

    if sep != None and len(sep) == 1:
        file = file.replace(sep[0], '/')

    if len(file) > 0 and file[0] != '/':
        file = '/' + file

    return URL('file', None, file).toString()

def createDocument():
    from com.sun.xml.tree import XmlDocument
    return Document(XmlDocument())

def buildDocumentString(string):
    from com.sun.xml.tree import XmlDocumentBuilder
    return Document(XmlDocumentBuilder.createXmlDocument(string))    

def buildDocumentUrl(url):
    from com.sun.xml.tree import XmlDocument
    return Document(XmlDocument.createXmlDocument(url))

def buildDocumentFile(filename):
    return buildDocumentUrl(filetourl(filename))

# ===== Utilities

def _wrap_node(node):
    if node == None:
        return None
    
    return NODE_CLASS_MAP[node.getNodeType()] (node)

# ===== Constants

ELEMENT_NODE                = 1
ATTRIBUTE_NODE              = 2
TEXT_NODE                   = 3
CDATA_SECTION_NODE          = 4
ENTITY_REFERENCE_NODE       = 5
ENTITY_NODE                 = 6
PROCESSING_INSTRUCTION_NODE = 7
COMMENT_NODE                = 8
DOCUMENT_NODE               = 9
DOCUMENT_TYPE_NODE          = 10
DOCUMENT_FRAGMENT_NODE      = 11
NOTATION_NODE               = 12

# ===== DOMImplementation

class DOMImplementation:

    def __init__(self, impl):
        self._impl = impl

    def hasFeature(self, feature, version):
        if version == None or version == "1.0":
            return string.lower(feature) == "xml" and \
                   self._impl.hasFeature(feature, version)
        else:
            return 0

    def __repr__(self):
        return "<DOMImplementation javadom.py, using '%s'>" % self._impl

# ===== Node

class Node:

    def __init__(self, impl):
        self._impl = impl

    # attributes
        
    def get_nodeName(self):
        return self._impl.getNodeName()

    def get_nodeValue(self):
        return self._impl.getNodeValue()

    def get_nodeType(self):
        return self._impl.getNodeType()

    def get_parentNode(self):
        return _wrap_node(self._impl.getParentNode())

    def get_childNodes(self):
        children = self._impl.getChildNodes()
        if children is None:
            return children
        else:
            return NodeList(children)

    def get_firstChild(self):
        return _wrap_node(self._impl.getFirstChild())

    def get_lastChild(self):
        return _wrap_node(self._impl.getLastChild())
        
    def get_previousSibling(self):
        return _wrap_node(self._impl.getPreviousSibling())
        
    def get_nextSibling(self):
        return _wrap_node(self._impl.getNextSibling())
        
    def get_ownerDocument(self):
        return _wrap_node(self._impl.getOwnerDocument())

    def get_attributes(self):
        atts = self._impl.getAttributes()
        if atts is None:
            return None
        else:
            return NamedNodeMap(atts)
    
    # methods

    def insertBefore(self, new, neighbour):
        self._impl.insertBefore(new._impl, neighbour._impl)

    def replaceChild(self, new, old):
        self._impl.replaceChild(new._impl, old._impl)
        return old

    def removeChild(self, old):
        self._impl.removeChild(old._impl)
        return old

    def appendChild(self, new):
        self._impl.appendChild(new._impl)

    def hasChildNodes(self):
        return self._impl.hasChildNodes()

    def cloneNode(self):
        return _wrap_node(self._impl.cloneNode())

    # attribute access

    def __getattr__(self, name):
        if name[ :4] != "get_" and hasattr(self, "get_" + name):
            return getattr(self, "get_" + name) ()
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name[ :4] != "set_" and hasattr(self, "set_" + name):
            getattr(self, "set_" + name) (value)
        else:
            raise AttributeError(name)
        
# ===== Document

class Document(Node):
        
    # methods

    def createTextNode(self, data):
        return Text(self._impl.createTextNode(data))

    def createEntityReference(self, ):
        return EntityReference(self._impl.createEntityReference())

    def createElement(self, name):
        return Element(self._impl.createElement(name))

    def createDocumentFragment(self):
        return DocumentFragment(self._impl.createDocumentFragment())

    def createComment(self, data):
        return Comment(self._impl.createComment(data))

    def createCDATASection(self, data):
        return CDATASection(self._impl.createCDATASection(data))

    def createProcessingInstruction(self, target, data):
        return ProcessingInstruction(self._impl.createProcessingInstruction(target, data))

    def createAttribute(self, name):
        return Attr(self._impl.createAttribute(name))

    def getElementsByTagName(self, name):
        return NodeList(self._impl.getElementsByTagName(name))
        
    # attributes

    def get_doctype(self):
        return self._impl.getDoctype()

    def get_implementation(self):
        return DOMImplementation(self._impl.getImplementation())

    def get_documentElement(self):
        return _wrap_node(self._impl.getDocumentElement())

    def __repr__(self):
        docelm = self._impl.getDocumentElement()
        if docelm:
            return "<Document with root '%s'>" % docelm.getTagName()
        else:
            return "<Document with no root>"
    
# ===== Element

class Element(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_tagName     = self._impl.getTagName
        self.getAttribute    = self._impl.getAttribute
        self.setAttribute    = self._impl.setAttribute
        self.removeAttribute = self._impl.removeAttribute
        self.normalize       = self._impl.normalize

    def getAttributeNode(self, name):
        return Attr(self._impl.getAttributeNode(name))

    def setAttributeNode(self, attr):
        self._impl.setAttributeNode(attr._impl)

    def removeAttributeNode(self, attr):
        self._impl.removeAttributeNode(attr._impl)

    def getElementsByTagName(self, name):
        return NodeList(self._impl.getElementsByTagName(name))

    def __repr__(self):
        return "<Element '%s' with %d attributes and %d children>" % \
               (self._impl.getTagName(),
                self._impl.getAttributes().getLength(),
                self._impl.getChildNodes().getLength())
    
# ===== CharacterData

class CharacterData(Node):
        
    def __init__(self, impl):
        Node.__init__(self, impl)
        
        self.get_data      = self._impl.getData
        self.set_data      = self._impl.setData
        self.get_length    = self._impl.getLength
        
        self.substringData = self._impl.substringData
        self.appendData    = self._impl.appendData
        self.insertData    = self._impl.insertData
        self.deleteData    = self._impl.deleteData
        self.replaceData   = self._impl.replaceData
        
# ===== Comment

class Comment(CharacterData):

    def __repr__(self):
        return "<Comment of length %d>" % self.getLength()

# ===== ProcessingInstruction

class ProcessingInstruction(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_target = self._impl.getTarget
        self.get_data   = self._impl.getData
        self.set_data   = self._impl.setData

    def __repr__(self):
        return "<PI with target '%s'>" % self._impl.getTarget()
        
# ===== Text

class Text(CharacterData):

    def splitText(self, offset):
        return Text(self._impl.splitText(offset))

    def __repr__(self):
        return "<Text of length %d>" % self._impl.getLength()
    
# ===== CDATASection

class CDATASection(Text):

    def __repr__(self):
        return "<CDATA section of length %d>" % self._impl.getLength()
    
# ===== Attr

class Attr(Node):
        
    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_name      = self._impl.getName
        self.get_specified = self._impl.getSpecified
        self.get_value     = self._impl.setValue
        self.set_value     = self._impl.setValue

    def __repr__(self):
        return "<Attr '%s'>" % self._impl.getName()
        
# ===== EntityReference

class EntityReference(Node):

    def __repr__(self):
        return "<EntityReference '%s'>" % self.getNodeName()
        
# ===== DocumentType

class DocumentType(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_name = self._impl.getName

    def get_entities(self):
        return NamedNodeMap(self._impl.getEntities())

    def get_notations(self):
        return NamedNodeMap(self._impl.getNotations())

    def __repr__(self):
        return "<DocumentType '%s'>" % self._impl.getNodeName()
    
# ===== Notation

class Notation(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_publicId = self._impl.getPublicId
        self.get_systemId = self._impl.getSystemId

    def __repr__(self):
        return "<Notation '%s'>" % self._impl.getNodeName()
        
# ===== Entity

class Entity(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.get_publicId = self._impl.getPublicId
        self.get_systemId = self._impl.getSystemId
        self.get_notationName = self._impl.getNotationName

    def __repr__(self):
        return "<Entity '%s'>" % self._impl.getNodeName()
        
# ===== DocumentFragment

class DocumentFragment(Node):

    def __repr__(self):
        return "<DocumentFragment>"
        
# ===== NodeList

class NodeList:

    def __init__(self, impl):
        self._impl = impl

        self.__len__    = self._impl.getLength
        self.get_length = self._impl.getLength
        self.item       = self._impl.item

    # Python list methods
        
    def __getitem__(self, ix):
        node = self._impl.item(ix)
        if node is None:
            raise IndexError
        else:
            return _wrap_node(node)

    def __setitem__(self, ix, item):
        raise TypeError, "NodeList instances don't support item assignment"

    def __delitem__(self, ix, item):
        raise TypeError, "NodeList instances don't support item deletion"

    def __setslice__(self, i, j, list):
        raise TypeError, "NodeList instances don't support slice assignment"
    
    def __delslice__(self, i, j):
        raise TypeError, "NodeList instances don't support slice deletion"

    def append(self, item): 
        raise TypeError, "NodeList instances don't support .append()"
    
    def insert(self, i, item):
        raise TypeError, "NodeList instances don't support .insert()"
    
    def pop(self, i=-1): 
        raise TypeError, "NodeList instances don't support .pop()"
    
    def remove(self, item): 
        raise TypeError, "NodeList instances don't support .remove()"
    
    def reverse(self): 
        raise TypeError, "NodeList instances don't support .reverse()"
    
    def sort(self, *args): 
        raise TypeError, "NodeList instances don't support .sort()"

    def __repr__(self):        
        return "<NodeList [ %s ]>" % string.join(map(repr, self), ", ")
    
    # FIXME: getslice, add, radd, mul, rmul, count, index
    
# ===== NamedNodeMap

class NamedNodeMap:

    def __init__(self, impl):
        self._impl = impl

        self.get_length = self._impl.getLength
        self.__len__    = self._impl.getLength

    def getNamedItem(self, name):
        return _wrap_node(self._impl.getNamedItem(name))

    def setNamedItem(self, node):
        return _wrap_node(self._impl.setNamedItem(node._impl))

    def removedNamedItem(self, name):
        return _wrap_node(self._impl.removedNamedItem(name))

    def item(self, index):
        return _wrap_node(self._impl.item(index))

    # Python dictionary methods
    
    def __getitem__(self, key):
        node = self._impl.getNamedItem(name)
        if node is None:
            raise KeyError, key
        else:
            return _wrap_node(node)

    def get(self, key, alternative = None):
        node = self._impl.getNamedItem(name)
        if node is None:
            return alternative
        else:
            return _wrap_node(node)        
        
    def has_key(self, key):
        return self._impl.getNamedItem(name) != None

    def items(self):
        list = []
        for ix in range(self._impl.getLength()):
            node = self._impl.item(ix)
            list.append((node.getNodeName(), _wrap_node(node)))
        return list

    def keys(self):
        list = []
        for ix in range(self._impl.getLength()):
            list.append(self._impl.item(ix).getNodeName())
        return list

    def values(self):
        list = []
        for ix in range(self._impl.getLength()):
            list.append(_wrap_node(self._impl.item(ix)))
        return list        

    def __repr__(self):
        pairs = []
        for pair in self.items():
            pairs.append("'%s' : %s" % pair)
        return "<NamedNodeMap { %s }>" % string.join(pairs, ", ")
    
    # FIXME! setitem, update
    
# ===== Various stuff

NODE_CLASS_MAP = {
    ELEMENT_NODE : Element,
    ATTRIBUTE_NODE : Attr,
    TEXT_NODE : Text,
    CDATA_SECTION_NODE : CDATASection,
    ENTITY_REFERENCE_NODE : EntityReference,
    ENTITY_NODE : Entity,
    PROCESSING_INSTRUCTION_NODE : ProcessingInstruction,
    COMMENT_NODE : Comment,
    DOCUMENT_NODE : Document,
    DOCUMENT_TYPE_NODE : DocumentType,
    DOCUMENT_FRAGMENT_NODE : DocumentFragment,
    NOTATION_NODE : Notation
    }
    
# ===== Self-test

if __name__ == "__main__":
    doc2 = createDocument()
    print doc2
    print doc2.get_implementation()
    root = doc2.createElement("doc")
    print root
    doc2.appendChild(root)
    txt = doc2.createTextNode("This is a simple sample \n")
    print txt
    root.appendChild(txt)

    print root.get_childNodes()[0]
    print root.get_childNodes()    

    root.setAttribute("huba", "haba")
    print root
    print root.get_attributes()
