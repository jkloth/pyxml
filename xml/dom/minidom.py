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

from xml.dom import EMPTY_NAMESPACE, EMPTY_PREFIX
from xml.dom.minicompat import *
from xml.dom.xmlbuilder import DOMImplementationLS, DocumentLS

_TupleType = type(())


class Node(xml.dom.Node, GetattrMagic):
    _makeParentNodes = 1
    namespaceURI = None # this is non-null only for elements and attributes
    parentNode = None
    ownerDocument = None
    nextSibling = None
    previousSibling = None

    prefix = EMPTY_PREFIX # non-null only for NS elements and attributes

    def __nonzero__(self):
        return True

    def toxml(self, encoding = None):
        return self.toprettyxml("", "", encoding)

    def toprettyxml(self, indent="\t", newl="\n", encoding = None):
        # indent = the indentation string to prepend, per level
        # newl = the newline string to append
        writer = _get_StringIO()
        if encoding is not None:
            import codecs
            # Can't use codecs.getwriter to preserve 2.0 compatibility
            writer = codecs.lookup(encoding)[3](writer)
        if self.nodeType == Node.DOCUMENT_NODE:
            # Can pass encoding only to document, to put it into XML header
            self.writexml(writer, "", indent, newl, encoding)
        else:
            self.writexml(writer, "", indent, newl)
        return writer.getvalue()

    def hasChildNodes(self):
        if self.childNodes:
            return True
        else:
            return False

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
        clone = CloneNode(self,deep,self.ownerDocument or self)
        return clone

    def isSupported(self, feature, version):
        return self.ownerDocument.implementation.hasFeature(feature, version)

    # Node interfaces from Level 3 (WD 9 April 2002)

    def isSameNode(self, other):
        return self is other

    def getInterface(self, feature):
        if self.isSupported(feature, None):
            return self
        else:
            return None

    def _get_localName(self):
        #Overridden in Element and Attr where localName can be Non-Null
        return None

    # The "user data" functions use a dictionary that is only present
    # if some user data has been set, so be careful not to assume it
    # exists.

    def getUserData(self, key):
        try:
            return self._user_data[key][0]
        except (AttributeError, KeyError):
            return None

    def setUserData(self, key, data, handler):
        old = None
        try:
            d = self._user_data
        except AttributeError:
            d = {}
            self._user_data = d
        if d.has_key(key):
            old = d[key][0]
        if data is None:
            # ignore handlers passed for None
            handler = None
            if old is not None:
                del d[key]
        else:
            d[key] = (data, handler)
        return old

    def _call_user_data_handler(self, operation, src, dst):
        if hasattr(self, "_user_data"):
            for key, (data, handler) in self._user_data.items():
                if handler is not None:
                    handler.handle(operation, key, data, src, dst)

    # minidom-specific API:

    def unlink(self):
        self.parentNode = self.ownerDocument = None
        if self.childNodes:
            for child in self.childNodes:
                child.unlink()
            self.childNodes = NodeList()
        self.previousSibling = None
        self.nextSibling = None

defproperty(Node, "firstChild", doc="First child node, or None.")
defproperty(Node, "lastChild",  doc="Last child node, or None.")
defproperty(Node, "localName", doc="Namespace-local name of this attribute.")


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
    specified = 0
    
    def __init__(self, qName, namespaceURI=EMPTY_NAMESPACE, localName=None,
                 prefix=None):
        # skip setattr for performance
        d = self.__dict__
        d["nodeName"] = d["name"] = qName
        d["namespaceURI"] = namespaceURI
        d["prefix"] = prefix
        d['childNodes'] = NodeList()

        #Add the single child node that represents the value of the attr
        d['childNodes'].append(Text())

        # nodeValue and value are set elsewhere

    def _get_localName(self):
        return self.nodeName.split(":", 1)[-1]

    def __setattr__(self, name, value):
        d = self.__dict__
        if name in ("value", "nodeValue"):
            d["value"] = d["nodeValue"] = value
            d["childNodes"][0].data = value
        elif name in ("name", "nodeName"):
            d["name"] = d["nodeName"] = value
        else:
            d[name] = value


