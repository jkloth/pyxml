'''
core.py: `light' implementation of the Document Object Model (core) level 1.

Reference: http://www.w3.org/TR/WD-DOM/level-one-core

Deviations from the specs:

-- there is currently no DocumentFragment.

So, useful classes in this module are Node (abstract) and its
(concrete) subclasses -- Document, Element, Text, Comment,
ProcessingInstruction -- all of which should be instantiated though
the relevant createXXX() methods on a Document object.  

Typical usage XXX

from xml.dom.core import *

XXX example here
...

'''

import string
from xml.utils import escape

# References inside square brackets, such as [1.5], are to a section in the
# October 1st DOM Level One specification.

#
# Module-level definitions
#

# Exception codes [1.2]
INDEX_SIZE_ERR              = 1
DOMSTRING_SIZE_ERR          = 2
HIERARCHY_REQUEST_ERR       = 3
WRONG_DOCUMENT_ERR          = 4
INVALID_CHARACTER_ERR       = 5
NO_DATA_ALLOWED_ERR         = 6
NO_MODIFICATION_ALLOWED_ERR = 7
NOT_FOUND_ERR               = 8
NOT_SUPPORTED_ERR           = 9
INUSE_ATTRIBUTE_ERR         = 10

# Exceptions (now changed to class-based. --amk)

class DOMException:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg
    
class IndexSizeException(DOMException):
    code = INDEX_SIZE_ERR
class DOMStringSizeException(DOMException):
    code = DOMSTRING_SIZE_ERR
class HierarchyRequestException(DOMException):
    code = HIERARCHY_REQUEST_ERR
class WrongDocumentException(DOMException):
    code = WRONG_DOCUMENT_ERR
class NoDataAllowedException(DOMException):
    code = NO_DATA_ALLOWED_ERR
class NoModificationAllowedException(DOMException):
    code = NO_MODIFICATION_ALLOWED_ERR
class NotFoundException(DOMException):
    code = NOT_FOUND_ERR
class NotSupportedException(DOMException):
    code = NOT_SUPPORTED_ERR
class InUseAttributeException:
    code = INUSE_ATTRIBUTE_ERR

# Old exceptions (deprecated)
class NoSuchNodeException(DOMException): pass
class NotMyChildException(DOMException): pass
class NotImplementedException(DOMException): pass

# Node types. 

ELEMENT                = ELEMENT_NODE                = 1
ATTRIBUTE              = ATTRIBUTE_NODE              = 2
TEXT                   = TEXT_NODE                   = 3
CDATA_SECTION          = CDATA_SECTION_NODE          = 4
ENTITY_REFERENCE       = ENTITY_REFERENCE_NODE       = 5
ENTITY                 = ENTITY_NODE                 = 6
PROCESSING_INSTRUCTION = PROCESSING_INSTRUCTION_NODE = 7
COMMENT                = COMMENT_NODE                = 8
DOCUMENT               = DOCUMENT_NODE               = 9
DOCUMENT_TYPE          = DOCUMENT_TYPE_NODE          = 10
DOCUMENT_FRAGMENT      = DOCUMENT_FRAGMENT_NODE      = 11
NOTATION               = NOTATION_NODE               = 12


def hasFeature(feature, version = None):
    """Test if the DOM implementation implements a specific feature.
    feature -- package name of the feature to test.  In Level 1 DOM the
               legal values are 'HTML' and 'XML'.
    version -- version number of the package to test (optional)
    """
    feature=string.lower(feature)
    
    if feature == 'html': return 0
    if feature == 'xml':
        if version is None: return 1
        if version == '1.0': return 1
        return 0

def createDocument():
    d = _nodeData(DOCUMENT_NODE)
    d.name = '#document'
    d.value = d.attributes = None
    d = Document(d, None, None)
    d._document = d
    return d

import UserList, UserDict

class NodeList(UserList.UserList):
    """An ordered collection of nodes, equivalent to a Python list.  The only
    difference is that an .item() method and a .length attribute are added.
    """
    item = UserList.UserList.__getitem__
    get_length = UserList.UserList.__len__

class NamedNodeMap(UserDict.UserDict):
    """Used to represent a collection of nodes that can be accessed by name.
    Equivalent to a Python dictionary, with various aliases added such as
    getNamedItem and removeNamedItem.
    """

    getNamedItem = UserDict.UserDict.__getitem__
    removeNamedItem = UserDict.UserDict.__delitem__
    get_length = UserDict.UserDict.__len__
    def setNamedItem(self, arg):
        key = arg.nodeName
        self.data[key] = arg

    def item(self, index):
        return self.data.values[ index ]

