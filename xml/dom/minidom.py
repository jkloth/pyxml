"""\
minidom.py -- a lightweight DOM implementation.

parse("foo.xml")

parseString("<foo><bar/></foo>")

Todo:
=====
 * convenience methods for getting elements and text.
 * more testing
 * bring some of the writer and linearizer code into conformance with this
        interface
 * SAX 2 namespaces
"""

import xml.dom

from xml.dom import EMPTY_NAMESPACE
from xml.dom.minicompat import *


class Node(xml.dom.Node, GetattrMagic):
    _makeParentNodes = 1
    namespaceURI = None # this is non-null only for elements and attributes
    parentNode = None
    ownerDocument = None
    nextSibling = None
    previousSibling = None

    def __nonzero__(self):
        return 1

    def toxml(self):
        writer = _get_StringIO()
        self.writexml(writer)
        return writer.getvalue()

    def toprettyxml(self, indent="\t", newl="\n"):
        # indent = the indentation string to prepend, per level
        # newl = the newline string to append
        writer = _get_StringIO()
        self.writexml(writer, "", indent, newl)
        return writer.getvalue()

    def hasChildNodes(self):
        if self.childNodes:
            return 1
        else:
            return 0

    def _get_firstChild(self):
        if self.childNodes:
            return self.childNodes[0]

    def _get_lastChild(self):
        if self.childNodes:
            return self.childNodes[-1]

    def insertBefore(self, newChild, refChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(newChild.childNodes):
                self.insertBefore(c, refChild)
            ### The DOM does not clearly specify what to return in this case
            return newChild
        if newChild.nodeType not in self.childNodeTypes:
            raise xml.dom.HierarchyRequestErr(
                "%s cannot be child of %s" % (repr(newChild), repr(self)))
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        if refChild is None:
            self.appendChild(newChild)
        else:
            index = self.childNodes.index(refChild)
            self.childNodes.insert(index, newChild)
            newChild.nextSibling = refChild
            refChild.previousSibling = newChild
            if index:
                node = self.childNodes[index-1]
                node.nextSibling = newChild
                newChild.previousSibling = node
            else:
                newChild.previousSibling = None
            if self._makeParentNodes:
                newChild.parentNode = self
        return newChild

    def appendChild(self, node):
        if node.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(node.childNodes):
                self.appendChild(c)
            ### The DOM does not clearly specify what to return in this case
            return node
        if node.nodeType not in self.childNodeTypes:
            raise xml.dom.HierarchyRequestErr(
                "%s cannot be child of %s" % (repr(node), repr(self)))
        if node.parentNode is not None:
            node.parentNode.removeChild(node)
        _appendChild(self, node)
        node.nextSibling = None
        return node

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            refChild = oldChild.nextSibling
            self.removeChild(oldChild)
            return self.insertBefore(newChild, refChild)
        if newChild.nodeType not in self.childNodeTypes:
            raise xml.dom.HierarchyRequestErr(
                "%s cannot be child of %s" % (repr(newChild), repr(self)))
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        if newChild is oldChild:
            return
        index = self.childNodes.index(oldChild)
        self.childNodes[index] = newChild
        if self._makeParentNodes:
            newChild.parentNode = self
            oldChild.parentNode = None
        newChild.nextSibling = oldChild.nextSibling
        newChild.previousSibling = oldChild.previousSibling
        oldChild.nextSibling = None
        oldChild.previousSibling = None
        if newChild.previousSibling:
            newChild.previousSibling.nextSibling = newChild
        if newChild.nextSibling:
            newChild.nextSibling.previousSibling = newChild
        return oldChild

    def removeChild(self, oldChild):
        self.childNodes.remove(oldChild)
        if oldChild.nextSibling is not None:
            oldChild.nextSibling.previousSibling = oldChild.previousSibling
        if oldChild.previousSibling is not None:
            oldChild.previousSibling.nextSibling = oldChild.nextSibling
        oldChild.nextSibling = oldChild.previousSibling = None

        if self._makeParentNodes:
            oldChild.parentNode = None
        return oldChild

    def normalize(self):
        L = []
        for child in self.childNodes:
            if child.nodeType == Node.TEXT_NODE:
                data = child.data
                if data and L and L[-1].nodeType == child.nodeType:
                    # collapse text node
                    node = L[-1]
                    node.data = node.nodeValue = node.data + child.data
                    node.nextSibling = child.nextSibling
                    child.unlink()
                elif data:
                    if L:
                        L[-1].nextSibling = child
                        child.previousSibling = L[-1]
                    else:
                        child.previousSibling = None
                    L.append(child)
                else:
                    # empty text node; discard
                    child.unlink()
            else:
                if L:
                    L[-1].nextSibling = child
                    child.previousSibling = L[-1]
                else:
                    child.previousSibling = None
                L.append(child)
                if child.nodeType == Node.ELEMENT_NODE:
                    child.normalize()
        self.childNodes[:] = L

    def cloneNode(self, deep):
        import new
        clone = new.instance(self.__class__, self.__dict__.copy())
        if self._makeParentNodes:
            clone.parentNode = None
        clone.childNodes = NodeList()
        if deep:
            for child in self.childNodes:
                clone.appendChild(child.cloneNode(1))
        return clone

    # DOM Level 3 (Working Draft 2001-Jan-26)

    def isSameNode(self, other):
        return self is other

    # minidom-specific API:

    def unlink(self):
        self.parentNode = self.ownerDocument = None
        for child in self.childNodes:
            child.unlink()
        self.childNodes = None
        self.previousSibling = None
        self.nextSibling = None

defproperty(Node, "firstChild", doc="First child node, or None.")
defproperty(Node, "lastChild",  doc="Last child node, or None.")


def _appendChild(self, node):
    # fast path with less checks; usable by DOM builders if careful
    childNodes = self.childNodes
    if childNodes:
        last = childNodes[-1]
        node.previousSibling = last
        last.nextSibling = node
    childNodes.append(node)
    if self._makeParentNodes:
        node.parentNode = self

def _write_data(writer, data):
    "Writes datachars to writer."
    data = data.replace("&", "&amp;").replace("<", "&lt;")
    data = data.replace("\"", "&quot;").replace(">", "&gt;")
    writer.write(data)

def _getElementsByTagNameHelper(parent, name, rc):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and \
            (name == "*" or node.tagName == name):
            rc.append(node)
        _getElementsByTagNameHelper(node, name, rc)
    return rc

def _getElementsByTagNameNSHelper(parent, nsURI, localName, rc):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            if ((localName == "*" or node.localName == localName) and
                (nsURI == "*" or node.namespaceURI == nsURI)):
                rc.append(node)
            _getElementsByTagNameNSHelper(node, nsURI, localName, rc)
    return rc

class DocumentFragment(Node):
    nodeType = Node.DOCUMENT_FRAGMENT_NODE
    nodeName = "#document-fragment"
    nodeValue = None
    attributes = None
    parentNode = None
    childNodeTypes = (Node.ELEMENT_NODE,
                      Node.TEXT_NODE,
                      Node.CDATA_SECTION_NODE,
                      Node.ENTITY_REFERENCE_NODE,
                      Node.PROCESSING_INSTRUCTION_NODE,
                      Node.COMMENT_NODE,
                      Node.NOTATION_NODE)

    def __init__(self):
        self.childNodes = NodeList()


class Attr(Node):
    nodeType = Node.ATTRIBUTE_NODE
    attributes = None
    ownerElement = None
    childNodeTypes = (Node.TEXT_NODE, Node.ENTITY_REFERENCE_NODE)

    def __init__(self, qName, namespaceURI=EMPTY_NAMESPACE, localName=None,
                 prefix=None):
        # skip setattr for performance
        d = self.__dict__
        d["nodeName"] = d["name"] = qName
        d["namespaceURI"] = namespaceURI
        d["prefix"] = prefix
        d['childNodes'] = NodeList()
        # nodeValue and value are set elsewhere

    def _get_localName(self):
        return self.nodeName.split(":", 1)[-1]

    def __setattr__(self, name, value):
        d = self.__dict__
        if name in ("value", "nodeValue"):
            d["value"] = d["nodeValue"] = value
        elif name in ("name", "nodeName"):
            d["name"] = d["nodeName"] = value
        else:
            d[name] = value

    def cloneNode(self, deep):
        clone = Node.cloneNode(self, deep)
        if clone.__dict__.has_key("ownerElement"):
            del clone.ownerElement
        return clone

defproperty(Attr, "localName", doc="Namespace-local name of this attribute.")


class NamedNodeMap(GetattrMagic):
    """The attribute list is a transient interface to the underlying
    dictionaries.  Mutations here will change the underlying element's
    dictionary.

    Ordering is imposed artificially and does not reflect the order of
    attributes as found in an input document.
    """

    def __init__(self, attrs, attrsNS, ownerElement):
        self._attrs = attrs
        self._attrsNS = attrsNS
        self._ownerElement = ownerElement

    def _get_length(self):
        return len(self._attrs)

    def item(self, index):
        try:
            return self[self._attrs.keys()[index]]
        except IndexError:
            return None

    def items(self):
        L = []
        for node in self._attrs.values():
            L.append((node.nodeName, node.value))
        return L

    def itemsNS(self):
        L = []
        for node in self._attrs.values():
            L.append(((node.namespaceURI, node.localName), node.value))
        return L

    def keys(self):
        return self._attrs.keys()

    def keysNS(self):
        return self._attrsNS.keys()

    def values(self):
        return self._attrs.values()

    def get(self, name, value = None):
        return self._attrs.get(name, value)

    __len__ = _get_length

    def __cmp__(self, other):
        if self._attrs is getattr(other, "_attrs", None):
            return 0
        else:
            return cmp(id(self), id(other))

    #FIXME: is it appropriate to return .value?
    def __getitem__(self, attname_or_tuple):
        if isinstance(attname_or_tuple, TupleType):
            return self._attrsNS[attname_or_tuple]
        else:
            return self._attrs[attname_or_tuple]

    # same as set
    def __setitem__(self, attname, value):
        if isinstance(value, StringTypes):
            node = Attr(attname)
            node.value = value
            node.ownerDocument = self._ownerElement.ownerDocument
        else:
            if not isinstance(value, Attr):
                raise TypeError, "value must be a string or Attr object"
            node = value
        self.setNamedItem(node)

    def setNamedItem(self, node):
        if not isinstance(node, Attr):
            raise xml.dom.HierarchyRequestErr(
                "%s cannot be child of %s" % (repr(node), repr(self)))
        old = self._attrs.get(node.name)
        if old:
            old.unlink()
        self._attrs[node.name] = node
        self._attrsNS[(node.namespaceURI, node.localName)] = node
        node.ownerElement = self._ownerElement
        return old

    def setNamedItemNS(self, node):
        return self.setNamedItem(node)

    def __delitem__(self, attname_or_tuple):
        node = self[attname_or_tuple]
        node.unlink()
        del self._attrs[node.name]
        del self._attrsNS[(node.namespaceURI, node.localName)]
        self.length = len(self._attrs)

defproperty(NamedNodeMap, "length",
            doc="Number of nodes in the NamedNodeMap.")

AttributeList = NamedNodeMap


class Element(Node):
    nodeType = Node.ELEMENT_NODE
    nodeValue = None
    childNodeTypes = (Node.ELEMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE,
                      Node.COMMENT_NODE, Node.TEXT_NODE,
                      Node.CDATA_SECTION_NODE, Node.ENTITY_REFERENCE_NODE)

    def __init__(self, tagName, namespaceURI=EMPTY_NAMESPACE, prefix=None,
                 localName=None):
        self.tagName = self.nodeName = tagName
        self.prefix = prefix
        self.namespaceURI = namespaceURI
        self.childNodes = NodeList()

        self._attrs = {}   # attributes are double-indexed:
        self._attrsNS = {} #    tagName -> Attribute
                           #    URI,localName -> Attribute
                           # in the future: consider lazy generation
                           # of attribute objects this is too tricky
                           # for now because of headaches with
                           # namespaces.

    def _get_localName(self):
        return self.tagName.split(":", 1)[-1]

    def cloneNode(self, deep):
        clone = Node.cloneNode(self, deep)
        clone._attrs = {}
        clone._attrsNS = {}
        for attr in self._attrs.values():
            node = attr.cloneNode(1)
            clone._attrs[node.name] = node
            clone._attrsNS[(node.namespaceURI, node.localName)] = node
            node.ownerElement = clone
        return clone

    def unlink(self):
        for attr in self._attrs.values():
            attr.unlink()
        self._attrs = None
        self._attrsNS = None
        Node.unlink(self)

    def getAttribute(self, attname):
        try:
            return self._attrs[attname].value
        except KeyError:
            return ""

    def getAttributeNS(self, namespaceURI, localName):
        try:
            return self._attrsNS[(namespaceURI, localName)].value
        except KeyError:
            return ""

    def setAttribute(self, attname, value):
        attr = Attr(attname)
        # for performance
        d = attr.__dict__
        d["value"] = d["nodeValue"] = value
        d["ownerDocument"] = self.ownerDocument
        self.setAttributeNode(attr)

    def setAttributeNS(self, namespaceURI, qualifiedName, value):
        prefix, localname = _nssplit(qualifiedName)
        # for performance
        attr = Attr(qualifiedName, namespaceURI, localname, prefix)
        d = attr.__dict__
        d["value"] = d["nodeValue"] = value
        d["ownerDocument"] = self.ownerDocument
        self.setAttributeNode(attr)

    def getAttributeNode(self, attrname):
        return self._attrs.get(attrname)

    def getAttributeNodeNS(self, namespaceURI, localName):
        return self._attrsNS.get((namespaceURI, localName))

    def setAttributeNode(self, attr):
        if attr.ownerElement not in (None, self):
            raise xml.dom.InuseAttributeErr("attribute node already owned")
        old = self._attrs.get(attr.name, None)
        if old:
            old.unlink()
        _setAttributeNode(self, attr)

        if old is not attr:
            # It might have already been part of this node, in which case
            # it doesn't represent a change, and should not be returned.
            return old

    setAttributeNodeNS = setAttributeNode

    def removeAttribute(self, name):
        attr = self._attrs[name]
        self.removeAttributeNode(attr)

    def removeAttributeNS(self, namespaceURI, localName):
        attr = self._attrsNS[(namespaceURI, localName)]
        self.removeAttributeNode(attr)

    def removeAttributeNode(self, node):
        node.unlink()
        del self._attrs[node.name]
        del self._attrsNS[(node.namespaceURI, node.localName)]

    removeAttributeNodeNS = removeAttributeNode

    def hasAttribute(self, name):
        return self._attrs.has_key(name)

    def hasAttributeNS(self, namespaceURI, localName):
        return self._attrsNS.has_key((namespaceURI, localName))

    def getElementsByTagName(self, name):
        return _getElementsByTagNameHelper(self, name, [])

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _getElementsByTagNameNSHelper(self, namespaceURI, localName, [])

    def __repr__(self):
        return "<DOM Element: %s at %s>" % (self.tagName, id(self))

    def writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent+"<" + self.tagName)

        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            writer.write(">%s"%(newl))
            for node in self.childNodes:
                node.writexml(writer,indent+addindent,addindent,newl)
            writer.write("%s</%s>%s" % (indent,self.tagName,newl))
        else:
            writer.write("/>%s"%(newl))

    def _get_attributes(self):
        return NamedNodeMap(self._attrs, self._attrsNS, self)

    def hasAttributes(self):
        if self._attrs:
            return 1
        else:
            return 0

