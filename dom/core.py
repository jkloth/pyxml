"""
core.py: `light' implementation of the Document Object Model (core) level 1.

Reference: http://www.w3.org/TR/1998/REC-DOM-Level-1-19981001/

Deviations from the specs:

 XXX not documented yet -- one hopes there are none :)

Useful classes in this module are Node (abstract) and its
(concrete) subclasses -- Document, Element, Text, Comment,
ProcessingInstruction -- all of which should be instantiated though
the relevant create{Element,TextNode,Comment,...}() methods on a
Document object.  

Typical usage:

from xml.dom.core import *

doc = core.createDocument()
html = doc.createElement('html')
html.setAttribute('attr', 'value')
head = doc.createElement('head')
title = doc.createElement('title')

text = doc.createTextNode("Title goes here")
title.appendChild( text )

print doc.toxml()
...

"""

import string, sys
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
    """DOM operations only raise exceptions in "exceptional" circumstances,
     i.e., when an operation is impossible to perform (either for logical
     reasons, because data is lost, or because the implementation has become
     unstable). In general, DOM methods return specific error values in
     ordinary processing situations, such as out-of-bound errors when using
     NodeList.
     """
    
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
    "Create a fresh Document object and return it"
    d = _nodeData(DOCUMENT_NODE)
    d.name = '#document'
    d.value = d.attributes = None
    d = Document(d, None, None)
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
    Node_counter = 0
    def __init__(self, type):
        self.type = type
        self.children = []
        self.name = self.value = self.attributes = None
        _nodeData.Node_counter = _nodeData.Node_counter + 1
#        print '_nodeData\tinit\t%s\t%s' % (_nodeData.Node_counter, self.name)

    def __del__(self):
        _nodeData.Node_counter = _nodeData.Node_counter -1
#        print '_nodeData\tdel\t%s\t%s' % (_nodeData.Node_counter, self.name)


class Node:
    """Base class for grove nodes in DOM model.  Proxies an instance
    of the _nodeData class."""

    readonly = 0
    Node_counter = 0
    def __init__(self, node, parent = None, document = None):
        self._node = node
        self.parentNode = parent
        self._document = document
        Node.Node_counter = Node.Node_counter + 1
#        print 'Node      \tinit\t%s\t%s' % (Node.Node_counter, self.get_nodeName())

    def __del__(self):
        Node.Node_counter = Node.Node_counter -1