class _nodeData:
    """Class used for storing the data for a single node.  Instances of
    this class should never be returned to users of the DOM implementation."""
    def __init__(self, type):
        self.type = type
        self.children = []
        self.name = self.value = self.attributes = None
        
class Node:
    '''Base class for grove nodes in DOM model.  Proxies an instance
    of the _nodeData class.'''

    def __init__(self, node, parent = None, document = None):
        self._node = node
        self.parentNode = parent
        self._document = document

    def _index(self):
        "Return the index of this child in its parent's child list"
        if self.parentNode:
            return self.parentNode._node.children._index(self)
        else:
            return -1

    def _checkChild(self, child, parent):
        "Raise HierarchyRequestException if the child can't be added"
        for klass in self.childClasses:
            if isinstance(child, klass): break
        else:
            raise HierarchyRequestException, \
                  "%s cannot be child of %s" % (repr(child), repr(self) )

        cn = child._node ; p=self
        while p is not None:
            if p._node is cn: 
                raise HierarchyRequestException, \
                      "%s is an ancestor of %s" % (repr(child), repr(parent) )
            p = p.parentNode
        
    # get/set attributes

    def get_nodeName(self):
        return self._node.name
    get_name = get_nodeName

    def get_nodeValue(self):
        return self._node.value
    get_value = get_nodeValue

    def get_nodeType(self):
        return self._node.type

    def get_parentNode(self):
        return self.parentNode

    def get_childNodes(self):
        L = self._node.children[:]
        # Convert the list of _nodeData instances into a list of
        # the appropriate Node subclasses
        for i in range(len(L)):
            L[i] =  NODE_CLASS[ L[i].type ] (L[i], self, self._document)
        return NodeList(L)

    def get_firstChild(self):
        if self._node.children:
            n = self._node.children[0]
            return NODE_CLASS[ n.type ] (n, self, self._document)
        else:
            return None

    def get_lastChild(self):
        if self._node.children:
            n = self._node.children[-1]
            return NODE_CLASS[ n.type ] (n, self, self._document)
        else:
            return None

    def get_previousSibling(self):
        if self.parentNode is None: return None
        i = self._index()
        if i <= 0:
            return None
        else:
            n = self.parentNode._node.children[i - 1]
            return NODE_CLASS[ n.type ] (n, self, self._document)

    def get_nextSibling(self):
        if self.parentNode is None: return None
        L = self.parentNode._node.children
        i = self._index()
        if i == -1 or i == len(L) - 1:
            return None
        else:
            return L[i + 1]

    def get_attributes(self):
        return self._node.attributes

    def get_ownerDocument(self):
        return self._document

    # Methods

    def insertBefore(self, newChild, refChild):
        self._checkChild(newChild, self)
        if newChild._document != self._document:
            raise WrongDocumentException("newChild %s created from a "
                                         "different document" % (repr(s),) )

        # If newChild is already in the tree, remove it
        if newChild.parentNode != None:
            newChild.parentNode.removeChild( newChild )

        if refChild == None:
            self.appendChild(newChild)
            return newChild

        L = self._node.children ; n = refChild._node
        for i in range(len(L)):
            if L[i] == n:
                L[i:i] = [newChild._node]
                newChild.parentNode = self
                return newChild
        raise NotFoundException("refChild not a child in insertBefore()")

    def replaceChild(self, newChild, oldChild):
        self._checkChild(newChild, self)
        o = oldChild._node ; L = self._node.children
        for i in range(len(L)):
            if L[i] == o:
                # If newChild is already in the tree, remove it
                if newChild.parentNode != None:
                    newChild.parentNode.removeChild( newChild )

                L[i] = newChild._node
                newChild.parentNode = self
                oldChild.parentNode = None
                return oldChild
        raise NotFoundException("oldChild not a child of this node")

    def removeChild(self, oldChild):
        try:
            self._node.children.remove(oldChild._node)
            oldChild.parentNode = None
            return oldChild
        except ValueError:
            raise NotFoundException("oldChild is not a child of this node")

    def appendChild(self, newChild):
        self._checkChild(newChild, self)
        if newChild._document != self._document:
            raise WrongDocumentException("newChild created from a different document")

        # If newChild is already in the tree, remove it
        if newChild.parentNode != None:
            newChild.parentNode.removeChild( newChild )

        self._node.children.append( newChild._node )
        newChild.parentNode = self
        return newChild

    def hasChildNodes(self):
        return len(self._node.children) > 0

    def cloneNode(self, deep):
        pass # XXX I don't understand the exact definition of cloneNode()

			
