"""Facility to use the Expat parser to load a minidom instance
from a string or file.

This avoids all the overhead of SAX and pulldom to gain performance.
"""

# Warning!
#
# This module is tightly bound to the implementation details of the
# minidom DOM and can't be used with other DOM implementations.  This
# is due, in part, to a lack of appropriate methods in the DOM (there is
# no way to create Entity and Notation nodes via the DOM Level 2
# interface), and for performance.  The later is the cause of some fairly
# cryptic code.
#
# Performance hacks:
#
#   -  .character_data_handler() has an extra case in which continuing
#      data is appended to an existing Text node; this can be a
#      speedup since pyexpat can break up character data into multiple
#      callbacks even though we set the buffer_text attribute on the
#      parser.  This also gives us the advantage that we don't need a
#      separate normalization pass.
#
#   -  Determining that a node exists is done using an identity comparison
#      with None rather than a truth test; this avoids searching for and
#      calling any methods on the node object if it exists.  (A rather
#      nice speedup is achieved this way as well!)

from xml.dom import xmlbuilder, minidom, Node
from xml.dom import EMPTY_NAMESPACE, XMLNS_NAMESPACE
from xml.parsers import expat
from xml.dom.minidom import _appendChild, _setAttributeNode
from xml.dom.NodeFilter import NodeFilter

TEXT_NODE = Node.TEXT_NODE
CDATA_SECTION_NODE = Node.CDATA_SECTION_NODE
DOCUMENT_NODE = Node.DOCUMENT_NODE

theDOMImplementation = minidom.getDOMImplementation()


def _intern(builder, s):
    return builder._intern_setdefault(s, s)

def _parse_ns_name(builder, name):
    assert ' ' in name
    parts = name.split(' ')
    intern = builder._intern_setdefault
    if len(parts) == 3:
        uri, localname, prefix = parts
        prefix = intern(prefix, prefix)
        s = "%s:%s" % (prefix, localname)
        qname = intern(s, s)
        localname = intern(localname, localname)
    else:
        uri, localname = parts
        prefix = None
        qname = localname = intern(localname, localname)
    return intern(uri, uri), localname, prefix, qname