class NamedNodeMap(NewStyle, GetattrMagic):
    """The attribute list is a transient interface to the underlying
    dictionaries.  Mutations here will change the underlying element's
    dictionary.

    Ordering is imposed artificially and does not reflect the order of
    attributes as found in an input document.
    """

    __slots__ = ('_attrs', '_attrsNS', '_ownerElement')

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
        if isinstance(attname_or_tuple, _TupleType):
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
        # Restore this since the node is still useful and otherwise
        # unlinked
        node.ownerDocument = self.ownerDocument

    removeAttributeNodeNS = removeAttributeNode

    def hasAttribute(self, name):
        return self._attrs.has_key(name)

    def hasAttributeNS(self, namespaceURI, localName):
        return self._attrsNS.has_key((namespaceURI, localName))

    def getElementsByTagName(self, name):
        return _getElementsByTagNameHelper(self, name, NodeList())

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _getElementsByTagNameNSHelper(self, namespaceURI, localName,
                                             NodeList())

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
            return True
        else:
            return False

defproperty(Element, "attributes",
            doc="NamedNodeMap of attributes on the element.")


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
        return False

    def insertBefore(self, newChild, refChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")

    def removeChild(self, oldChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")

    def replaceChild(self, newChild, oldChild):
        raise xml.dom.HierarchyRequestErr(
            self.nodeName + " nodes do not have children")


class ProcessingInstruction(Childless, Node):
    nodeType = Node.PROCESSING_INSTRUCTION_NODE

    def __init__(self, target, data):
        self.target = self.nodeName = target
        self.data = self.nodeValue = data

    def __setattr__(self, name, value):
        if name == "data" or name == "nodeValue":
            self.__dict__['data'] = self.__dict__['nodeValue'] = value
        elif name == "target" or name == "nodeName":
            self.__dict__['target'] = self.__dict__['nodeName'] = value
        else:
            self.__dict__[name] = value

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
            self.__dict__['data'] = self.__dict__['nodeValue'] = value
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

    # DOM Level 3 (WD 9 April 2002)

    def _get_wholeText(self):
        L = [self.data]
        n = self.previousSibling
        while n is not None:
            if n.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                L.insert(0, n.data)
                n = n.previousSibling
            else:
                break
        n = self.nextSibling
        while n is not None:
            if n.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                L.append(n.data)
                n = n.nextSibling
            else:
                break
        return ''.join(L)

    def replaceWholeText(self, content):
        # XXX This needs to be seriously changed if minidom ever
        # supports EntityReference nodes.
        parent = self.parentNode
        n = self.previousSibling
        while n is not None:
            if n.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                next = n.previousSibling
                parent.removeChild(n)
                n = next
            else:
                break
        n = self.nextSibling
        if not content:
            parent.removeChild(self)
        while n is not None:
            if n.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                next = n.nextSibling
                parent.removeChild(n)
                n = next
            else:
                break
        if content:
            d = self.__dict__
            d['data'] = content
            d['nodeValue'] = content
            return self
        else:
            return None


defproperty(Text, "wholeText",
            doc="The text of all logically-adjacent text nodes.")

class Comment(Childless, CharacterData):
    nodeType = Node.COMMENT_NODE
    nodeName = "#comment"

    def __init__(self, data):
        self.data = self.nodeValue = data

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("%s<!--%s-->%s" % (indent,self.data,newl))


class CDATASection(Text):
    # Make sure we don't add an instance __dict__ if we don't already
    # have one, at least when that's possible:
    __slots__ = ()

    nodeType = Node.CDATA_SECTION_NODE
    nodeName = "#cdata-section"

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("<![CDATA[%s]]>" % self.data)



def _nssplit(qualifiedName):
    fields = qualifiedName.split(':', 1)
    if len(fields) == 2:
        return fields
    elif len(fields) == 1:
        return (None, fields[0])

class ReadOnlySequentialNamedNodeMap(NewStyle, GetattrMagic):
    __slots__ = '_seq',

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

    def __getitem__(self, name_or_tuple):
        if isinstance(name_or_tuple, _TupleType):
            return self.getNamedItemNS(*name_or_tuple)
        else:
            return self.getNamedItem(name_or_tuple)

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
        self.nodeName = self.name

class Identified:
    """Mix-in class that supports the publicId and systemId attributes."""

    def _identified_mixin_init(self, publicId, systemId):
        self.publicId = publicId
        self.systemId = systemId

    def _get_publicId(self):
        return self.publicId

    def _get_systemId(self):
        return self.systemId

class Entity(Identified, Node):
    nodeType = Node.ENTITY_NODE
    nodeValue = None

    actualEncoding = None
    encoding = None
    version = None

    def __init__(self, name, publicId, systemId, notation):
        self.nodeName = name
        self.notationName = notation
        self._identified_mixin_init(publicId, systemId)

class Notation(Identified, Childless, Node):
    nodeType = Node.NOTATION_NODE
    nodeValue = None

    def __init__(self, name, publicId, systemId):
        self.nodeName = name
        self._identified_mixin_init(publicId, systemId)


class DOMImplementation(DOMImplementationLS):
    _features = [("core", "1.0"),
                 ("core", "2.0"),
                 ("core", "3.0"),
                 ("core", None),
                 ("xml", "1.0"),
                 ("xml", "2.0"),
                 ("xml", "3.0"),
                 ("xml", None),
                 ("ls-load", "3.0"),
                 ("ls-load", None),
                 ]

    def hasFeature(self, feature, version):
        if version == "":
            version = None
        return (feature.lower(), version) in self._features

    def createDocument(self, namespaceURI, qualifiedName, doctype):
        if doctype and doctype.parentNode is not None:
            raise xml.dom.WrongDocumentErr(
                "doctype object owned by another DOM tree")
        doc = self._createDocument()

        add_root_element = not (namespaceURI is None
                                and qualifiedName is None
                                and doctype is None)

        #if doctype is None:
        #    doctype = self.createDocumentType(qualifiedName, None, None)
        
        if not qualifiedName and add_root_element:
            # The spec is unclear what to raise here; SyntaxErr
            # would be the other obvious candidate. Since Xerces raises
            # InvalidCharacterErr, and since SyntaxErr is not listed
            # for createDocument, that seems to be the better choice.
            # XXX: need to check for illegal characters here and in
            # createElement.

            #DOM Level III clears this up when talking about the return value
            #of this function.  If namespaceURI, qName and DocType are
            #Null the document is returned without a document element
            #Otherwise if doctype or namespaceURI are not None
            #Then we go back to the above problem
            raise xml.dom.InvalidCharacterErr("Element with no name")

        if add_root_element:
            prefix, localname = _nssplit(qualifiedName)
            if prefix == "xml" \
               and namespaceURI != "http://www.w3.org/XML/1998/namespace":
                raise xml.dom.NamespaceErr("illegal use of 'xml' prefix")
            if prefix and not namespaceURI:
                raise xml.dom.NamespaceErr(
                    "illegal use of prefix without namespaces")
            element = doc.createElementNS(namespaceURI, qualifiedName)
            doc.appendChild(element)

        if doctype:
            doctype.parentNode = doctype.ownerDocument = doc

        doc.doctype = doctype
        doc.implementation = self
        return doc

    def createDocumentType(self, qualifiedName, publicId, systemId):
        doctype = DocumentType(qualifiedName)
        doctype.publicId = publicId
        doctype.systemId = systemId
        return doctype

    # DOM Level 3 (WD 9 April 2002)

    def getInterface(self, feature):
        if self.hasFeature(feature, None):
            return self
        else:
            return None

    # internal
    def _createDocument(self):
        return Document()

class Document(Node, DocumentLS):
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

    # Document attributes from Level 3 (WD 9 April 2002)

    actualEncoding = None
    encoding = None
    standalone = None
    version = None
    strictErrorChecking = False
    errorHandler = None
    documentURI = None

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
        d.ownerDocument = self
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
        c = CDATASection()
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
        return _getElementsByTagNameHelper(self, name, NodeList())

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _getElementsByTagNameNSHelper(self, namespaceURI, localName,
                                             NodeList())

    def isSupported(self, feature, version):
        return self.implementation.hasFeature(feature, version)

    def importNode(self,node,deep):
        return CloneNode(node,deep,self)

    def writexml(self, writer, indent="", addindent="", newl="",
                 encoding = None):
        if encoding is None:
            writer.write('<?xml version="1.0" ?>\n')
        else:
            writer.write('<?xml version="1.0" encoding="%s"?>\n' % encoding)
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)

    # DOM Level 3 (WD 9 April 2002)

    def renameNode(self, n, namespaceURI, name):
        if n.ownerDocument is not self:
            raise xml.dom.WrongDocumentErr(
                "cannot rename nodes from other documents;\n"
                "expected %s,\nfound %s" % (self, n.ownerDocument))
        if n.nodeType not in (Node.ELEMENT_NODE, Node.ATTRIBUTE_NODE):
            raise xml.dom.NotSupportedErr(
                "renameNode() only applies to element and attribute nodes")
        if namespaceURI != EMPTY_NAMESPACE:
            if ':' in name:
                prefix, localName = name.split(':', 1)
                if (  prefix == "xmlns"
                      and namespaceURI != xml.dom.XMLNS_NAMESPACE):
                    raise xml.dom.NamespaceErr(
                        "illegal use of 'xmlns' prefix")
            else:
                if (  name == "xmlns"
                      and namespaceURI != xml.dom.XMLNS_NAMESPACE
                      and n.nodeType == Node.ATTRIBUTE_NODE):
                    raise xml.dom.NamespaceErr(
                        "illegal use of the 'xmlns' attribute")
                prefix = None
                localName = name
        else:
            prefix = None
            localName = None
        if n.nodeType == Node.ATTRIBUTE_NODE:
            element = n.ownerElement
            if element is not None:
                element.removeAttributeNode(n)
        else:
            element = None
        # avoid __setattr__
        d = n.__dict__
        d['prefix'] = prefix
        d['localName'] = localName
        d['namespaceURI'] = namespaceURI
        d['nodeName'] = name
        if n.nodeType == Node.ELEMENT_NODE:
            d['tagName'] = name
        else:
            # attribute node
            d['name'] = name
            if element is not None:
                element.setAttributeNode(n)
        # XXX not clear whether we should call the user data handlers
        # for the NODE_RENAMED event since we're re-using the existing
        # node.  This is a whole in the spec.
        return n

defproperty(Document, "documentElement",
            doc="Top-level element of this document.")




def CloneNode(node,deep,newOwnerDocument):
    """
    Clone a node and give it the new owner document.
    Called by Node.cloneNode and Document.importNode
    """
    if node.nodeType == Node.ELEMENT_NODE:
        clone = newOwnerDocument.createElementNS(node.namespaceURI,
                                                 node.nodeName)
        for attr in node.attributes.values():
            clone.setAttributeNS(attr.namespaceURI,attr.nodeName,attr.value)

        if deep:
            for child in node.childNodes:
                c = CloneNode(child,deep,newOwnerDocument)
                clone.appendChild(c)

    elif node.nodeType == Node.TEXT_NODE:
        clone = newOwnerDocument.createTextNode(node.data)
    elif node.nodeType == Node.CDATA_SECTION_NODE:
        clone = newOwnerDocument.createCDATASection(node.data)
    elif node.nodeType == PROCESSING_INSTRUCTION_NODE:
        clone = newOwnerDocument.createProcessingInstruction(node.target,
                                                             node.data)
    elif node.nodeType == COMMENT_NODE:
        clone = newOwnerDocument.createComment(node.data)
    else:
        raise Exception("Cannot clone node %s" % repr(node))

    if hasattr(node,'_call_user_data_handler'):
        node._call_user_data_handler(xml.dom.UserDataHandler.NODE_CLONED,
                                     node, clone)
    return clone


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