defproperty(Element, "attributes",
            doc="NamedNodeMap of attributes on the element.")
defproperty(Element, "localName",
            doc="Namespace-local name for this element.")


def _setAttributeNode(self, attr):
    self._attrs[attr.name] = attr
    self._attrsNS[(attr.namespaceURI, attr.localName)] = attr

    # This creates a circular reference, but Element.unlink()
    # breaks the cycle since the references to the attribute
    # dictionaries are tossed.
    attr.__dict__['ownerElement'] = self


class Childless:
    """Mixin that makes childless-ness easy to implement and avoids
    the complexity of the Node methods that deal with children.
    """

    attributes = None
    childNodes = EmptyNodeList()
    firstChild = None
    lastChild = None

    def _get_firstChild(self):
        return None

    def _get_lastChild(self):
        return None

    def appendChild(self, node):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes cannot have children")

    def hasChildNodes(self):
        return 0

    def insertBefore(self, newChild, refChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")

    def removeChild(self, oldChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")

    def replaceChild(self, newChild, oldChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")


class Comment(Childless, Node):
    nodeType = Node.COMMENT_NODE
    nodeName = "#comment"

    def __init__(self, data):
        self.data = self.nodeValue = data

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("%s<!--%s-->%s" % (indent,self.data,newl))


class ProcessingInstruction(Childless, Node):
    nodeType = Node.PROCESSING_INSTRUCTION_NODE

    def __init__(self, target, data):
        self.target = self.nodeName = target
        self.data = self.nodeValue = data

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("%s<?%s %s?>%s" % (indent,self.target, self.data, newl))


class CharacterData(Childless, Node):
    def _get_length(self):
        return len(self.data)

    def _get_data(self):
        return self.__dict__['data']
    def _set_data(self, data):
        self.__dict__['data'] = data

    _get_nodeValue = _get_data
    _set_nodeValue = _set_data

    def __setattr__(self, name, value):
        if name == "data" or name == "nodeValue":
            self.__dict__['data'] = value
        else:
            self.__dict__[name] = value

    def __repr__(self):
        data = self.data
        if len(data) > 10:
            dotdotdot = "..."
        else:
            dotdotdot = ""
        return "<DOM %s node \"%s%s\">" % (
            self.__class__.__name__, data[0:10], dotdotdot)

    def substringData(self, offset, count):
        if offset < 0:
            raise xml.dom.IndexSizeErr("offset cannot be negative")
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr("offset cannot be beyond end of data")
        if count < 0:
            raise xml.dom.IndexSizeErr("count cannot be negative")
        return self.data[offset:offset+count]

    def appendData(self, arg):
        self.data = self.data + arg

    def insertData(self, offset, arg):
        if offset < 0:
            raise xml.dom.IndexSizeErr("offset cannot be negative")
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr("offset cannot be beyond end of data")
        if arg:
            self.data = "%s%s%s" % (
                self.data[:offset], arg, self.data[offset:])

    def deleteData(self, offset, count):
        if offset < 0:
            raise xml.dom.IndexSizeErr("offset cannot be negative")
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr("offset cannot be beyond end of data")
        if count < 0:
            raise xml.dom.IndexSizeErr("count cannot be negative")
        if count:
            self.data = self.data[:offset] + self.data[offset+count:]

    def replaceData(self, offset, count, arg):
        if offset < 0:
            raise xml.dom.IndexSizeErr("offset cannot be negative")
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr("offset cannot be beyond end of data")
        if count < 0:
            raise xml.dom.IndexSizeErr("count cannot be negative")
        if count:
            self.data = "%s%s%s" % (
                self.data[:offset], arg, self.data[offset+count:])

defproperty(CharacterData, "length", doc="Length of the string data.")


class Text(CharacterData):
    # Make sure we don't add an instance __dict__ if we don't already
    # have one, at least when that's possible:
    __slots__ = ()

    nodeType = Node.TEXT_NODE
    nodeName = "#text"
    attributes = None

    def splitText(self, offset):
        if offset < 0 or offset > len(self.data):
            raise xml.dom.IndexSizeErr("illegal offset value")
        newText = self.__class__()
        newText.data = self.data[offset:]
        newText.ownerDocument = self.ownerDocument
        next = self.nextSibling
        if self.parentNode and self in self.parentNode.childNodes:
            if next is None:
                self.parentNode.appendChild(newText)
            else:
                self.parentNode.insertBefore(newText, next)
        self.data = self.data[:offset]
        return newText

    def writexml(self, writer, indent="", addindent="", newl=""):
        _write_data(writer, "%s%s%s"%(indent, self.data, newl))


class CDATASection(Text):
    # Make sure we don't add an instance __dict__ if we don't already
    # have one, at least when that's possible:
    __slots__ = ()

    nodeType = Node.CDATA_SECTION_NODE
    nodeName = "#cdata-section"

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("<![CDATA[%s]]>" % self.data)


class ReadOnlySequentialNamedNodeMap(GetattrMagic):
    def __init__(self, seq=()):
        # seq should be a list or tuple
        self._seq = seq

    def _get_length(self):
        return len(self._seq)

    def getNamedItem(self, name):
        for n in self._seq:
            if n.nodeName == name:
                return n

    def getNamedItemNS(self, namespaceURI, localName):
        for n in self._seq:
            if n.namespaceURI == namespaceURI and n.localName == localName:
                return n

    def item(self, index):
        if index < 0:
            return None
        try:
            return self._seq[index]
        except IndexError:
            return None

    def removeNamedItem(self, name):
        raise xml.dom.NoModificationAllowedErr(
            "NamedNodeMap instance is read-only")

    def removeNamedItemNS(self, namespaceURI, localName):
        raise xml.dom.NoModificationAllowedErr(
            "NamedNodeMap instance is read-only")

    def setNamedItem(self, node):
        raise xml.dom.NoModificationAllowedErr(
            "NamedNodeMap instance is read-only")

    def setNamedItemNS(self, node):
        raise xml.dom.NoModificationAllowedErr(
            "NamedNodeMap instance is read-only")

defproperty(ReadOnlySequentialNamedNodeMap, "length",
            doc="Number of entries in the NamedNodeMap.")


class DocumentType(Childless, Node):
    nodeType = Node.DOCUMENT_TYPE_NODE
    nodeValue = None
    name = None
    publicId = None
    systemId = None
    internalSubset = None

    def __init__(self, qualifiedName):
        self.entities = ReadOnlySequentialNamedNodeMap()
        self.notations = ReadOnlySequentialNamedNodeMap()
        if qualifiedName:
            prefix, localname = _nssplit(qualifiedName)
            self.name = localname


class DOMImplementation:
    def hasFeature(self, feature, version):
        if version not in ("1.0", "2.0"):
            return 0
        return feature.lower() == "core"

    def createDocument(self, namespaceURI, qualifiedName, doctype):
        if doctype and doctype.parentNode is not None:
            raise xml.dom.WrongDocumentErr(
                "doctype object owned by another DOM tree")
        doc = self._createDocument()
        if doctype is None:
            doctype = self.createDocumentType(qualifiedName, None, None)
        if not qualifiedName:
            # The spec is unclear what to raise here; SyntaxErr
            # would be the other obvious candidate. Since Xerces raises
            # InvalidCharacterErr, and since SyntaxErr is not listed
            # for createDocument, that seems to be the better choice.
            # XXX: need to check for illegal characters here and in
            # createElement.
            raise xml.dom.InvalidCharacterErr("Element with no name")
        prefix, localname = _nssplit(qualifiedName)
        if prefix == "xml" \
           and namespaceURI != "http://www.w3.org/XML/1998/namespace":
            raise xml.dom.NamespaceErr("illegal use of 'xml' prefix")
        if prefix and not namespaceURI:
            raise xml.dom.NamespaceErr(
                "illegal use of prefix without namespaces")
        element = doc.createElementNS(namespaceURI, qualifiedName)
        doc.appendChild(element)
        doctype.parentNode = doctype.ownerDocument = doc
        doc.doctype = doctype
        doc.implementation = self
        return doc

    def createDocumentType(self, qualifiedName, publicId, systemId):
        doctype = DocumentType(qualifiedName)
        doctype.publicId = publicId
        doctype.systemId = systemId
        return doctype

    # internal
    def _createDocument(self):
        return Document()

class Document(Node):
    nodeType = Node.DOCUMENT_NODE
    nodeName = "#document"
    nodeValue = None
    attributes = None
    doctype = None
    parentNode = None
    previousSibling = nextSibling = None

    implementation = DOMImplementation()
    childNodeTypes = (Node.ELEMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE,
                      Node.COMMENT_NODE, Node.DOCUMENT_TYPE_NODE)

    def __init__(self):
        self.childNodes = NodeList()

    def appendChild(self, node):
        if node.nodeType not in self.childNodeTypes:
            raise xml.dom.HierarchyRequestErr(
                "%s cannot be child of %s" % (repr(node), repr(self)))
        if node.parentNode is not None:
            node.parentNode.removeChild(node)

        if node.nodeType == Node.ELEMENT_NODE \
           and self._get_documentElement():
            raise xml.dom.HierarchyRequestErr(
                "two document elements disallowed")
        return Node.appendChild(self, node)

    def removeChild(self, oldChild):
        self.childNodes.remove(oldChild)
        oldChild.nextSibling = oldChild.previousSibling = None
        oldChild.parentNode = None
        if self.documentElement is oldChild:
            self.documentElement = None

        return oldChild

    def _get_documentElement(self):
        for node in self.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                return node

    def unlink(self):
        if self.doctype is not None:
            self.doctype.unlink()
            self.doctype = None
        Node.unlink(self)

    def createDocumentFragment(self):
        d = DocumentFragment()
        d.ownerDoc = self
        return d

    def createElement(self, tagName):
        e = Element(tagName)
        e.ownerDocument = self
        return e

    def createTextNode(self, data):
        if not isinstance(data, StringTypes):
            raise TypeError, "node contents must be a string"
        t = Text()
        t.data = data
        t.ownerDocument = self
        return t

    def createCDATASection(self, data):
        if not isinstance(data, StringTypes):
            raise TypeError, "node contents must be a string"
        c = CDATASection(data)
        c.data = data
        c.ownerDocument = self
        return c

    def createComment(self, data):
        c = Comment(data)
        c.ownerDocument = self
        return c

    def createProcessingInstruction(self, target, data):
        p = ProcessingInstruction(target, data)
        p.ownerDocument = self
        return p

    def createAttribute(self, qName):
        a = Attr(qName)
        a.ownerDocument = self
        a.value = ""
        return a

    def createElementNS(self, namespaceURI, qualifiedName):
        prefix, localName = _nssplit(qualifiedName)
        e = Element(qualifiedName, namespaceURI, prefix)
        e.ownerDocument = self
        return e

    def createAttributeNS(self, namespaceURI, qualifiedName):
        prefix, localName = _nssplit(qualifiedName)
        a = Attr(qualifiedName, namespaceURI, localName, prefix)
        a.ownerDocument = self
        a.value = ""
        return a

    def getElementsByTagName(self, name):
        return _getElementsByTagNameHelper(self, name, [])

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _getElementsByTagNameNSHelper(self, namespaceURI, localName, [])

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write('<?xml version="1.0" ?>\n')
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)

defproperty(Document, "documentElement",
            doc="Top-level element of this document.")


def _nssplit(qualifiedName):
    fields = qualifiedName.split(':', 1)
    if len(fields) == 2:
        return fields
    else:
        return (None, fields[0])


def _get_StringIO():
    # we can't use cStringIO since it doesn't support Unicode strings
    from StringIO import StringIO
    return StringIO()

def _doparse(func, args, kwargs):
    events = apply(func, args, kwargs)
    toktype, rootNode = events.getEvent()
    events.expandNode(rootNode)
    events.clear()
    return rootNode

def parse(*args, **kwargs):
    """Parse a file into a DOM by filename or file object."""
    from xml.dom import pulldom
    return _doparse(pulldom.parse, args, kwargs)

def parseString(*args, **kwargs):
    """Parse a file into a DOM from a string."""
    from xml.dom import pulldom
    return _doparse(pulldom.parseString, args, kwargs)

def getDOMImplementation():
    return Document.implementation