class ExpatBuilder:
    """Document builder that uses Expat to build a ParsedXML.DOM document
    instance."""

    def __init__(self, options=None):
        if options is None:
            options = xmlbuilder.Options()
        self._options = options
        if self._options.filter is not None:
            self._filter = FilterVisibilityController(self._options.filter)
        else:
            self._filter = None
            # This *really* doesn't do anything in this case, so
            # override it with something fast & minimal.
            self._finish_start_element = id
        self._parser = None
        self.reset()

    def createParser(self):
        """Create a new parser object."""
        return expat.ParserCreate()

    def getParser(self):
        """Return the parser object, creating a new one if needed."""
        if not self._parser:
            self._parser = self.createParser()
            self._intern_setdefault = self._parser.intern.setdefault
            self._parser.buffer_text = 1
            self._parser.ordered_attributes = 1
            self._parser.specified_attributes = 1
            self.install(self._parser)
        return self._parser

    def reset(self):
        """Free all data structures used during DOM construction."""
        self.document = None
        self._cdata = 0
        self._standalone = -1
        self._version = None
        self._encoding = None
        self._doctype_args = None
        self._entities = []
        self._notations = []
        self._pre_doc_events = []
        self._attr_info = {}
        self._elem_info = {}

    def install(self, parser):
        """Install the callbacks needed to build the DOM into the parser."""
        # This creates circular references!
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.StartElementHandler = self.start_element_handler
        parser.EndElementHandler = self.end_element_handler
        parser.ProcessingInstructionHandler = self.pi_handler
        if self._options.create_entity_nodes:
            parser.EntityDeclHandler = self.entity_decl_handler
        parser.NotationDeclHandler = self.notation_decl_handler
        if self._options.comments:
            parser.CommentHandler = self.comment_handler
        if self._options.create_cdata_nodes:
            parser.StartCdataSectionHandler = self.start_cdata_section_handler
            parser.EndCdataSectionHandler = self.end_cdata_section_handler
            parser.CharacterDataHandler = self.character_data_handler_cdata
        else:
            parser.CharacterDataHandler = self.character_data_handler
        parser.ExternalEntityRefHandler = self.external_entity_ref_handler
        parser.XmlDeclHandler = self.xml_decl_handler
        parser.ElementDeclHandler = self.element_decl_handler
        parser.AttlistDeclHandler = self.attlist_decl_handler

    def parseFile(self, file):
        """Parse a document from a file object, returning the document
        node."""
        parser = self.getParser()
        first_buffer = 1
        strip_newline = 0
        while 1:
            buffer = file.read(16*1024)
            if not buffer:
                break
            if strip_newline:
                if buffer[0] == "\n":
                    buffer = buffer[1:]
                strip_newline = 0
            if buffer and buffer[-1] == "\r":
                strip_newline = 1
            buffer = _normalize_lines(buffer)
            parser.Parse(buffer, 0)
            if first_buffer and self.document:
                if self.document.doctype:
                    self._setup_subset(buffer)
                first_buffer = 0
        parser.Parse("", 1)
        doc = self.document
        self.reset()
        self._parser = None
        return doc

    def parseString(self, string):
        """Parse a document from a string, returning the document node."""
        string = _normalize_lines(string)
        parser = self.getParser()
        parser.Parse(string, 1)
        self._setup_subset(string)
        doc = self.document
        self.reset()
        self._parser = None
        return doc

    def _setup_subset(self, buffer):
        """Load the internal subset if there might be one."""
        if self.document.doctype:
            extractor = InternalSubsetExtractor()
            extractor.parseString(buffer)
            subset = extractor.getSubset()
            if subset is not None:
                d = self.document.doctype.__dict__
                d['internalSubset'] = subset

    def start_doctype_decl_handler(self, doctypeName, systemId, publicId,
                                   has_internal_subset):
        self._pre_doc_events.append(("doctype",))
        self._doctype_args = (doctypeName, publicId, systemId)

    def pi_handler(self, target, data):
        if self.document is None:
            self._pre_doc_events.append(("pi", target, data))
        else:
            node = self.document.createProcessingInstruction(target, data)
            _appendChild(self.curNode, node)
            if (  self._filter and
                  self._filter.doNode(node) == xmlbuilder.REJECT):
                curNode.removeChild(node)

    def character_data_handler_cdata(self, data):
        childNodes = self.curNode.childNodes
        if self._cdata:
            if (  self._cdata_continue
                  and childNodes[-1].nodeType == CDATA_SECTION_NODE):
                childNodes[-1].appendData(data)
                return
            node = self.document.createCDATASection(data)
            self._cdata_continue = 1
        elif childNodes and childNodes[-1].nodeType == TEXT_NODE:
            node = childNodes[-1]
            node.data = node.data + data
            return
        else:
            node = minidom.Text()
            node.data = data
            node.ownerDocument = self.document
        _appendChild(self.curNode, node)

    def character_data_handler(self, data):
        childNodes = self.curNode.childNodes
        if childNodes and childNodes[-1].nodeType == TEXT_NODE:
            node = childNodes[-1]
            node.data = node.data + data
            return
        node = minidom.Text()
        node.data = data
        node.ownerDocument = self.document
        _appendChild(self.curNode, node)

    def entity_decl_handler(self, entityName, is_parameter_entity, value,
                            base, systemId, publicId, notationName):
        if is_parameter_entity:
            # we don't care about parameter entities for the DOM
            return
        if not self._options.create_entity_nodes:
            return
        node = minidom.Entity(entityName, publicId, systemId, notationName)
        if value is not None:
            # internal entity
            child = minidom.Text()
            child.data = value
            child.ownerDocument = self.document
            node.__dict__['childNodes'] = minidom.NodeList()
            node.childNodes.append(child)
        self._entities.append(node)

    def notation_decl_handler(self, notationName, base, systemId, publicId):
        node = minidom.Notation(notationName, publicId, systemId)
        self._notations.append(node)

    def comment_handler(self, data):
        if self.document is None:
            self._pre_doc_events.append(("comment", data))
        else:
            node = self.document.createComment(data)
            _appendChild(self.curNode, node)
            if (  self._filter and
                  self._filter.doNode(node) == xmlbuilder.REJECT):
                curNode.removeChild(node)

    def start_cdata_section_handler(self):
        self._cdata = 1
        self._cdata_continue = 0

    def end_cdata_section_handler(self):
        self._cdata = 0
        self._cdata_continue = 0

    def external_entity_ref_handler(self, context, base, systemId, publicId):
        return 1

    def start_element_handler(self, name, attributes):
        if self.document is None:
            doctype = self._create_doctype()
            doc = theDOMImplementation.createDocument(
                None, name, doctype)
            if self._standalone >= 0:
                doc.standalone = self._standalone
            doc.encoding = self._encoding
            doc.version = self._version
            self.document = doc
            self._include_early_events()
            node = doc.documentElement
        else:
            node = self.document.createElement(name)
            _appendChild(self.curNode, node)
        self.curNode = node

        if attributes:
            for i in range(0, len(attributes), 2):
                a = minidom.Attr(attributes[i], EMPTY_NAMESPACE, None, None)
                d = a.__dict__
                d['value'] = d['nodeValue'] = attributes[i+1]
                d['ownerDocument'] = self.document
                _setAttributeNode(node, a)

        self._finish_start_element(node)

    def _finish_start_element(self, node):
        if self._filter:
            # To be general, we'd have to call isSameNode(), but this
            # is sufficient for minidom:
            if node is self.document.documentElement:
                return
            filt = self._filter.startNode(node)
            if filt == xmlbuilder.REJECT:
                # ignore this node & all descendents
                Rejecter(self)
            elif filt == xmlbuilder.SKIP:
                # ignore this node, but make it's children become
                # children of the parent node
                Skipper(self)
            else:
                return
            self.curNode = node.parentNode
            node.parentNode.removeChild(node)
            node.unlink()

    # If this ever changes, Namespaces.end_element_handler() needs to
    # be changed to match.
    #
    def end_element_handler(self, name):
        curNode = self.curNode
        self.curNode = curNode.parentNode
        self._finish_end_element(curNode)

    def _finish_end_element(self, curNode):
        info = self._elem_info.get(curNode.tagName)
        if info:
            self._handle_white_text_nodes(curNode, info)
        if self._filter:
            if curNode is self.document.documentElement:
                return
            if self._filter.endNode(curNode) == xmlbuilder.REJECT:
                self.curNode.removeChild(curNode)
                curNode.unlink()

    def _handle_white_text_nodes(self, node, info):
        type = info[0]
        if type in (expat.model.XML_CTYPE_ANY,
                    expat.model.XML_CTYPE_MIXED):
            return
        #
        # We have element type information; look for text nodes which
        # contain only whitespace.
        #
        L = []
        for child in node.childNodes:
            if (  child.nodeType == TEXT_NODE
                  and not child.data.strip()):
                L.append(child)
        #
        # Depending on the options, either mark the nodes as ignorable
        # whitespace or remove them from the tree.
        #
        for child in L:
            if self._options.whitespace_in_element_content:
                child.__dict__['isWhitespaceInElementContent'] = 1
            else:
                node.removeChild(child)

    def element_decl_handler(self, name, model):
        self._elem_info[name] = model

    def attlist_decl_handler(self, elem, name, type, default, required):
        if self._attr_info.has_key(elem):
            L = self._attr_info[elem]
        else:
            L = []
            self._attr_info[elem] = L
        L.append([None, name, None, None, default, 0, type, required])

    def xml_decl_handler(self, version, encoding, standalone):
        self._version = version
        self._encoding = encoding
        self._standalone = standalone

    def _create_doctype(self):
        if not self._doctype_args:
            return
        doctype = apply(theDOMImplementation.createDocumentType,
                        self._doctype_args)
        # To modify the entities and notations NamedNodeMaps, we
        # simply need to work with the underlying sequences.
        doctype.entities._seq = self._entities
        doctype.notations._seq = self._notations
        return doctype

    def _include_early_events(self):
        doc = self.document
        if doc.doctype:
            refnode = doc.doctype
        else:
            refnode = doc.documentElement
        for event in self._pre_doc_events:
            t = event[0]
            if t == "comment":
                node = doc.createComment(event[1])
            elif t == "doctype":
                # marker; switch to before document element
                refnode = doc.documentElement
                continue
            elif t == "pi":
                node = doc.createProcessingInstruction(event[1], event[2])
            else:
                raise RuntimeError, "unexpected early event type: " + `t`
            doc.insertBefore(node, refnode)
            if (  self._filter and
                  self._filter.doNode(node) == xmlbuilder.REJECT):
                doc.removeChild(node)