class CharacterData(Node):
    # Attributes
    def get_data(self):
        return self._node.value
    
    def set_data(self, data):
        self._node.value = data
        
    def __len__(self):
        return len(self._node.value)
    get_length = __len__

    # Methods
    def substringData(self, offset, count):
        """Extracts a range of data from the object.
        offset -- start of substring to extract count -- number of characters to extract"""
        if offset<0:
            raise IndexSizeException("Negative offset")
        if offset>len(self._node.value):
            raise IndexSizeException("Offset larger than size of data")
        if count<0:
            raise IndexSizeException("Negative-length substring requested")

        return self._node.value[offset:offset+count]

    def appendData(self, arg):
        """Append the string to the end of the character data."""
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.value = self._node.value + arg

    def insertData(self, offset, arg):
        """Insert a string at the specified character offset.
        offset -- character offset at which to insert
        arg -- the string to insert"""
        if offset<0:
            raise IndexSizeException("Negative offset")
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        if offset>len(self._node.value):
            raise IndexSizeException("Offset larger than size of data")
        self._node.value = self._node.value[:offset] + arg + self._node.value[offset:]

    def deleteData(self, offset, count):
        """Remove a range of characters from the node.
        offset -- start of substring to delete
        count -- number of characters to delete"""
        if offset<0:
            raise IndexSizeException("Negative offset")
        if offset>len(self._node.value):
            raise IndexSizeException("Offset larger than size of data")
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.value = self._node.value[:offset] + self._node.value[offset+count:]        

    def replaceData(self, offset, count, arg):
        """Replace the characters starting at the specified offset
        with the specified string.
        offset -- start of substring to delete
        count -- number of characters to delete
        arg -- string with which the range will be replaced"""
        if offset<0:
            raise IndexSizeException("Negative offset")
        if offset>len(self._node.value):
            raise IndexSizeException("Offset larger than size of data")
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.value = self._node.value[:offset] + arg + self._node.value[offset+count:]

    # XXX define __getslice__ & friends here...

    def toxml(self):
        return escape(self._node.value) 
    
class Attr(Node):
    def __init__(self, node, parent = None):
        Node.__init__(self, node, parent, None)

    def __repr__(self):
        return '<Attribute node %s, %s>' % (repr(self._node.name),
                                            repr(self._node.value))

    def get_name(self):
        return self._node.name

    def get_value(self):
        return self._node.value

    def set_value(self, value):
        self._node.value = value
        self._node.specified = 1

    def get_specified(self):
        return self._node.specified