#        print 'Node      \tdel\t%s\t%s' % (Node.Node_counter, self.get_nodeName())

    def _index(self):
        "Return the index of this child in its parent's child list"
        if self.parentNode:
            return self.parentNode._node.children._index(self)
        else:
            return -1

    def _checkChild(self, child, parent):
        "Raise HierarchyRequestException if the child can't be added"

        cn = child._node ; p=self
        while p is not None:
            if p._node is cn: 
                raise HierarchyRequestException, \
                      "%s is an ancestor of %s" % (repr(child), repr(parent) )
            p = p.parentNode

    def __getattr__(self, key):
        if key[0:4] == 'get_' or key[0:4] == 'set_':
            raise AttributeError, repr(key[4:])
        func = getattr(self, 'get_'+key)
        return func()

    def __setattr__(self, key, value):
        if hasattr(self, 'set_'+key):
            func = getattr(self, 'set_'+key)
            func( value )
        self.__dict__[key] = value
        
    # get/set attributes

    def get_nodeName(self):
        "Returns the name of this node."
        return self._node.name
    
    get_name = get_nodeName

    def get_nodeValue(self):
        "Returns the value of this node."
        return self._node.value
    get_value = get_nodeValue

    def get_nodeType(self):
        "Returns the type of this node."
        return self._node.type

    def get_parentNode(self):
        """Return the parent of this node. All nodes, except Document,
        DocumentFragment, and Attr may have a parent. However, if a
        node has just been created and not yet added to the tree, or
        if it has been removed from the tree, this is null."""
        return self.parentNode

    def get_childNodes(self):
        """Return a NodeList containing all children of this node. If there
        are no children, this is a NodeList containing no nodes."""

        # Copy the list, because we're going to modify it
        L = self._node.children[:]

        # Convert the list of _nodeData instances into a list of
        # the appropriate Node subclasses
        for i in range(len(L)):
            L[i] =  NODE_CLASS[ L[i].type ] (L[i], self, self.get_ownerDocument() )
        return NodeList(L)

    def get_firstChild(self):
        """Return the first child of this node. If there is no such node, this
        returns null."""

        if self._node.children:
            n = self._node.children[0]
            return NODE_CLASS[ n.type ] (n, self, self.get_ownerDocument() )
        else:
            return None

    def get_lastChild(self):
        """Return the last child of this node. If there is no such node, this
        returns null."""
        if self._node.children:
            n = self._node.children[-1]
            return NODE_CLASS[ n.type ] (n, self, self._document)
        else:
            return None

    def get_previousSibling(self):
        """Return the node immediately preceding this node. If there is no such
        node, this returns null."""

        if self.parentNode is None: return None
        i = self._index()
        if i <= 0:
            return None
        else:
            n = self.parentNode._node.children[i - 1]
            return NODE_CLASS[ n.type ] (n, self, self._document)

    def get_nextSibling(self):
        """Return the node immediately following this node. If there is no such
        node, this returns null."""
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
        """The Document object associated with this node. This is also
        the Document object used to create new nodes. When this node
        is a Document this is null."""
        return self._document

    # Methods

    def insertBefore(self, newChild, refChild):
        """Inserts the node newChild before the existing child node
        refChild. If refChild is null, insert newChild at the end of
        the list of children.
        
        If newChild is a DocumentFragment object, all of its children
        are inserted, in the same order, before refChild. If the
        newChild is already in the tree, it is first removed."""

        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)
        self._checkChild(newChild, self)

        if newChild._document != self._document:
            raise WrongDocumentException("newChild %s created from a "
                                         "different document" % (repr(newChild),) )

        # If newChild is already in the tree, remove it
        if newChild.parentNode != None:
            newChild.parentNode.removeChild( newChild )

        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            nodelist = newChild._node.children
        else:
            nodelist = [ newChild._node ]

        for node in nodelist:
            if node.type not in self.childNodeTypes:
                node = NODE_CLASS[ node.type ] (node, self, self._document)
                raise HierarchyRequestException, \
                      "%s cannot be child of %s" % (repr(node), repr(self) )

        if refChild == None:
            for node in nodelist:
                self._node.children.append( node )
                
            if newChild._node.type != DOCUMENT_FRAGMENT_NODE:
                newChild.parentNode = self
            return newChild

        L = self._node.children ; n = refChild._node
        for i in range(len(L)):
            if L[i] == n:
                L[i:i] = nodelist
                if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
                    newChild._node.children = []
                else:
                    newChild.parentNode = self
                return newChild

        raise NotFoundException("refChild not a child in insertBefore()")

    def replaceChild(self, newChild, oldChild):
        """Replaces the child node oldChild with newChild in the list of
        children, and returns the oldChild node. If the newChild is
        already in the tree, it is first removed."""
        
        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)
        self._checkChild(newChild, self)

        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            for node in newChild._node.children:
                if node.type not in self.childNodeTypes:
                    node = NODE_CLASS[ node.type ] (node, self, self._document)
                    raise HierarchyRequestException, \
                          "%s cannot be child of %s" % (repr(node), repr(self) )

        o = oldChild._node ; L = self._node.children
        for i in range(len(L)):
            if L[i] == o:
                # If newChild is already in the tree, remove it
                if newChild.parentNode != None:
                    newChild.parentNode.removeChild( newChild )

                if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
                    L[i:i+1] = newChild._node.children
                    newChild._node.children = []
                else:
                    L[i] = newChild._node
                    newChild.parentNode = self
                    
                oldChild.parentNode = None
                return oldChild

        raise NotFoundException("oldChild not a child of this node")

    def removeChild(self, oldChild):
        """Removes the child node indicated by oldChild from the list of
        children, and returns it."""

        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)

        try:
            self._node.children.remove(oldChild._node)
            oldChild.parentNode = None
            return oldChild
        except ValueError:
            raise NotFoundException("oldChild is not a child of this node")

    def appendChild(self, newChild):
        """Adds the node newChild to the end of the list of children of
        this node. If the newChild is already in the tree, it is
        first removed."""

        self.insertBefore(newChild,None)
        return

    def hasChildNodes(self):
        """Return true if the node has any children, false if the node has
        no children."""

        return len(self._node.children) > 0

    def cloneNode(self, deep):
        """Returns a duplicate of this node, i.e., serves as a generic
        copy constructor for nodes. The duplicate node has no parent
        (parentNode returns null.)."""
        
        import copy
        d = _nodeData( self._node.type )
        for key, value in self._node.__dict__.items():
            if key == 'children' or key[0:2] == '__':
                continue
            else:
                setattr(d, key, copy.deepcopy(value) )

        node = NODE_CLASS[ d.type ] (d, None, self.get_ownerDocument())
        if deep:
            d.children = copy.deepcopy(self._node.children)
        return node