def _normalize_lines(s):
    """Return a copy of 's' with line-endings normalized according to
    XML 1.0 section 2.11."""
    return s.replace("\r\n", "\n").replace("\r", "\n")


class FilterVisibilityController:
    """Wrapper around a DOMBuilderFilter which implements the checks
    to make the whatToShow filter attribute work."""

    def __init__(self, filter):
        self.filter = filter

    def startNode(self, node):
        mask = self._nodetype_mask[node.nodeType]
        if self.filter.whatToShow & mask:
            return self.filter.startNode(node)
        else:
            return xmlbuilder.ACCEPT

    def endNode(self, node):
        mask = self._nodetype_mask[node.nodeType]
        if self.filter.whatToShow & mask:
            return self.filter.endNode(node)
        else:
            return xmlbuilder.ACCEPT

    def doNode(self, node):
        """Combined startNode()/endNode() for everything but elements.

        Using this allows the mask lookup to be done only once,
        and only calls endNode() if startNode() returned ACCEPT.  It
        also makes the logic easier to reader in the main builder.
        """
        mask = self._nodetype_mask[node.nodeType]
        if self.filter.whatToShow & mask:
            filt = self.filter.startNode(node)
            if (  filt == xmlbuilder.ACCEPT
                  and self.filter.whatToShow & mask):
                filt = self.filter.endNode(node)
            return filt
        else:
            return xmlbuilder.ACCEPT

    _nodetype_mask = {
        Node.ELEMENT_NODE:                NodeFilter.SHOW_ELEMENT,
        Node.ATTRIBUTE_NODE:              NodeFilter.SHOW_ATTRIBUTE,
        Node.TEXT_NODE:                   NodeFilter.SHOW_TEXT,
        Node.CDATA_SECTION_NODE:          NodeFilter.SHOW_CDATA_SECTION,
        Node.ENTITY_REFERENCE_NODE:       NodeFilter.SHOW_ENTITY_REFERENCE,
        Node.ENTITY_NODE:                 NodeFilter.SHOW_ENTITY,
        Node.PROCESSING_INSTRUCTION_NODE: NodeFilter.SHOW_PROCESSING_INSTRUCTION,
        Node.COMMENT_NODE:                NodeFilter.SHOW_COMMENT,
        Node.DOCUMENT_NODE:               NodeFilter.SHOW_DOCUMENT,
        Node.DOCUMENT_TYPE_NODE:          NodeFilter.SHOW_DOCUMENT_TYPE,
        Node.DOCUMENT_FRAGMENT_NODE:      NodeFilter.SHOW_DOCUMENT_FRAGMENT,
        Node.NOTATION_NODE:               NodeFilter.SHOW_NOTATION,
        }