class Element(Node):
    def __init__(self, node, parent = None, document = None):
        Node.__init__(self, node, parent, document)
        
    def __repr__(self):
        return "<Element '%s'>" % (self._node.name)

    def toxml(self):
        s = "<" + self._node.name
        for name, value in self._node.attributes.items():
            s = s + " %s='%s'" % (name, value)
        if len(self._node.children) == 0:
            return s + "/>"
        s = s + '>'
        for child in self._node.children:
            n = NODE_CLASS[ child.type ] (child, self, self._document)
            s = s + n.toxml()
        s = s + "</" + self._node.name + '>'
        return s

    # Attributes
    
    def get_tagName(self):
        return self._node.name

    # Methods
    
    def getAttribute(self, name):
        if self._node.attributes.has_key(name):
            return self._node.attributes[name]
        else:
            return ""
    
    def setAttribute(self, name, value):
        self._node.attributes[name] = value

    def removeAttribute(self, name):
        if self._node.attributes.has_key(name):
            del self._node.attributes[name]

    def getAttributeNode(self, name):
        if not self._node.attributes.has_key[ name ]:
            return None
        d = _nodeData(ATTRIBUTE_NODE)
        d.name = name
        d.value = self._node.attributes[name]
        d.attributes = None
        return Attr(d, None)

    def setAttributeNode(self, newAttr):
        if self._node.attributes.has_key[ newAttr._node.name ]:
            d = _nodeData(ATTRIBUTE_NODE)
            d.name = newAttr._node.name
            d.value = self._node.attributes[ newAttr._node.name]
            d.attributes = None
            retval = Attr(d, None)
        else: retval = None

        self._node.attributes[ newAttr._node.name ] = newAttr._node.value
        return retval

    def removeAttributeNode(self, oldAttr):
        # XXX this needs to know about DTDs to restore a default value
        if self._node.attributes.has_key[ oldAttr._node.name ]:
            d = _nodeData(ATTRIBUTE_NODE)
            d.name = newAttr._node.name
            d.value = self._node.attributes[ oldAttr._node.name ]
            d.attributes = None
            retval = Attr(d, None)
            del self._node.attributes[ d.name ]
            return retval
        else: return None

    def getElementsByTagName(self, tagname):
        L = []
        for child in self._node.children:
            if child.type == ELEMENT:
                d = Element(child, self, self._document)
                if child.name == tagname:
                    L.append(d)
                L = L + d.getElementsByTagName(tagname)
        return NodeList(L)

    def normalize(self):
        # Traverse the list of children, and merge adjacent text nodes
        L = self._node.children
        for i in range(len(L)-1, 0, -1):
            if L[i].type == TEXT_NODE and L[i-1].type == TEXT_NODE:
                # Two text nodes together, so merge them
                # XXX any Text instances proxying the deleted
                # _nodeData instance will find themselves
                # disconnected from the tree.  
                L[i-1].value = L[i-1].value + L[i].value
                del L[i:i+1]
                
        for i in range(len(L)):
            if L[i].type == ELEMENT_NODE:
                n = NODE_CLASS[ L[i].type ] (L[i], self, self._document)
                n.normalize()
    
class Text(CharacterData):
    # Methods

    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Text node %s>' % (repr(s),)
        
    def splitText(self, offset):
        n1 = _nodeData(TEXT_NODE) ; n2 = _nodeData(TEXT_NODE)
        n1.name = "#text" ; n2.name = "#text"
        n1.value = self.substringData(0, offset)
        n2.value = self.substringData(offset, len(self) - offset)
        parent = self.parentNode
        n1 = Text(n1, None, self._document)
        n2 = Text(n2, None, self._document)

        # Insert n1 and n2, and delete this node
        parent.insertBefore(n1, self)
        parent.replaceChild(n2, self)
    
class Comment(CharacterData):
    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Comment node %s>' % (repr(s),)
    
    def toxml(self):
        return '<-- %s -->' % self._node.value

class CDATASection(Text):
    """Represents CDATA sections, which are blocks of text that would
    otherwise be regarded as markup."""
    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<CDATASection node %s>' % (repr(s),)

    def toxml(self):
        return self._node.value

class DocumentType(Node):
    # Attributes
    def get_name(self):
        return self._node.name

    def get_entities(self):
        pass # XXX

    def get_notations(self):
        pass # XXX

class Notation(Node):
    # Attributes
    def get_publicId(self):
        pass # XXX
        
    def get_systemId(self):
        pass # XXX
        
class Entity(Node):
    def get_publicId(self):
        pass # XXX

    def get_systemId(self):
        pass # XXX

    def get_notationName(self):
        pass # XXX

class EntityReference(Node):
    pass 

class ProcessingInstruction(Node):
    def toxml(self):
        return "<? " + self._node.name + ' ' +self._node.target + "?>"

    def get_target(self):
        return self._node.name

    def get_data(self):
        return self._node.target

    def set_data(self, data):
        self._node.target = data