class CharacterData(Node):
    # Attributes
    def get_data(self):
        "Return the character data of the node."
        return self._node.value
    
    def set_data(self, data):
        "Set the character data of the node to a new value"
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.value = data
        
    def __len__(self):
        "Return the length of the node's character data."
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

    def toxml(self):
        return escape(self._node.value) 

    # Methods to make slicing work naturally
    def __delslice__(self, i, j):
        v = self._node.value
        self._node.value = v[:i] + v[j:]

    def __setslice__(self, i, j, seq):
        if isinstance(seq, CharacterData):
            seq = seq._node.value
        v = self._node.value
        self._node.value = v[:i] + seq + v[j:]

    def __getslice__(self, i,j):
        value = self._node.value[i:j]
        return self._document.createTextNode( value )

    
class Attr(Node):
    childNodeTypes = [TEXT_NODE, ENTITY_REFERENCE_NODE]
    
    def __init__(self, node, parent = None, document = None):
        Node.__init__(self, node, None, document)

    def __repr__(self):
        return '<Attribute node %s>' % (repr(self._node.name),)

    def toxml(self):
        s = ""
        for c in self._node.children:
            if c.type == TEXT_NODE:
                s = s + c.value
            elif c.type == ENTITY_REFERENCE_NODE:
                s = s + '&' + c.name + ';'
        return s
    
    def get_nodeName(self):
        return self._node.name
    get_name = get_nodeName
    
    def get_nodeValue(self):
        # This must traverse all of the node's children, and return a
        # string containing their values
        s = ""
        for child in self._node.children:
            if n.type == TEXT_NODE:
                s = s + n.value
            else:
                # Must be an EntityReference
                s = s + '&' + n.name + ';'
        return s
    get_value = get_nodeValue
    
    def set_nodeValue(self, value):
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        t = _nodeData(TEXT_NODE)
        t.name = "#text"
        t.value = value
        self._node.value = None
        self._node.children[0:] = [ t ]
        self._node.specified = 1
    set_value = set_nodeValue
    
    def get_specified(self):
        return self._node.specified

    def get_parentNode(self): return None
    def get_previousSibling(self): return None
    def get_nextSibling(self): return None
    