class FilterCrutch:
    _level = 0

    def __init__(self, builder):
        self._builder = builder
        parser = builder._parser
        self._old_start = parser.StartElementHandler
        self._old_end = parser.EndElementHandler
        parser.StartElementHandler = self.start_element_handler
        parser.EndElementHandler = self.end_element_handler

class Rejecter(FilterCrutch):
    def __init__(self, builder):
        FilterCrutch.__init__(self, builder)
        parser = builder._parser
        for name in ("ProcessingInstructionHandler",
                     "CommentHandler",
                     "CharacterDataHandler",
                     "StartCdataSectionHandler",
                     "EndCdataSectionHandler",
                     "ExternalEntityRefHandler",
                     ):
            setattr(parser, name, None)

    def start_element_handler(self, *args):
        self._level = self._level + 1

    def end_element_handler(self, *args):
        if self._level == 0:
            # restore the old handlers
            parser = self._builder._parser
            self._builder.install(parser)
            parser.StartElementHandler = self._old_start
            parser.EndElementHandler = self._old_end
        else:
            self._level = self._level - 1

class Skipper(FilterCrutch):
    def start_element_handler(self, *args):
        node = self._builder.curNode
        self._old_start(*args)
        if self._builder.curNode is not node:
            self._level = self._level + 1

    def end_element_handler(self, *args):
        if self._level == 0:
            # We're popping back out of the node we're skipping, so we
            # shouldn't need to do anything but reset the handlers.
            self._builder._parser.StartElementHandler = self._old_start
            self._builder._parser.EndElementHandler = self._old_end
            self._builder = None
        else:
            self._level = self._level - 1
            self._old_end(*args)