class Document(Node):
    def __init__(self, node, parent = None, document = None):
        Node.__init__(self, node, parent = None, document = None)
        self.documentType = None
        self.documentElement = None
        self.DOMImplementation = __import__(__name__)

    def toxml(self):
        s = '<?xml version="1.0"?>\n'
        s = s + "<!DOCTYPE XXX>\n"
        if len(self._node.children):
            n = self._node.children[0]
            n =  NODE_CLASS[ n.type ] (n, self, self._document)
            s = s + n.toxml()
        return s

    def createElement(self, tagName):
        d = _nodeData(ELEMENT_NODE)
        d.name = tagName
        d.value = None
        d.attributes = NamedNodeMap()
        return Element(d, None, self)

    def createDocumentFragment(self):
        pass #XXX

    def createTextNode(self, data):
        d = _nodeData(TEXT_NODE)
        d.name = "#text"
        d.value = data
        return Text(d, None, self)

    def createComment(self, data):
        d = _nodeData(COMMENT_NODE)
        d.name = "#comment"
        d.value = data
        return Comment(d, None, self)

    def createCDATAsection(self, data):
        d = _nodeData(CDATA_SECTION_NODE)
        d.name = "#cdata-section"
        d.value = data
        return CDATASection(d, None, self)

    def createProcessingInstruction(self, target, data):
        d = _nodeData(PROCESSING_INSTRUCTION_NODE)
        d.name = target
        d.value = data
        return ProcessingInstruction(d, None, self)
        
    def createAttribute(self, name):
        d = _nodeData(ATTRIBUTE_NODE)
        d.name = name
        d.value = ""
        return Attribute(d, None, self)

    def createEntityReference(self, name):
        d = _nodeData(ENTITY_REFERENCE_NODE)
        d.name = name
        d.value = None
        return EntityReference(d, None, self)

    def getElementsByTagName(self, tagname):
        if self.documentElement == None: return []
        L = []
        if self.documentElement._node.name == tagname:
            L.append( self.documentElement )
        return L + self.documentElement.getElementsByTagName(tagname)

    # Attributes
    def get_doctype(self):
        return self.documentType
    def get_implementation(self):
        return self.DOMImplementation
    def get_documentElement(self):
        return self.documentElement

    # Override the Node mutation methods in order to check that
    # there's at most a single Element child, and to update
    # self.documentElement.

    def insertBefore(self, newChild, refChild):
        retval = Node.insertBefore(self, newChild, refChild)
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self, self)
                else:
                    raise HierarchyRequestException, \
                          "Can't add %s; too many Element children of Document" % (repr(newChild),)
        self.documentElement = doc
        
        return retval

    def replaceChild(self, newChild, oldChild):
        retval = Node.replaceChild(self, newChild, oldChild)
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self, self)
                else:
                    raise HierarchyRequestException, \
                          "Can't add %s; too many Element children of Document" % (repr(newChild),)
        self.documentElement = doc
        return retval

    def removeChild(self, oldChild):
        retval = Node.removeChild(self, oldChild)
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self, self)
                else:
                    raise HierarchyRequestException, \
                          "Can't add %s; too many Element children of Document" % (repr(newChild),)
        self.documentElement = doc
        return retval

    def appendChild(self, newChild):
        retval = Node.appendChild(self, newChild)
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self, self)
                else:
                    raise HierarchyRequestException, \
                          "Can't add %s; too many Element children of Document" % (repr(newChild),)
        self.documentElement = doc
        return retval
    
class DocumentFragment(Node):
    pass

# Dictionary mapping types to the corresponding class object

NODE_CLASS = {
ELEMENT_NODE                : Element,
ATTRIBUTE_NODE              : Attr, 
TEXT_NODE                   : Text, 
CDATA_SECTION_NODE          : CDATASection,
ENTITY_REFERENCE_NODE       : EntityReference,
ENTITY_NODE                 : Entity, 
PROCESSING_INSTRUCTION_NODE : ProcessingInstruction, 
COMMENT_NODE                : Comment,
DOCUMENT_NODE               : Document,
DOCUMENT_TYPE_NODE          : DocumentType,
DOCUMENT_FRAGMENT_NODE      : DocumentFragment,
NOTATION_NODE               : Notation
}

# Set the childClasses attributes; we need to do this at the end once
# all the classes have been defined.

Document.childClasses = [Element, ProcessingInstruction, Comment, DocumentType]
DocumentFragment.childClasses = [Element, ProcessingInstruction, Comment,
                                 Text, CDATASection, EntityReference]
DocumentType.childClasses = []
EntityReference.childClasses = [Element, ProcessingInstruction, Comment,
                                Text, CDATASection, EntityReference]
Element.childClasses = [Element, ProcessingInstruction, Comment,
                        Text, CDATASection, EntityReference]
Attr.childClasses = [Text, EntityReference]
ProcessingInstruction.childClasses = []
Comment.childClasses = []
Text.childClasses = []
CDATASection.childClasses = []
Entity.childClasses = [Element, ProcessingInstruction, Comment,
                       Text, CDATASection, EntityReference]
Notation.childClasses = []

# vim:ts=2:ai