class Element(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE, COMMENT_NODE,
                      TEXT_NODE, CDATA_SECTION_NODE, ENTITY_REFERENCE_NODE]
    
    def __init__(self, node, parent = None, document = None):
        Node.__init__(self, node, parent, document)
        
    def __repr__(self):
        return "<Element '%s'>" % (self._node.name)

    def toxml(self):
        s = "<" + self._node.name
        for attr, attrnode in self._node.attributes.items():
            s = s + " %s='" % (attr,)
            for value in attrnode.children:
                print value.__dict__
                if value.type == TEXT_NODE:
                    s = s + escape(value.value) 
                else:
                    n = NODE_CLASS[ value.type ] (value, None, self._document)
                    s = s + value.toxml()
            s = s + "'"
            
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
        "Retrieve an attribute value by name."

        if self._node.attributes.has_key(name):
            n = self._node.attributes[name]
            assert n.type == ATTRIBUTE_NODE
            n = Attr(n, None, self._document)
            return n.toxml()
        else:
            return ""
    
    def setAttribute(self, name, value):
        """Adds a new attribute. If an attribute with that name is
        already present in the element, its value is changed to be
        that of the value parameter. This value is a simple string."""
        
        if isinstance(value, Node):
            raise ValueError, "setAttribute() method expects a string value"
        t = _nodeData(TEXT_NODE)
        t.name = "#text"
        t.value = value
        a = _nodeData(ATTRIBUTE_NODE)
        a.name = name
        a.children.append( t )
        self._node.attributes[name] = a

    def removeAttribute(self, name):
        "Removes an attribute by name."

        if self._node.attributes.has_key(name):
            del self._node.attributes[name]

    def getAttributeNode(self, name):
        "Retrieves an Attr node by name."
        
        if not self._node.attributes.has_key( name ):
            return None
        d = self._node.attributes[name]
        assert d.type == ATTRIBUTE_NODE
        return Attr(d, None, self._document)

    def setAttributeNode(self, newAttr):
        """Adds a new attribute. If an attribute with that name is
        already present in the element, it is replaced by the new
        one."""
        
        if not isinstance(newAttr, Attr):
            raise ValueError, "setAttributeNode() requires an Attr node as argument"
        name = newAttr._node.name
        if self._node.attributes.has_key( name ):
            attr = self._node.attributes[ name ]
            assert attr.type == ATTRIBUTE_NODE
            retval = Attr(attr, None, self._document )
        else: retval = None

        self._node.attributes[ name ] = newAttr._node
        return retval

    def removeAttributeNode(self, oldAttr):
        "Removes the specified attribute."
        # XXX this needs to know about DTDs to restore a default value
        name = oldAttr._node.name
        if self._node.attributes.has_key( name ):
            retval = Attr(self._node.attributes[name], None,
                          self._document )
            del self._node.attributes[ name ]
            return retval
        else: return None

    def getElementsByTagName(self, tagname):
        """Returns a NodeList of all descendant elements with a given
        tag name, in the order in which they would be encountered in
        a preorder traversal of the Element tree."""

        L = []
        for child in self._node.children:
            if child.type == ELEMENT:
                d = Element(child, self, self._document)
                if tagname == '*' or child.name == tagname:
                    L.append(d)
                L = L + d.getElementsByTagName(tagname)
        return NodeList(L)

    def normalize(self):
        """Puts all Text nodes in the full depth of the sub-tree
        underneath this Element into a "normal" form where only
        markup (e.g., tags, comments, processing instructions, CDATA
        sections, and entity references) separates Text nodes, i.e.,
        there are no adjacent Text nodes."""

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
    childNodeTypes = []
    # Methods

    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Text node %s>' % (repr(s),)
        
    def splitText(self, offset):
        """Breaks this Text node into two Text nodes at the specified
        offset, keeping both in the tree as siblings. This node then
        only contains all the content up to the offset point. And a
        new Text node, which is inserted as the next sibling of this
        node, contains all the content at and after the offset point."""
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
    childNodeTypes = []
    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Comment node %s>' % (repr(s),)
    
    def toxml(self):
        return '<-- %s -->' % self._node.value