# framework document used by the fragment builder.
# Takes a string for the doctype, subset string, and namespace attrs string.

_FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID = \
    "http://xml.python.org/entities/fragment-builder/internal"

_FRAGMENT_BUILDER_TEMPLATE = (
    '''\
<!DOCTYPE wrapper
  %%s [
  <!ENTITY fragment-builder-internal
    SYSTEM "%s">
%%s
]>
<wrapper %%s
>&fragment-builder-internal;</wrapper>'''
    % _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID)


class FragmentBuilder(ExpatBuilder):
    """Builder which constructs document fragments given XML source
    text and a context node.

    The context node is expected to provide information about the
    namespace declarations which are in scope at the start of the
    fragment.
    """

    def __init__(self, context, options=None):
        if context.nodeType == DOCUMENT_NODE:
            self.originalDocument = context
            self.context = context
        else:
            self.originalDocument = context.ownerDocument
            self.context = context
        ExpatBuilder.__init__(self, options)

    def reset(self):
        ExpatBuilder.reset(self)
        self.fragment = None

    def parseFile(self, file):
        """Parse a document fragment from a file object, returning the
        fragment node."""
        return self.parseString(file.read())

    def parseString(self, string):
        """Parse a document fragment from a string, returning the
        fragment node."""
        self._source = string
        parser = self.getParser()
        doctype = self.originalDocument.doctype
        ident = ""
        if doctype:
            subset = doctype.internalSubset or self._getDeclarations()
            if doctype.publicId:
                ident = ('PUBLIC "%s" "%s"'
                         % (doctype.publicId, doctype.systemId))
            elif doctype.systemId:
                ident = 'SYSTEM "%s"' % doctype.systemId
        else:
            subset = ""
        nsattrs = self._getNSattrs() # get ns decls from node's ancestors
        document = _FRAGMENT_BUILDER_TEMPLATE % (ident, subset, nsattrs)
        try:
            parser.Parse(document, 1)
        except:
            self.reset()
            raise
        fragment = self.fragment
        self.reset()
##         self._parser = None
        return fragment

    def _getDeclarations(self):
        """Re-create the internal subset from the DocumentType node.

        This is only needed if we don't already have the
        internalSubset as a string.
        """
        doctype = self.context.ownerDocument.doctype
        s = ""
        if doctype:
            for i in range(doctype.notations.length):
                notation = doctype.notations.item(i)
                if s:
                    s = s + "\n  "
                s = "%s<!NOTATION %s" % (s, notation.nodeName)
                if notation.publicId:
                    s = '%s PUBLIC "%s"\n             "%s">' \
                        % (s, notation.publicId, notation.systemId)
                else:
                    s = '%s SYSTEM "%s">' % (s, notation.systemId)
            for i in range(doctype.entities.length):
                entity = doctype.entities.item(i)
                if s:
                    s = s + "\n  "
                s = "%s<!ENTITY %s" % (s, entity.nodeName)
                if entity.publicId:
                    s = '%s PUBLIC "%s"\n             "%s"' \
                        % (s, entity.publicId, entity.systemId)
                elif entity.systemId:
                    s = '%s SYSTEM "%s"' % (s, entity.systemId)
                else:
                    s = '%s "%s"' % (s, entity.firstChild.data)
                if entity.notationName:
                    s = "%s NOTATION %s" % (s, entity.notationName)
                s = s + ">"
        return s

    def _getNSattrs(self):
        return ""

    def external_entity_ref_handler(self, context, base, systemId, publicId):
        if systemId == _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID:
            # this entref is the one that we made to put the subtree
            # in; all of our given input is parsed in here.
            old_document = self.document
            old_cur_node = self.curNode
            parser = self._parser.ExternalEntityParserCreate(context)
            # put the real document back, parse into the fragment to return
            self.document = self.originalDocument
            self.fragment = self.document.createDocumentFragment()
            self.curNode = self.fragment
            try:
                parser.Parse(self._source, 1)
            finally:
                self.curNode = old_cur_node
                self.document = old_document
                self._source = None
            return -1
        else:
            return ExpatBuilder.external_entity_ref_handler(
                self, context, base, systemId, publicId)


