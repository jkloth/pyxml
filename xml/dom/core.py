"""
core.py: 'light' implementation of the Document Object Model (core) level 1.

Reference: http://www.w3.org/TR/1998/REC-DOM-Level-1-19981001/

Deviations from the Level 1 spec:
   * The list returned by .getElementsByTagName() isn't live

Useful classes in this module are Node (abstract) and its
(concrete) subclasses -- Document, Element, Text, Comment,
ProcessingInstruction -- all of which should be instantiated though
the relevant create{Element,TextNode,Comment,...}() methods on a
Document object.  

Typical usage:

from xml.dom.core import *

doc = createDocument()                  
html = doc.createElement('html')
html.setAttribute('attr', 'value')
head = doc.createElement('head')
title = doc.createElement('title')

text = doc.createTextNode("Title goes here")
title.appendChild(text)
head.appendChild(title)                
html.appendChild(head)
doc.appendChild (html)                 

print doc.toxml()
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
INVALID_STATE_ERR           = 11
SYNTAX_ERR                  = 12
INVALID_MODIFICATION_ERR    = 13
NAMESPACE_ERR               = 14
INVALID_ACCESS_ERR          = 15

# Exception classes

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
class InUseAttributeException(DOMException):
    code = INUSE_ATTRIBUTE_ERR
class InvalidStateException(DOMException):
    code = INVALID_STATE_ERR
class SyntaxException(DOMException):
    code = SYNTAX_ERR
class InvalidModificationException(DOMException):
    code = INVALID_MODIFICATION_ERR 
class NamespaceException(DOMException):
    code = NAMESPACE_ERR
class InvalidAccessException(DOMException):
    code = INVALID_ACCESS_ERR
    
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
        if version in ['1.0', '2.0']: return 1
        return 0

def createDocumentType(qualifiedName, publicId, systemId, internalSubset):
    d = _nodeData(DOCUMENT_TYPE_NODE)
    d.name = qualifiedName
    d.value = d.attributes = None
    d.publicId = publicId
    d.systemId = systemId
    d.internalSubset = internalSubset
    d = DocumentType(d, None)
    return d
    
def createDocument(namespaceURI = None,
                   qualifiedName = "",
                   doctype = None
                   ):
    "Create a fresh Document object and return it"
    d = _nodeData(DOCUMENT_NODE)
    d.name = '#document'
    d.value = d.attributes = None

    # Check doctype value, if provided.
    if doctype is not None:
        if not isinstance( DocumentType, doctype ):
            raise ValueError, ('doctype argument must be a DocumentType node: '
                               + repr(doctype) )

        if doctype.get_ownerDocument() is not None:
            raise ValueError, ('doctype argument already owned by Document '
                               + repr(doctype.get_ownerDocument() ) )
            
        # Change ownerDocument of doctype
        doctype._document = d
        
    d = Document(d, None)
    return d


import UserList, UserDict

class NodeList(UserList.UserList):
    """An ordered collection of nodes, equivalent to a Python list.  The only
    difference is that an .item() method and a .length attribute are added.
    """

    def __init__(self, list, document):
        # We don't make a copy of the list; instead, we take a reference
        # to it, so that the NodeList is always up-to-date.
        self.data = list
        self._document = document
	
    def __repr__(self):
        s = '<NodeList [ '
        for i in range(len(self.data)):
            n = self.data[i] 
            n = NODE_CLASS[ n.type ](n, self._document)
            s = s + repr(n) + ','
        return s[:-1] + ']>'
    
    def __getitem__(self, i):
        n = self.data[i]
        return NODE_CLASS[ n.type ](n, self._document)

    def __setitem__(self, i, item):
        raise TypeError, "NodeList instances don't support item assignment"
    def __delitem__(self, i, item):
        raise TypeError, "NodeList instances don't support item deletion"

    def __getslice__(self, i, j):
        userlist = NodeList([], self._document)
        userlist.data[:] = self.data[i:j]
        return userlist

    def __setslice__(self, i, j, list):
        raise TypeError, "NodeList instances don't support slice assignment"
    def __delslice__(self, i, j):
        raise TypeError, "NodeList instances don't support slice deletion"

    def __add__(self, list):
        if type(list) == type(self.data):
            return self.__class__(self.data + list, self._document)
        else:
            return self.__class__(self.data + list.data, 
                                  self._document)
    def __radd__(self, list):
        if type(list) == type(self.data):
            return self.__class__(list + self.data, self._document)
        else:
            return self.__class__(list.data + self.data, 
                                              self._document)
    def __mul__(self, n):
        return self.__class__(self.data*n, self._document)
    __rmul__ = __mul__

    def append(self, item): 
        raise TypeError, "NodeList instances don't support .append()"
    def insert(self, i, item):
        raise TypeError, "NodeList instances don't support .insert()"
    def pop(self, i=-1): 
        raise TypeError, "NodeList instances don't support .pop()"
    def remove(self, item): 
        raise TypeError, "NodeList instances don't support .remove()"
    def count(self, item): return self.data.count(item._node)
    def index(self, item): return self.data.index(item._node)
    def reverse(self): 
        raise TypeError, "NodeList instances don't support .reverse()"
    def sort(self, *args): 
        raise TypeError, "NodeList instances don't support .sort()"

    # Aliases required by the DOM Recommendation
    item = __getitem__
    get_length = UserList.UserList.__len__


class NamedNodeMap(UserDict.UserDict):
    """Used to represent a collection of nodes that can be accessed by name.
    Equivalent to a Python dictionary, with various aliases added such as
    getNamedItem and removeNamedItem.
    """

    def __init__(self, dict, document):
        self.data = dict
        self._document = document

    def __getitem__(self, key):
        n = self.data[key]
        assert n.type == ATTRIBUTE_NODE
        n = NODE_CLASS[ n.type ](n, self._document )
        return n

    def __setitem__(self, key, item):
        if item.type != ATTRIBUTE_NODE:
            raise TypeError, "NamedNodeMap instances only accept Attr nodes as values"
        self.data[key] = item._node

    def items(self):
        L = []
        for key, value in self.data.items():
            L.append( (key,
                       NODE_CLASS[ value.type ](value, self._document )
                       )
                     )
        return L
    
    def values(self):
        L = self.data.values()
        for i in range(len(L)):
            n = L[i]
            L[i] = NODE_CLASS[ n.type ](n, self._document )
        return L

    def update(self, other):
        if not isinstance(other, NamedNodeMap):
             raise TypeError, "Can only use .update() with another NamedNodeMap"
        for k, v in other.data.items():
            self.data[k] = v

    def get(self, key, default=None):
        if self.data.has_key(key):
            return self[key]
        else:
            return default

    # Additional methods specified in the DOM Recommendation
    def item(self, index):
        n = self.data.values()[ index ]
        return NODE_CLASS[ n.type ](n, self._document )

    getNamedItem = __getitem__
    removeNamedItem = UserDict.UserDict.__delitem__
    get_length = UserDict.UserDict.__len__

    def setNamedItem(self, arg):
        key = arg.nodeName
        self[key] = arg

    
    
class _nodeData:
    """Class used for storing the data for a single node.  Instances of
    this class should never be returned to users of the DOM implementation."""
    ##Node_counter = 0
    def __init__(self, type):
        self.type = type
        self.children = []
        self.name = self.value = self.attributes = None
        ##_nodeData.Node_counter = _nodeData.Node_counter + 1

        if self.type == DOCUMENT_NODE:
            # Dictionary mapping id(_nodeData instance) to parent
            # _nodeData instance 
            self._parent_relation = {}

    def __getinitargs__(self):
        return (self.type,)
    
##    def __del__(self):
##        _nodeData.Node_counter = _nodeData.Node_counter -1

    def __repr__(self):
        return ("<_nodeData: type=%i name=%s value=%s att=%s>" %
                (self.type, self.name, self.value, self.attributes) )

class Node:
    """Base class for tree nodes in DOM model."""

    readonly = 0
    ##Node_counter = 0

    def __init__(self, node, document = None):
	d = self.__dict__
	d['_node'] = node
	d['nodeType'] = node.type
	d['nodeName'] = node.name

	if not isinstance(node, _nodeData):
	    raise ValueError, ( "node parameter isn't a _nodeData instance: "
	                        + repr(node) )
	
	if not (isinstance(document, _nodeData) or (document is None) ):
	    raise ValueError, ( "document parameter isn't a _nodeData instance: "
	                        + repr(document) )
	    

        if document is not None: d['_document'] = document
        else: d['_document'] = None
##        Node.Node_counter = Node.Node_counter + 1

##    def __del__(self):
##        Node.Node_counter = Node.Node_counter - 1

    # For the sake of pickling, don't pickle the Node instance, since it's
    # just a proxy, and doesn't have any interesting info in itself.
    def __getinitargs__(self):
        return self._node, self._document

    # The following two methods implement handling of properties; references
    # to attributes such as .parentNode are redirected into calls to 
    # get_parentNode or set_parentNode.
    def __getattr__(self, key):
	# Check if it's a class attribute
	if hasattr(self.__class__, key):
	    return getattr(self.__class__, key)

	# Otherwise, look for a get_X attribute on the class, and call it
	if key[0:1] != '_':
	    k2 = 'get_' + key
	    if hasattr(self.__class__, k2):
		meth = getattr(self.__class__, k2)
		return meth(self)
	
	raise AttributeError, repr(key)

    def __setattr__(self, key, value):
        if (not self.__dict__.has_key(key) and 
	    hasattr(self.__class__, 'set_'+key) ):
            func = getattr(self.__class__, 'set_'+key)
            func( self, value )
        self.__dict__[key] = value

    def __cmp__(self, other):
        if isinstance(other, Node):
            # Compare the underlying _nodeData instances.
            return cmp(self._node, other._node)
        else:
            # If the other object isn't a Node, then we'll do an
            # arbitrary comparison that will at least be consistent.
            return cmp(self._node, other)        

    # Methods to get/set the DOM-specified attributes of a node: name, value,
    # attributes.

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

    def get_childNodes(self):
        """Return a NodeList containing all children of this node. If there
        are no children, this is a NodeList containing no nodes."""
        return NodeList(self._node.children, self._document )

    def get_firstChild(self):
        """Return the first child of this node. If there is no such node, this
        returns None."""

        if self._node.children:
            n = self._node.children[0]
            return NODE_CLASS[ n.type ] (n, self._document )
        else:
            return None

    def get_lastChild(self):
        """Return the last child of this node. If there is no such node, this
        returns None."""
        if self._node.children:
            n = self._node.children[-1]
            return NODE_CLASS[ n.type ] (n, self._document)
        else:
            return None

    def get_previousSibling(self):
        """Return the node immediately preceding this node. If there is no such
        node, this returns None."""

        if self.get_parentNode() is None: return None
        i = self._index()
        if i <= 0:
            return None
        else:
            n = self.get_parentNode()._node.children[i - 1]
            return NODE_CLASS[ n.type ] (n, self._document)

    def get_nextSibling(self):
        """Return the node immediately following this node. If there is no such
        node, this returns None."""
        if self.get_parentNode() is None: return None
        L = self.get_parentNode()._node.children
        i = self._index()
        if i == -1 or i == len(L) - 1:
            return None
        else:
            n = L[i+1]
            return NODE_CLASS[ n.type ] (n, self._document)

    def get_attributes(self):
        return None
    
    def get_ownerDocument(self):
        """The Document object associated with this node. This is also
        the Document object used to create new nodes. When this node
        is a Document or a DocumentType unattached to a document,
        this is None."""
        if self._document is None: return None
        return Document(self._document, None)

    # Methods

    def insertBefore(self, newChild, refChild):
        """Inserts the node newChild before the existing child node
        refChild. If refChild is None, insert newChild at the end of
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

        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            nodelist = newChild._node.children
        else:
            nodelist = [ newChild._node ]

        for node in nodelist:
            if node.type not in self.childNodeTypes:
                node = NODE_CLASS[ node.type ] (node, self._document)
                raise HierarchyRequestException, \
                      "%s cannot be child of %s" % (repr(node), repr(self) )

        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            newChild._node.children = []

        if refChild is None:
            # If newChild is already in the tree, remove it
            if newChild.get_parentNode() != None:
                newChild.get_parentNode().removeChild( newChild )

            for node in nodelist:
                self._node.children.append( node )
                self._set_parentdict( id(node), self._node)
                            
            return newChild

        L = self._node.children ; n = refChild._node
        for i in range(len(L)):
            if L[i] == n:
                # If newChild is already in the tree, remove it
                if newChild.get_parentNode() != None:
                    newChild.get_parentNode().removeChild( newChild )

                L[i:i] = nodelist
                if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
                    newChild._node.children = []
                else:
                    for node in nodelist:
                        self._set_parentdict(id(node), self._node)
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
                    node = NODE_CLASS[ node.type ] (node, self._document)
                    raise HierarchyRequestException, \
                          "%s cannot be child of %s" % (repr(node), repr(self) )

        o = oldChild._node ; L = self._node.children
        for i in range(len(L)):
            if L[i] == o:
                # If newChild is already in the tree, remove it
                if newChild.get_parentNode() != None:
                    newChild.get_parentNode().removeChild( newChild )

                if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
                    L[i:i+1] = newChild._node.children
                    for child in newChild._node.children:
                        self._set_parentdict(id(child), self._node)
                    newChild._node.children = []
                else:
                    L[i] = newChild._node
                    self._set_parentdict(id(newChild._node), self._node)
                self._del_parentdict( id(oldChild._node) )
                return oldChild

        raise NotFoundException("oldChild not a child of this node")

    def removeChild(self, oldChild):
        """Removes the child node indicated by oldChild from the list of
        children, and returns it."""

        if self.readonly:
            raise NoModificationAllowedException, "Read-only node "+repr(self)

        try:
            self._node.children.remove(oldChild._node)
        except ValueError:
            raise NotFoundException("oldChild is not a child of this node")

        self._del_parentdict( id(oldChild._node) )
        return oldChild

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
        (parentNode returns None.)."""
        
        import copy
        d = _nodeData( self._node.type )
        for key, value in self._node.__dict__.items():
            if key == 'children' or key[0:2] == '__':
                continue
            else:
                setattr(d, key, copy.deepcopy(value) )

        if self._node.type == DOCUMENT_NODE: document = d
        else: document = self._document
        node = NODE_CLASS[ d.type ] ( d, document )
        if deep:
            d.children = copy.deepcopy(self._node.children)
        return node

    def dump(self, stream = sys.stdout, indent = 0):
        """Dump the XML subtree from this node, in a form that lets you
        see the structure of the tree."""
        stream.write( indent*' ' + repr(self) + '\n')
        for c in self._node.children:
            c = NODE_CLASS[ c.type ](c, self._document)
            c.dump(stream, indent + 1)

    def get_parentNode(self):
        # If self._document is None, this must be the Document node,
        # which doesn't have a parent.
        if self._document is None: return None

        # Check if the id() of this node is a key in the dictionary;
        # if so, the corresponding value is the _nodeData instance 
        # that's the parent node.  
        pr = self._get_parentdict()
        parent = pr.get( id(self._node), None)
        if parent is not None: 
            return NODE_CLASS[ parent.type ] (parent, self._document)
        else:
            # The children of the Document node can't be added to the
            # parentdict, because that would lead to a cycle; the
            # Document _nodeData instance would contain a dictionary which
            # contained the Document node as a value.  Therefore, if
            # there's no key for id(self._node), we have to check 
            # the children of the Document element before concluding 
            # that this node is parentless.
        
            if self._node in self._document.children:
                return Document(self._document, None)
            return None

    # Private methods        

    def _get_parentdict(self):
        if self._node.type == DOCUMENT_NODE:
            return self._node._parent_relation
        else:
            return self._document._parent_relation

    def _set_parentdict(self, key, node):
        d = self._get_parentdict()
        # Don't insert the document node, in order to avoid a cycle
        if node == self._document: 
            # If this node is already represented in the dictionary,
            # we have to delete it.
            if d.has_key( key ): del d[key]
            return
        d[key] = node

    def _del_parentdict(self, key):
        d = self._get_parentdict()
        if d.has_key(key): del d[key]

    def _index(self):
        "Return the index of this child in its parent's child list"
        parent = self.get_parentNode()
        if parent:
            return parent._node.children.index(self._node)
        else:
            return -1

    def _checkChild(self, child, parent):
        "Raise HierarchyRequestException if the child can't be added"

        cn = child._node ; p=self
        while p is not None:
            if p._node is cn: 
                raise HierarchyRequestException, \
                      "%s is an ancestor of %s" % (repr(child), repr(parent) )
            p = p.get_parentNode()

        
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
    set_nodeValue = set_data
    
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
        d = _nodeData(TEXT_NODE)
        d.name = "#text"
        d.value = value
        return Text(d, self._document)
    
class Attr(Node):
    
    childNodeTypes = [TEXT_NODE, ENTITY_REFERENCE_NODE]
        
    def __init__(self, node, document = None):
        Node.__init__(self, node, document)

    def __repr__(self):
        return '<Attribute node %s>' % (repr(self._node.name),)

    def toxml(self):
        L = []
        append = L.append
        for c in self._node.children:
            if c.type == TEXT_NODE:
                append(c.value)
            elif c.type == ENTITY_REFERENCE_NODE:
                append("&")
                append(c.name)
                append(";")
        return string.join(L, "")
    
    def get_nodeName(self):
        return self._node.name
    get_name = get_nodeName
    
    def get_nodeValue(self):
        # This must traverse all of the node's children, and return a
        # string containing their values
        s = ""
        for n in self._node.children:
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
    
    def __init__(self, node, document = None):
        Node.__init__(self, node, document)
        self.__dict__['nodeName'] = node.name
        self.__dict__['ns_prefix'] = {}         # Dictionary for namespaces
        
    def __repr__(self):
        return "<Element '%s'>" % (self._node.name)

    def toxml(self):
        L = ["<", self._node.name]
        append = L.append
        for attr, attrnode in self._node.attributes.items():
            append(" %s='" % (attr,))
            for value in attrnode.children:
                if value.type == TEXT_NODE:
                    append(escape(value.value) )
                else:
                    n = NODE_CLASS[ value.type ] (value, self._document)
                    append(value.toxml())
            append("'")
            
        if len(self._node.children) == 0:
            append(" />")
            return string.join(L, "")
        append(">")
        for child in self._node.children:
            n = NODE_CLASS[ child.type ] (child, self._document)
            append(n.toxml())
        append("</")
        append(self._node.name)
        append(">")
        return string.join(L, "")

    # Attributes
    
    def get_tagName(self):
        return self._node.name

    # Methods

    def get_attributes(self):
        "Return a NamedNodeMap containing all the attributes of this element."
        d = NamedNodeMap( self._node.attributes, self._document )
        return d
        
    def getAttribute(self, name):
        "Retrieve an attribute value by name."

        if self._node.attributes.has_key(name):
            n = self._node.attributes[name]
	    if n.type != ATTRIBUTE_NODE:
		raise ValueError, ("Not an attribute node in .attributes: " 
	                           + repr(n) )
            n = Attr(n, self._document)
            return n.toxml()
        else:
            return ""
    
    def setAttribute(self, name, value):
        """Adds a new attribute. If an attribute with that name is
        already present in the element, its value is changed to be
        that of the value parameter. This value is a simple string."""
        
        if isinstance(value, Node):
            raise TypeError, "setAttribute() method expects a string value"
        t = _nodeData(TEXT_NODE)
        t.name = "#text"
        t.value = value
        a = _nodeData(ATTRIBUTE_NODE)
        a.name = name
        a.children.append( t )
        self._node.attributes[name] = a

        # Update the namespace prefixes, if required
        if name[0:5] == 'xmlns':
            prefix = name[6:]
            uri = value
            self.ns_prefix[prefix] = uri

    def removeAttribute(self, name):
        "Removes an attribute by name."

        if self._node.attributes.has_key(name):
            del self._node.attributes[name]

        # Update the namespace prefixes, if required
        if name[0:5] == 'xmlns':
            prefix = name[6:]
            assert self.ns_prefix.has_key( prefix )
            del self.ns_prefix[prefix]

    def getAttributeNode(self, name):
        "Retrieves an Attr node by name."
        
        if not self._node.attributes.has_key( name ):
            return None
        d = self._node.attributes[name]
        assert d.type == ATTRIBUTE_NODE
        return Attr(d, self._document)

    def setAttributeNode(self, newAttr):
        """Adds a new attribute. If an attribute with that name is
        already present in the element, it is replaced by the new
        one."""
        
        if not isinstance(newAttr, Attr):
            raise TypeError, "setAttributeNode() requires an Attr node as argument"
        name = newAttr._node.name
        if self._node.attributes.has_key( name ):
            attr = self._node.attributes[ name ]
            assert attr.type == ATTRIBUTE_NODE
            retval = Attr(attr, self._document )
        else: retval = None

        self._node.attributes[ name ] = newAttr._node

        # Update the namespace prefixes, if required
        if name[0:5] == 'xmlns':
            prefix = name[6:]
            uri = newAttr.get_nodeValue()
            self.ns_prefix[prefix] = uri

        return retval

    def removeAttributeNode(self, oldAttr):
        "Removes the specified attribute."
        # XXX this needs to know about DTDs to restore a default value
        name = oldAttr._node.name

        # Update the namespace prefixes, if required
        if name[0:5] == 'xmlns':
            prefix = name[6:]
            assert self.ns_prefix.has_key( prefix )
            del self.ns_prefix[prefix]

        if self._node.attributes.has_key( name ):
            retval = Attr(self._node.attributes[name], self._document )
            del self._node.attributes[ name ]
            return retval
        else: return None

    def getElementsByTagName(self, tagname):
        """Returns a NodeList of all descendant elements with a given
        tag name, in the order in which they would be encountered in
        a preorder traversal of the Element tree."""

        nodes = [] ; parents = []
        for child in self._node.children:
            if child.type == ELEMENT:
                d = Element(child, self._document)
                if tagname == '*' or child.name == tagname:
                    nodes.append( child )
                    parents.append( self )
                nl = d.getElementsByTagName(tagname)
                nodes = nodes + nl.data
        return NodeList(nodes, self._document )

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
                # Two text nodes together, so merge them.
                # Any Text instances proxying the deleted
                # _nodeData instance will find themselves
                # disconnected from the tree; this is not a bug, I think.
                L[i-1].value = L[i-1].value + L[i].value
                self._del_parentdict( id(L[i]) ) # Mark the node as parentless
                del L[i:i+1]
                
        for i in range(len(L)):
            if L[i].type == ELEMENT_NODE:
                n = NODE_CLASS[ L[i].type ] (L[i], self._document)
                n.normalize()
    
class Text(CharacterData):
    childNodeTypes = []
    nodeName = "#text"
    # Methods

    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Text node %s>' % (repr(s),)

    def get_nodeName(self):
        return "#text"
        
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
        n1 = Text(n1, self._document)
        n2 = Text(n2, self._document)
        parent = self.get_parentNode()

        # Insert n1 and n2, and delete this node
        parent.insertBefore(n1, self)
        parent.replaceChild(n2, self)
    
class Comment(CharacterData):
    childNodeTypes = []
    nodeName = "#comment"

    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<Comment node %s>' % (repr(s),)
    
    def get_nodeName(self):
        return "#comment"

    def toxml(self):
        return '<!--%s-->' % self._node.value

class CDATASection(Text):
    """Represents CDATA sections, which are blocks of text that would
    otherwise be regarded as markup."""
    childNodeTypes = []
    nodeName = "#cdata-section"
    
    def __repr__(self):
        if len(self._node.value)<20: s=self._node.value
        else: s=self._node.value[:17] + '...'
        return '<CDATASection node %s>' % (repr(s),)

    def get_nodeName(self):
        return "#cdata-section"

    def toxml(self):
        return '<![CDATA[' + self._node.value + ']]>'

class DocumentType(Node):
    readonly = 1    # This is a read-only class
    childNodeTypes = []

    # Attributes
    def get_name(self):
        return self._node.name

    def get_entities(self):
        d = NamedNodeMap(self._node.entities, self._document)
        # XXX untested
        #for entity_name, value in self._node.entities:
            #d[entitity_name] = value
        return d
    
    def get_notations(self):
        # XXX untested
        d = NamedNodeMap(self._node.notations, self._document)
        pass # XXX
        return d

    def get_publicId(self):
        return self._node.publicId
        
    def get_systemId(self):
        return self._node.systemId

    def get_internalSubset(self):
        return self._node.internalSubset

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

    def toxml(self):
        if self._node.systemId is None:
            return '<!NOTATION %s PUBLIC %s>' % (self._node.name, self._node.publicId)
        elif self._node.publicId is None:
            return '<!NOTATION %s SYSTEM %s>' % (self._node.name, self._node.systemId)
        else:
            return '<!NOTATION %s PUBLIC %s %s>' % (self._node.name,
                                                    self._node.publicId,
                                                    self._node.systemId)
        
        
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
        return '&%s;' % self._node.name
    
class ProcessingInstruction(Node):
    childNodeTypes = []
    
    def toxml(self):
        return "<?%s %s?>" % (self._node.name, self._node.value)

    def __repr__(self):
        return '<Processing instruction ?%s %s?>' \
               % (self._node.name, self._node.value)

    def get_target(self):
        return self._node.name

    def get_data(self):
        return self._node.value

    def set_data(self, data):
        if self.readonly:
            raise NoModificationAllowedException("Read-only object")
        self._node.value = data


class Document(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                      COMMENT_NODE, DOCUMENT_TYPE_NODE]
    nodeName = "#document"

    def __init__(self, node, document = None):
        Node.__init__(self, node, None)
	d = self.__dict__
	d['documentType'] = None
	d['_document'] = node

    def get_nodeName(self):
        return "#document"

    def toxml(self):
        L = ['<?xml version="1.0"?>\n']
        if self.documentType:
            L.append(self.documentType.toxml())
        for n in self._node.children:
            n = NODE_CLASS[ n.type ] (n, self._document)
            L.append(n.toxml())
        return string.join(L, "")

    def __repr__(self):
        return '<DOM Document; root=%s >' % (repr(self.get_documentElement()),)
    
    def createElement(self, tagName, dict={}, **kwdict):
        "Return a new Element object."

        d = _nodeData(ELEMENT_NODE)
        d.name = tagName
        d.value = None
        d.attributes = {}
        elem = Element(d, self._node)
        kwdict.update( dict )
        for name, value in kwdict.items():
            elem.setAttribute(name, value)
        return elem

    def createDocumentFragment(self):
        "Return a new DocumentFragment object."
        
        d = _nodeData(DOCUMENT_FRAGMENT_NODE)
        d.name = "#document-fragment"
        return DocumentFragment(d, self._node)

    def createTextNode(self, data):
        "Return a new Text object."
        d = _nodeData(TEXT_NODE)
        d.name = "#text"
        d.value = data
        return Text(d, self._node)
    createText = createTextNode
    
    def createComment(self, data):
        "Return a new Comment object."
        d = _nodeData(COMMENT_NODE)
        d.name = "#comment"
        d.value = data
        return Comment(d, self._node)

    def createCDATAsection(self, data):
        "Return a new CDATASection object."
        d = _nodeData(CDATA_SECTION_NODE)
        d.name = "#cdata-section"
        d.value = data
        return CDATASection(d, self._node)

    def createProcessingInstruction(self, target, data):
        "Return a new ProcessingInstruction object."
        d = _nodeData(PROCESSING_INSTRUCTION_NODE)
        d.name = target
        d.value = data
        return ProcessingInstruction(d, self._node)
        
    def createAttribute(self, name):
        "Return a new Attribute object."
        d = _nodeData(ATTRIBUTE_NODE)
        d.name = name
        d.value = ""
        return Attr(d, self._node)

    def createEntityReference(self, name):
        "Return a new EntityRefernce object."
        d = _nodeData(ENTITY_REFERENCE_NODE)
        d.name = name
        d.value = None
        return EntityReference(d, self._node)

    # Extended methods for creating entity and notation nodes
    def createNotation(self, name, publicId = None, systemId = None):
        "Return a new Notation object."
        d = _nodeData(NOTATION_NODE)
        d.name = name
        d.value = None
        d.publicId, d.systemId = publicId, systemId
        return Notation(d, self._node)

    def createEntity(self, name, publicId, systemId, notationName = None):
        "Return a new Entity object."
        d = _nodeData(ENTITY_NODE)
        d.name = name
        d.value = None
        d.publicId, d.systemId = publicId, systemId
        d.notationName = notationName
        return Entity(d, self._node)

    def getElementsByTagName(self, tagname):
        """Returns a NodeList of all the Elements with a given tag name
        in the order in which they would be encountered in a preorder
        traversal of the Document tree."""
        
        # This function could be optimized by doing it in a private function
        # and dealing with _nodeData instances directly.  This would save 
        # the overhead of creating Node instances only to take their ._node
        # attribute and append it to a list.  Haven't bothered to code that
        # yet...

        elem = self.get_documentElement()
        if elem is None: return NodeList([], self._node)
        nodes = [] 
        if tagname == '*' or tagname == elem._node.name:
            nodes.append( elem._node ) 
        nl = elem.getElementsByTagName(tagname)
        nodes = nodes + nl.data
        return NodeList( nodes, self._node )
        
    # Attributes
    def get_doctype(self):
        return self.documentType
    def get_implementation(self):
	return __import__(__name__)

    def get_childNodes(self):
        return NodeList(self._node.children, self._node)

    def get_documentElement(self):
        """Return the root element of the Document object, or None
        if there is no root element."""
        
        doc = None
        for elem in self._node.children:
            if elem.type == ELEMENT_NODE:
                if doc is None:
                    doc = Element(elem, self._node)
                else:
                    raise HierarchyRequestException, \
                          "Too many Element children of Document" 
        return doc
    
    def get_ownerDocument(self):
        """Return the Document object associated with this node. This is also
        the Document object used to create new nodes. When this node
        is a Document this is None."""
        return None

    # Override the Node mutation methods in order to check that
    # there's at most a single Element child, and to update
    # self.documentElement.  
        
    def insertBefore(self, newChild, refChild):
        """Inserts the node newChild before the existing child node
        refChild. If refChild is None, insert newChild at the end of
        the list of children.
        
        If newChild is a DocumentFragment object, all of its children
        are inserted, in the same order, before refChild. If the
        newChild is already in the tree, it is first removed."""

        # Check that this operation wouldn't result in the Document node
        # having more than one children that are Element nodes.
        # This is done by counting the number of unique element nodes
        # in both the Document's children, and the nodes to be inserted.
        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            nodelist = newChild._node.children
        else:
            nodelist = [newChild._node]

        d = {}                         # Dictionary for counting
        for c in nodelist:
            if c.type == ELEMENT_NODE: d[ id(c) ] = None
        for c in self._node.children:
            if c.type == ELEMENT_NODE: d[ id(c) ] = None
        if len(d) > 1:
            raise HierarchyRequestException, \
               "insertBefore() would result in more than one root document element"
         
        # Call the original version of insertBefore
        Node.insertBefore(self, newChild, refChild)
        
    def replaceChild(self, newChild, oldChild):
        """Replaces the child node oldChild with newChild in the list of
        children, and returns the oldChild node. If the newChild is
        already in the tree, it is first removed."""

        # Check that this operation wouldn't result in the Document node
        # having more than one children that are Element nodes.
        # This is as in insertBefore, with one change; if the old node being
        # replaced is an element, it shouldn't be counted.
        if newChild._node.type == DOCUMENT_FRAGMENT_NODE:
            nodelist = newChild._node.children
        else:
            nodelist = [newChild._node]

        d = {}                         # Dictionary for counting
        for c in nodelist:
            if c.type == ELEMENT_NODE: d[ id(c) ] = None
        for c in self._node.children:
            if c.type == ELEMENT_NODE: d[ id(c) ] = None

        # For a correct count, we should not count the oldChild node, in case
        # it's a
        ocn = oldChild._node
        if ocn.type == ELEMENT_NODE and d.has_key( id(ocn) ):
            del d[ id(ocn) ]

        if len(d) > 1:
            raise HierarchyRequestException, \
              "replaceChild() would result in more than one root document element" 

        Node.replaceChild(self, newChild, oldChild)

class DocumentFragment(Node):
    childNodeTypes = [ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                      COMMENT_NODE, TEXT_NODE, CDATA_SECTION_NODE,
                      ENTITY_REFERENCE_NODE]
    nodeName = "#document-fragment"

    def get_parentNode(self): 
        # DocumentFragments can never be part of a tree themselves; when added,
        # their children are added instead.
        return None    

    def get_nodeName(self):
        return "#document-fragment"

    def toxml(self):
        L = []
        for child in self._node.children:
            n = NODE_CLASS[ child.type ] (child, self._document)
            L.append(n.toxml())
        return string.join(L, "")
    
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

# vim:ts=2:ai