class CDATASection(Text):
    """Represents CDATA sections, which are blocks of text that would
    otherwise be regarded as markup."""
    childNodeTypes = []
    
    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<CDATASection node %s>' % (repr(s),)

    def toxml(self):
        return self._node.value

class DocumentType(Node):
    readonly = 1    # This is a read-only class
    childNodeTypes = []
    
    # Attributes
    def get_name(self):
        return self._node.name

    def get_entities(self):
        d = NamedNodeMap()
        for entity, value in self._node.entities:
            pass # XXX

    def get_notations(self):
        pass # XXX

    def toxml(self):
        return '<!DOCTYPE %s>\n' % (self._node.name,)
        
class Notation(Node):
    readonly = 1    # This is a read-only class
    childNodeTypes = []
    
    # Attributes
    def get_publicId(self):
        return self._node.publicId
        
    def get_systemId(self):
        return self._node.systemId
        
class Entity(Node):
    readonly = 1    # This is a read-only class
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE, COMMENT_NODE,
                      TEXT_NODE, CDATA_SECTION_NODE, ENTITY_REFERENCE_NODE]
    
    def get_publicId(self):
        return self._node.publicId

    def get_systemId(self):
        return self._node.systemId

    def get_notationName(self):
        return self._node.notationName

class EntityReference(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                      COMMENT_NODE, TEXT_NODE, CDATA_SECTION_NODE,
                      ENTITY_REFERENCE_NODE]

    def toxml(self):
        return '&' + self._node.name + ';'
    
class ProcessingInstruction(Node):
    childNodeTypes = []
    
    def toxml(self):
        return "<? " + self._node.name + ' ' +self._node.target + "?>"

    def get_target(self):
        return self._node.name

    def get_data(self):
        return self._node.target

    def set_data(self, data):
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.target = data