class Namespaces:
    """Mix-in class for builders; adds support for namespaces."""

    def _initNamespaces(self):
        # list of (prefix, uri) ns declarations.  Namespace attrs are
        # constructed from this and added to the element's attrs.
        self._ns_ordered_prefixes = []

    def createParser(self):
        """Create a new namespace-handling parser."""
        parser = expat.ParserCreate(namespace_separator=" ")
        parser.namespace_prefixes = 1
        return parser

    def install(self, parser):
        """Insert the namespace-handlers onto the parser."""
        ExpatBuilder.install(self, parser)
        parser.StartNamespaceDeclHandler = self.start_namespace_decl_handler

    def start_namespace_decl_handler(self, prefix, uri):
        """Push this namespace declaration on our storage."""
        self._ns_ordered_prefixes.append((prefix, uri))

    def start_element_handler(self, name, attributes):
        if ' ' in name:
            uri, localname, prefix, qname = _parse_ns_name(self, name)
        else:
            uri = EMPTY_NAMESPACE
            qname = name
            localname = prefix = None
        if self.document is None:
            doctype = self._create_doctype()
            doc = theDOMImplementation.createDocument(
                uri, qname, doctype)
            if self._standalone >= 0:
                doc.standalone = self._standalone
            doc.encoding = self._encoding
            doc.version = self._version
            self.document = doc
            self._include_early_events()
            node = doc.documentElement
        else:
            node = minidom.Element(qname, uri, prefix, localname)
            node.ownerDocument = self.document
            _appendChild(self.curNode, node)
        self.curNode = node

        if self._ns_ordered_prefixes and self._options.namespace_declarations:
            for prefix, uri in self._ns_ordered_prefixes:
                
                if prefix:
                    a = minidom.Attr(_intern(self, 'xmlns:' + prefix),
                                     XMLNS_NAMESPACE, prefix, "xmlns")
                else:
                    a = minidom.Attr("xmlns", XMLNS_NAMESPACE, "xmlns", None)
                d = a.__dict__
                d['value'] = d['nodeValue'] = uri
                d['ownerDocument'] = self.document
                _setAttributeNode(node, a)
            del self._ns_ordered_prefixes[:]

        if attributes:
            # This uses the most-recently declared prefix, not necessarily
            # the right one.
            _attrs = node._attrs
            _attrsNS = node._attrsNS
            for i in range(0, len(attributes), 2):
                aname = attributes[i]
                value = attributes[i+1]
                if ' ' in aname:
                    uri, localname, prefix, qname = _parse_ns_name(self, aname)
                    a = minidom.Attr(qname, uri, localname, prefix)
                    _attrs[localname] = a
                    _attrsNS[(uri, localname)] = a
                else:
                    a = minidom.Attr(aname, EMPTY_NAMESPACE, aname, None)
                    _attrs[aname] = a
                    _attrsNS[(EMPTY_NAMESPACE, aname)] = a
                d = a.__dict__
                d['ownerDocument'] = self.document
                d['value'] = d['nodeValue'] = value
                d['ownerElement'] = node

    if __debug__:
        # This only adds some asserts to the original
        # end_element_handler(), so we only define this when -O is not
        # used.  If changing one, be sure to check the other to see if
        # it needs to be changed as well.
        #
        def end_element_handler(self, name):
            curNode = self.curNode
            if ' ' in name:
                uri, localname, prefix, qname = _parse_ns_name(name)
                assert (curNode.namespaceURI == uri
                        and curNode.localName == localname
                        and curNode.prefix == prefix), \
                        "element stack messed up! (namespace)"
            else:
                assert curNode.nodeName == name, \
                       "element stack messed up - bad nodeName"
                assert curNode.namespaceURI == EMPTY_NAMESPACE, \
                       "element stack messed up - bad namespaceURI"
            self.curNode = curNode.parentNode
            self._finish_end_element(curNode)