class Document(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                      COMMENT_NODE, DOCUMENT_TYPE_NODE]
    
    def __init__(self, node, parent = None, document = None):
        Node.__init__(self, node, parent = None, document = None)
        self.documentType = None
        self.DOMImplementation = __import__(__name__)
        
    def toxml(self):
        s = '<?xml version="1.0"?>\n'
        if self.documentType:
            s = s + self.documentType
        if len(self._node.children):
            n = self._node.children[0]
            n =  NODE_CLASS[ n.type ] (n, self, self)
            s = s + n.toxml()
        return s

    def createElement(self, tagName, **kwdict):
        "Return a new Element object."

        d = _nodeData(ELEMENT_NODE)
        d.name = tagName
        d.value = None
        d.attributes = NamedNodeMap()
        elem = Element(d, None, self)
        for name, value in kwdict.items():
            elem.setAttribute(name, value)
        return elem

    def createDocumentFragment(self):
        "Return a new DocumentFragment object."
        
        d = _nodeData(DOCUMENT_FRAGMENT_NODE)
        d.name = "#document-fragment"
        return DocumentFragment(d, None, self)

    def createTextNode(self, data):
        "Return a new Text object."
        d = _nodeData(TEXT_NODE)
        d.name = "#text"
        d.value = data
        return Text(d, None, self)
    createText = createTextNode
    
    def createComment(self, data):
        "Return a new Comment object."
        d = _nodeData(COMMENT_NODE)
        d.name = "#comment"
        d.value = data
        return Comment(d, None, self)

    def createCDATAsection(self, data):
        "Return a new CDATASection object."
        d = _nodeData(CDATA_SECTION_NODE)
        d.name = "#cdata-section"
        d.value = data
        return CDATASection(d, None, self)

    def createProcessingInstruction(self, target, data):
        "Return a new ProcessingInstruction object."
        d = _nodeData(PROCESSING_INSTRUCTION_NODE)
        d.name = target
        d.value = data
        return ProcessingInstruction(d, None, self)
        
    def createAttribute(self, name):
        "Return a new Attribute object."
        d = _nodeData(ATTRIBUTE_NODE)
        d.name = name
        d.value = ""
        return Attribute(d, None, self)

    def createEntityReference(self, name):
        "Return a new EntityRefernce object."
        d = _nodeData(ENTITY_REFERENCE_NODE)
        d.name = name
        d.value = None
        return EntityReference(d, None, self)

    def getElementsByTagName(self, tagname):
        """Returns a NodeList of all the Elements with a given tag name
        in the order in which they would be encountered in a preorder
        traversal of the Document tree."""
        
        elem = self.get_documentElement()
        if elem == None: return []
        L = []
        if tagname == '*' or tagname == elem._node.name:
            L.append( elem )
        return L + elem.getElementsByTagName(tagname)

    # Extended methods for creating entity and notation nodes
    def createNotation(self, name, publicId, systemId):
        "Return a new Notation object."
        d = _nodeData(NOTATION_NODE)
        d.name = name
        d.value = None
        d.publicId, d.systemId = publicId, systemId
        return Notation(d, None, self)

    def createEntity(self, name, publicId, systemId, notationName = None):
        "Return a new Entity object."
        d = _nodeData(ENTITY_NODE)
        d.name = name
        d.value = None
        d.publicId, d.systemId = publicId, systemId
        d.notationName = notationName
        return Entity(d, None, self)

    # Attributes
    def get_doctype(self):
        return self.documentType
    def get_implementation(self):
        return self.DOMImplementation

    def get_documentElement(self):
        """Return the root element of the Document object, or None
        if there is no root element."""
        
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self, self)
                else:
                    raise HierarchyRequestException, \
                          "Too many Element children of Document" 
        return doc
    
    def get_ownerDocument(self):
        """Return the Document object associated with this node. This is also
        the Document object used to create new nodes. When this node
        is a Document this is null."""
        return None
    
    # Override the Node mutation methods in order to check that
    # there's at most a single Element child, and to update
    # self.documentElement.

    def insertBefore(self, newChild, refChild):
        """Inserts the node newChild before the existing child node
        refChild. If refChild is null, insert newChild at the end of
        the list of children.
        
        If newChild is a DocumentFragment object, all of its children
        are inserted, in the same order, before refChild. If the
        newChild is already in the tree, it is first removed."""
        
        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)
        self._checkChild(newChild, self)

        if newChild._document != self:
            raise WrongDocumentException("newChild %s created from a "
                                         "different document" % (repr(newChild),) )

        # If newChild is already in the tree, remove it
        if newChild.parentNode != None:
            newChild.parentNode.removeChild( newChild )

        if refChild == None:
            self._node.children.append( newChild._node )
            newChild.parentNode = self
            return newChild

        L = self._node.children ; n = refChild._node
        for i in range(len(L)):
            if L[i] == n:
                L[i:i] = [newChild._node]
                newChild.parentNode = self
                return newChild
        raise NotFoundException("refChild not a child in insertBefore()")

    def replaceChild(self, newChild, oldChild):
        """Replaces the child node oldChild with newChild in the list of
        children, and returns the oldChild node. If the newChild is
        already in the tree, it is first removed."""

        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)
        self._checkChild(newChild, self)
        if newChild._document != self:
            raise WrongDocumentException("newChild %s created from a "
                                         "different document" % (repr(newChild),) )

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
    
class DocumentFragment(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                      COMMENT_NODE, TEXT_NODE, CDATA_SECTION_NODE,
                      ENTITY_REFERENCE_NODE]
    
    def toxml(self):
        s = ""
        for child in self._node.children:
            n = NODE_CLASS[ child.type ] (child, self, self._document)
            s = s + n.toxml()
        return s
    
# Dictionary mapping types to the corresponding class object

NODE_CLASS = {
ELEMENT_NODE                : Element,
## ATTRIBUTE_NODE              : Attr, 
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

# vim:ts=2:ai