class ExpatBuilderNS(Namespaces, ExpatBuilder):
    """Document builder that supports namespaces."""

    def reset(self):
        ExpatBuilder.reset(self)
        self._initNamespaces()


class FragmentBuilderNS(Namespaces, FragmentBuilder):
    """Fragment builder that supports namespaces."""

    def reset(self):
        FragmentBuilder.reset(self)
        self._initNamespaces()

    def _getNSattrs(self):
        """Return string of namespace attributes from this element and
        ancestors."""
        # XXX This needs to be re-written to walk the ancestors of the
        # context to build up the namespace information from
        # declarations, elements, and attributes found in context.
        # Otherwise we have to store a bunch more data on the DOM
        # (though that *might* be more reliable -- not clear).
        attrs = ""
        context = self.context
        L = []
        while context:
            if hasattr(context, '_ns_prefix_uri'):
                for prefix, uri in context._ns_prefix_uri.items():
                    # add every new NS decl from context to L and attrs string
                    if prefix in L:
                        continue
                    L.append(prefix)
                    if prefix:
                        declname = "xmlns:" + prefix
                    else:
                        declname = "xmlns"
                    if attrs:
                        attrs = "%s\n    %s='%s'" % (attrs, declname, uri)
                    else:
                        attrs = " %s='%s'" % (declname, uri)
            context = context.parentNode
        return attrs


class ParseEscape(Exception):
    """Exception raised to short-circuit parsing in InternalSubsetExtractor."""
    pass

class InternalSubsetExtractor(ExpatBuilder):
    """XML processor which can rip out the internal document type subset."""

    subset = None

    def getSubset(self):
        """Return the internal subset as a string."""
        subset = self.subset
        while subset and subset[0] != "[":
            del subset[0]
        if subset:
            x = subset.index("]")
            return _nulljoin(subset[1:x])
        else:
            return None

    def parseFile(self, file):
        try:
            ExpatBuilder.parseFile(self, file)
        except ParseEscape:
            pass

    def parseString(self, string):
        try:
            ExpatBuilder.parseString(self, string)
        except ParseEscape:
            pass

    def install(self, parser):
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.EndDoctypeDeclHandler = self.end_doctype_decl_handler
        parser.StartElementHandler = self.start_element_handler

    def start_doctype_decl_handler(self, *args):
        self.subset = []
        self.getParser().DefaultHandler = self.subset.append

    def end_doctype_decl_handler(self):
        self.getParser().DefaultHandler = None
        raise ParseEscape()

    def start_element_handler(self, name, attrs):
        raise ParseEscape()


_nulljoin = "".join


def parse(file, namespaces=1):
    """Parse a document, returning the resulting Document node.

    'file' may be either a file name or an open file object.
    """
    if namespaces:
        builder = ExpatBuilderNS()
    else:
        builder = ExpatBuilder()

    if isinstance(file, type('')):
        fp = open(file, 'rb')
        result = builder.parseFile(fp)
        fp.close()
    else:
        result = builder.parseFile(file)
    return result


def parseString(string, namespaces=1):
    """Parse a document from a string, returning the resulting
    Document node.
    """
    if namespaces:
        builder = ExpatBuilderNS()
    else:
        builder = ExpatBuilder()
    return builder.parseString(string)


def parseFragment(file, context, namespaces=1):
    """Parse a fragment of a document, given the context from which it
    was originally extracted.  context should be the parent of the
    node(s) which are in the fragment.

    'file' may be either a file name or an open file object.
    """
    if namespaces:
        builder = FragmentBuilderNS(context)
    else:
        builder = FragmentBuilder(context)

    if isinstance(file, type('')):
        fp = open(file, 'rb')
        result = builder.parseFile(fp)
        fp.close()
    else:
        result = builder.parseFile(file)
    return result


def parseFragmentString(string, context, namespaces=1):
    """Parse a fragment of a document from a string, given the context
    from which it was originally extracted.  context should be the
    parent of the node(s) which are in the fragment.
    """
    if namespaces:
        builder = FragmentBuilderNS(context)
    else:
        builder = FragmentBuilder(context)
    return builder.parseString(string)


def makeBuilder(options):
    """Create a builder based on an Options object."""
    if options.namespaces:
        return ExpatBuilderNS(options)
    else:
        return ExpatBuilder(options)
