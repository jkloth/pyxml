"""
This module contains the core classes of version 2.0 of SAX for Python.
This file provides only default classes with absolutely minimum
functionality, from which drivers and applications can be subclassed.

Many of these classes are empty and are included only as documentation
of the interfaces.

$Id: saxlib.py,v 1.6 2000/05/15 20:21:48 lars Exp $
"""

version = '2.0beta'

#============================================================================
#
# MAIN INTERFACES
#
#============================================================================

# ===== XMLREADER =====

class XMLReader:

    def __init__(self):
	self._cont_handler = ContentHandler()
	self._dtd_handler  = DTDHandler()
	self._ent_handler  = EntityResolver()
	self._err_handler  = ErrorHandler()

    def parse(self, source):
	"Parse an XML document from a system identifier or an InputSource."
        raise NotImplementedError("This method must be implemented!")

    def getContentHandler(self):
        "Returns the current ContentHandler."
        return self._cont_handler

    def setContentHandler(self, handler):
        "Registers a new object to receive document content events."
        self._cont_handler = handler
        
    def getDTDHandler(self):
        "Returns the current DTD handler."
        return self._dtd_handler
        
    def setDTDHandler(self, handler):
	"Register an object to receive basic DTD-related events."
	self._dtd_handler = handler

    def getEntityResolver(self):
        "Returns the current EntityResolver."
        return self._ent_handler
        
    def setEntityResolver(self, resolver):
	"Register an object to resolve external entities."
	self._ent_handler = resolver

    def getErrorHandler(self):
        "Returns the current ErrorHandler."
        return self._err_handler
        
    def setErrorHandler(self, handler):
	"Register an object to receive error-message events."
	self._err_handler = handler

    def setLocale(self, locale):
        """Allow an application to set the locale for errors and warnings. 
   
        SAX parsers are not required to provide localisation for errors
        and warnings; if they cannot support the requested locale,
        however, they must throw a SAX exception. Applications may
        request a locale change in the middle of a parse."""
        raise SAXNotSupportedException("Locale support not implemented")
    
    def getFeature(self, name):
        "Looks up and returns the state of a SAX2 feature."
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def setFeature(self, name, state):
        "Sets the state of a SAX2 feature."
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def getProperty(self, name):
        "Looks up and returns the value of a SAX2 property."
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def setProperty(self, name, value):
        "Sets the value of a SAX2 property."
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    
# ===== INPUTSOURCE =====

class InputSource:
    """Encapsulation of the information needed by the XMLReader to
    read entities.

    This class may include information about the public identifier,
    system identifier, byte stream (possibly with character encoding
    information) and/or the character stream of an entity.

    Applications will create objects of this class for use in the
    XMLReader.parse method and for returning from
    EntityResolver.resolveEntity.

    An InputSource belongs to the application, the XMLReader is not
    allowed to modify InputSource objects passed to it from the
    application, although it may make copies and modify those."""

    def __init__(self, system_id = None):
        self.__system_id = system_id
        self.__public_id = None
        self.__encoding  = None
        self.__bytefile  = None
        self.__charfile  = None

    def setPublicId(self, public_id):
        "Sets the public identifier of this InputSource."
        self.__public_id = public_id

    def getPublicId(self):
        "Returns the public identifier of this InputSource."
        return self.__public_id

    def setSystemId(self, system_id):
        "Sets the system identifier of this InputSource."
        self.__system_id = system_id

    def getSystemId(self):
        "Returns the system identifier of this InputSource."
        return self.__system_id

    def setEncoding(self, encoding):
        """Sets the character encoding of this InputSource.

        The encoding must be a string acceptable for an XML encoding
        declaration (see section 4.3.3 of the XML recommendation).

        The encoding attribute of the InputSource is ignored if the
        InputSource also contains a character stream."""
        self.__encoding = encoding

    def getEncoding(self):
        "Get the character encoding of this InputSource."
        return self.__encoding

    def setByteStream(self, bytefile):
        """Set the byte stream (a Python file-like object which does
        not perform byte-to-character conversion) for this input
        source.
        
        The SAX parser will ignore this if there is also a character
        stream specified, but it will use a byte stream in preference
        to opening a URI connection itself.

        If the application knows the character encoding of the byte
        stream, it should set it with the setEncoding method."""
        self.__bytefile = bytefile

    def getByteStream(self):
        """Get the byte stream for this input source.
        
        The getEncoding method will return the character encoding for
        this byte stream, or None if unknown."""        
        return self.__bytefile
        
    def setCharacterStream(self, charfile):
        """Set the character stream for this input source. (The stream
        must be a Python 1.6 Unicode-wrapped file-like that performs
        conversion to Unicode strings.)
        
        If there is a character stream specified, the SAX parser will
        ignore any byte stream and will not attempt to open a URI
        connection to the system identifier."""
        self.__charfile = charfile

    def getCharacterStream(self):
        "Get the character stream for this input source."
        return self.__charfile
    
        
# ===== LOCATOR =====

class Locator:
    """Interface for associating a SAX event with a document
    location. A locator object will return valid results only during
    calls to DocumentHandler methods; at any other time, the
    results are unpredictable."""
    
    def getColumnNumber(self):
	"Return the column number where the current event ends."
	return -1

    def getLineNumber(self):
	"Return the line number where the current event ends."
	return -1

    def getPublicId(self):
	"Return the public identifier for the current event."
	return None

    def getSystemId(self):
	"Return the system identifier for the current event."
	return None


# ===== ErrorHandler =====

class ErrorHandler:
    """Basic interface for SAX error handlers. If you create an object
    that implements this interface, then register the object with your
    Parser, the parser will call the methods in your object to report
    all warnings and errors. There are three levels of errors
    available: warnings, (possibly) recoverable errors, and
    unrecoverable errors. All methods take a SAXParseException as the
    only parameter."""

    def error(self, exception):
	"Handle a recoverable error."

    def fatalError(self, exception):
	"Handle a non-recoverable error."

    def warning(self, exception):
	"Handle a warning."   
    
# ===== XMLFILTER =====

class XMLFilter(XMLReader):
    """Interface for a SAX2 parser filter.

    A parser filter is an XMLReader that gets its events from another
    XMLReader (which may in turn also be a filter) rather than from a
    primary source like a document or other non-SAX data source.
    Filters can modify a stream of events before passing it on to its
    handlers."""

    def __init__(self, parent = None):
        """Creates a filter instance, allowing applications to set the
        parent on instantiation."""
        XMLReader.__init__(self)
        self._parent = parent
    
    def setParent(self, parent):        
        """Sets the parent XMLReader of this filter. The argument may
        not be None."""
        self._parent = parent

    def getParent(self):
        "Returns the parent of this filter."
        return self._parent

    
# ===== ATTRIBUTES =====

class Attributes:
    """Interface for a list of XML attributes.

    Contains a list of XML attributes, accessible by name."""

    def getLength(self):
        "Returns the number of attributes in the list."
        raise NotImplementedError("This method must be implemented!")

    def getType(self, name):
        "Returns the type of the attribute with the given name."
        raise NotImplementedError("This method must be implemented!")

    def getValue(self, name):
        "Returns the value of the attribute with the given name."
        raise NotImplementedError("This method must be implemented!")

    def getValueByQName(self, name):
        """Returns the value of the attribute with the given raw (or
        qualified) name."""
        raise NotImplementedError("This method must be implemented!")

    def getNameByQName(self, name):
        """Returns the namespace name of the attribute with the given
        raw (or qualified) name."""
        raise NotImplementedError("This method must be implemented!")
    
    def getNames(self):
        """Returns a list of the names of all attributes 
        in the list."""
        raise NotImplementedError("This method must be implemented!")
    
    def getQNames(self):
        """Returns a list of the raw qualified names of all attributes
        in the list."""
        raise NotImplementedError("This method must be implemented!")
    
    def __len__(self):
	"Alias for getLength."
        raise NotImplementedError("This method must be implemented!")

    def __getitem__(self, name):
	"Alias for getValue."
        raise NotImplementedError("This method must be implemented!")

    def keys(self):
	"Returns a list of the attribute names in the list."
        raise NotImplementedError("This method must be implemented!")

    def has_key(self, name):
	"True if the attribute is in the list, false otherwise."
        raise NotImplementedError("This method must be implemented!")

    def get(self, name, alternative=None):
        """Return the value associated with attribute name; if it is not
        available, then return the alternative."""
        raise NotImplementedError("This method must be implemented!")

    def copy(self):
        "Return a copy of the Attributes object."
        raise NotImplementedError("This method must be implemented!")

    def items(self):
        "Return a list of (attribute_name, value) pairs."
        raise NotImplementedError("This method must be implemented!")

    def values(self):
        "Return a list of all attribute values."
        raise NotImplementedError("This method must be implemented!")

    
#============================================================================
#
# EXCEPTIONS
#
#============================================================================

import sys
if sys.platform[:4] == "java":
    from java.lang import Exception


# ===== SAXEXCEPTION =====
    
class SAXException(Exception):
    """Encapsulate an XML error or warning. This class can contain
    basic error or warning information from either the XML parser or
    the application: you can subclass it to provide additional
    functionality, or to add localization. Note that although you will
    receive a SAXException as the argument to the handlers in the
    ErrorHandler interface, you are not actually required to throw
    the exception; instead, you can simply read the information in
    it."""
    
    def __init__(self, msg, exception = None):
        """Creates an exception. The message is required, but the exception
        is optional."""
        self._msg = msg
        self._exception = exception

    def getMessage(self):
	"Return a message for this exception."
	return self._msg

    def getException(self):
        "Return the embedded exception, or None if there was none."
        return self._exception

    def __str__(self):
        "Create a string representation of the exception."
        return self._msg

    def __getitem__(self, ix):
        """Avoids weird error messages if someone does exception[ix] by
        mistake, since Exception has __getitem__ defined."""
        raise NameError("__getitem__")

    
# ===== SAXPARSEEXCEPTION =====

class SAXParseException(SAXException):    
    """Encapsulate an XML parse error or warning.
    
    This exception will include information for locating the error in
    the original XML document. Note that although the application will
    receive a SAXParseException as the argument to the handlers in the
    ErrorHandler interface, the application is not actually required
    to throw the exception; instead, it can simply read the
    information in it and take a different action.

    Since this exception is a subclass of SAXException, it inherits
    the ability to wrap another exception."""
    
    def __init__(self, msg, exception, locator):
        "Creates the exception. The exception parameter is allowed to be None."
        SAXException.__init__(self, msg, exception)
        self._locator = locator
        
    def getColumnNumber(self):
	"""The column number of the end of the text where the exception
	occurred."""
	return self._locator.getColumnNumber()

    def getLineNumber(self):
	"The line number of the end of the text where the exception occurred."
	return self._locator.getLineNumber()

    def getPublicId(self):
	"Get the public identifier of the entity where the exception occurred."
	return self._locator.getPublicId()

    def getSystemId(self):
	"Get the system identifier of the entity where the exception occurred."
	return self._locator.getSystemId()

    def __str__(self):
        "Create a string representation of the exception."
        return "%s at %s:%d:%d" % (self._msg,
                                   self.getSystemId(),
                                   self.getLineNumber(),
                                   self.getColumnNumber())

    
# ===== SAXNOTRECOGNIZEDEXCEPTION =====

class SAXNotRecognizedException(SAXException):
    """Exception class for an unrecognized identifier.

    An XMLReader will raise this exception when it is confronted with an
    unrecognized feature or property. SAX applications and extensions may
    use this class for similar purposes."""

    
# ===== SAXNOTSUPPORTEDEXCEPTION =====
    
class SAXNotSupportedException(SAXException):
    """Exception class for an unsupported operation.

    An XMLReader will raise this exception when a service it cannot
    perform is requested (specifically setting a state or value). SAX
    applications and extensions may use this class for similar
    purposes."""


#============================================================================
#
# HANDLER INTERFACES
#
#============================================================================

# ===== CONTENTHANDLER =====

class ContentHandler:
    """Interface for receiving logical document content events.

    This is the main callback interface in SAX, and the one most
    important to applications. The order of events in this interface
    mirrors the order of the information in the document."""

    def __init__(self):
        self._locator = None
    
    def setDocumentLocator(self, locator):
        """Called by the parser to give the application a locator for
        locating the origin of document events.

        SAX parsers are strongly encouraged (though not absolutely
        required) to supply a locator: if it does so, it must supply
        the locator to the application by invoking this method before
        invoking any of the other methods in the DocumentHandler
        interface.

        The locator allows the application to determine the end
        position of any document-related event, even if the parser is
        not reporting an error. Typically, the application will use
        this information for reporting its own errors (such as
        character content that does not match an application's
        business rules). The information returned by the locator is
        probably not sufficient for use with a search engine.
        
        Note that the locator will return correct information only
        during the invocation of the events in this interface. The
        application should not attempt to use it at any other time."""
        self._locator = locator        

    def startDocument(self):
        """Receive notification of the beginning of a document.
        
        The SAX parser will invoke this method only once, before any
        other methods in this interface or in DTDHandler (except for
        setDocumentLocator)."""

    def endDocument(self):
        """Receive notification of the end of a document.
        
        The SAX parser will invoke this method only once, and it will
        be the last method invoked during the parse. The parser shall
        not invoke this method until it has either abandoned parsing
        (because of an unrecoverable error) or reached the end of
        input."""

    def startPrefixMapping(self, prefix, uri):
        """Begin the scope of a prefix-URI Namespace mapping.
        
        The information from this event is not necessary for normal
        Namespace processing: the SAX XML reader will automatically
        replace prefixes for element and attribute names when the
        http://xml.org/sax/features/namespaces feature is true (the
        default).
        
        There are cases, however, when applications need to use
        prefixes in character data or in attribute values, where they
        cannot safely be expanded automatically; the
        start/endPrefixMapping event supplies the information to the
        application to expand prefixes in those contexts itself, if
        necessary.

        Note that start/endPrefixMapping events are not guaranteed to
        be properly nested relative to each-other: all
        startPrefixMapping events will occur before the corresponding
        startElement event, and all endPrefixMapping events will occur
        after the corresponding endElement event, but their order is
        not guaranteed."""

    def endPrefixMapping(self, prefix):
        """End the scope of a prefix-URI mapping.
        
        See startPrefixMapping for details. This event will always
        occur after the corresponding endElement event, but the order
        of endPrefixMapping events is not otherwise guaranteed."""

    def startElement(self, name, qname, attrs):
        """Signals the start of an element.

        The name parameter contains the name of the element type as a
        (uri ,localname) tuple, the qname parameter the raw XML 1.0
        name used in the source document, and the attrs parameter
        holds an instance of the Attributes class containing the
        attributes of the element."""

    def endElement(self, name, qname):
        """Signals the end of an element.

        The name parameter contains the name of the element type, just
        as with the startElement event."""

    def characters(self, content):
        """Receive notification of character data.
        
        The Parser will call this method to report each chunk of
        character data. SAX parsers may return all contiguous
        character data in a single chunk, or they may split it into
        several chunks; however, all of the characters in any single
        event must come from the same external entity so that the
        Locator provides useful information."""

    def ignorableWhitespace(self, chars, start, end):
        """Receive notification of ignorable whitespace in element content.
        
        Validating Parsers must use this method to report each chunk
        of ignorable whitespace (see the W3C XML 1.0 recommendation,
        section 2.10): non-validating parsers may also use this method
        if they are capable of parsing and using content models.
        
        SAX parsers may return all contiguous whitespace in a single
        chunk, or they may split it into several chunks; however, all
        of the characters in any single event must come from the same
        external entity, so that the Locator provides useful
        information.
        
        The application must not attempt to read from the array
        outside of the specified range."""

    def processingInstruction(self, target, data):
        """Receive notification of a processing instruction.
        
        The Parser will invoke this method once for each processing
        instruction found: note that processing instructions may occur
        before or after the main document element.

        A SAX parser should never report an XML declaration (XML 1.0,
        section 2.8) or a text declaration (XML 1.0, section 4.3.1)
        using this method."""

    def skippedEntity(self, name):
        """Receive notification of a skipped entity.
        
        The Parser will invoke this method once for each entity
        skipped. Non-validating processors may skip entities if they
        have not seen the declarations (because, for example, the
        entity was declared in an external DTD subset). All processors
        may skip external entities, depending on the values of the
        http://xml.org/sax/features/external-general-entities and the
        http://xml.org/sax/features/external-parameter-entities
        properties."""


# ===== DECLHANDLER =====

class DeclHandler:
    """Optional SAX2 handler for DTD declaration events.

    Note that some DTD declarations are already reported through the
    DTDHandler interface. All events reported to this handler will
    occur between the startDTD and endDTD events of the
    LexicalHandler.

    To se the DeclHandler for an XMLReader, use the setProperty method
    with the identifier http://xml.org/sax/handlers/DeclHandler."""

    def attributeDecl(self, elem_name, attr_name, type, value_def, value):
        """Report an attribute type declaration.

        Only the first declaration will be reported. The type will be
        one of the strings "CDATA", "ID", "IDREF", "IDREFS",
        "NMTOKEN", "NMTOKENS", "ENTITY", "ENTITIES", or "NOTATION", or
        a list of names (in the case of enumerated definitions).

        elem_name is the element type name, attr_name the attribute
        type name, type a string representing the attribute type,
        value_def a string representing the default declaration
        ('#IMPLIED', '#REQUIRED', '#FIXED' or None). value is a string
        representing the attribute's default value, or None if there
        is none."""

    def elementDecl(self, elem_name, content_model):
        """Report an element type declaration.

        Only the first declaration will be reported.

        content_model is the string 'EMPTY', the string 'ANY' or the content
        model structure represented as tuple (separator, tokens, modifier)
        where separator is the separator in the token list (that is, '|' or
        ','), tokens is the list of tokens (element type names or tuples
        representing parentheses) and modifier is the quantity modifier
        ('*', '?' or '+')."""

    def internalEntityDecl(self, name, value):
        """Report an internal entity declaration.

        Only the first declaration of an entity will be reported.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'. value is the replacement text of
        the entity."""

    def externalEntityDecl(self, name, public_id, system_id):
        """Report a parsed entity declaration. (Unparsed entities are
        reported to the DTDHandler.)

        Only the first declaration for each entity will be reported.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'. public_id and system_id are the
        public and system identifiers of the entity. public_id will be
        None if none were declared."""

        
# ===== DTDHandler =====

class DTDHandler:
    """Handle DTD events. This interface specifies only those DTD
    events required for basic parsing (unparsed entities and
    attributes). If you do not want to implement the entire interface,
    you can extend HandlerBase, which implements the default
    behaviour."""

    def notationDecl(self, name, publicId, systemId):
	"Handle a notation declaration event."

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
	"Handle an unparsed entity declaration event."

        
# ===== ENTITYRESOLVER =====
        
class EntityResolver:
    """Basic interface for resolving entities. If you create an object
    implementing this interface, then register the object with your
    Parser, the parser will call the method in your object to
    resolve all external entities. Note that HandlerBase implements
    this interface with the default behaviour."""
    
    def resolveEntity(self, publicId, systemId):
	"Resolve the system identifier of an entity."
	return systemId


# ===== LEXICALHANDLER =====

class LexicalHandler:
    """Optional SAX2 handler for lexical events.

    This handler is used to obtain lexical information about an XML
    document, that is, information about how the document was encoded
    (as opposed to what it contains, which is reported to the
    ContentHandler), such as comments and CDATA marked section
    boundaries.

    To set the LexicalHandler of an XMLReader, use the setProperty
    method with the property identifier
    'http://xml.org/sax/handlers/LexicalHandler'. There is no
    guarantee that the XMLReader will support or recognize this
    property."""

    def comment(self, content):        
        """Reports a comment anywhere in the document (including the
        DTD and outside the document element).

        content is a string that holds the contents of the comment."""

    def startDTD(self, name, public_id, system_id):
        """Report the start of the DTD declarations, if the document
        has an associated DTD.

        A startEntity event will be reported before declaration events
        from the external DTD subset are reported, and this can be
        used to infer from which subset DTD declarations derive.

        name is the name of the document element type, public_id the
        public identifier of the DTD (or None if none were supplied)
        and system_id the system identfier of the external subset (or
        None if none were supplied)."""

    def endDTD(self):
        "Signals the end of DTD declarations."

    def startEntity(self, name):
        """Report the beginning of an entity.

        The start and end of the document entity is not reported. The
        start and end of the external DTD subset is reported with the
        pseudo-name '[dtd]'.

        Skipped entities will be reported through the skippedEntity
        event of the ContentHandler rather than through this event.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'."""

    def endEntity(self, name):
        """Reports the end of an entity. name is the name of the
        entity, and follows the same conventions as for
        startEntity."""

    def startCDATA(self):
        """Reports the beginning of a CDATA marked section.

        The contents of the CDATA marked section will be reported
        through the characters event."""

    def endCDATA(self):
        "Reports the end of a CDATA marked section."


#============================================================================
#
# PYTHON SAX 2.0 EXTENSION INTERFACES
#
#============================================================================

class IncrementalParser(XMLReader):
    """This interface adds three extra methods to the XMLReader
    interface that allow XML parsers to support incremental
    parsing. Support for this interface is optional, since not all
    underlying XML parsers support this functionality.

    When the parser is instantiated it is ready to begin accepting
    data from the feed method immediately. After parsing has been
    finished with a call to close the reset method must be called to
    make the parser ready to accept new data, either from feed or
    using the parse method.

    Note that these methods must _not_ be called during parsing, that
    is, after parse has been called and before it returns."""

    def feed(self, data):        
        """This method gives the raw XML data in the data parameter to
        the parser and makes it parse the data, emitting the
        corresponding events. It is allowed for XML constructs to be
        split across several calls to feed.

        feed may raise SAXException."""
        raise NotImplementedError("This method must be implemented!")

    def close(self):
        """This method is called when the entire XML document has been
        passed to the parser through the feed method, to notify the
        parser that there are no more data. This allows the parser to
        do the final checks on the document and empty the internal
        data buffer.

        The parser will not be ready to parse another document until
        the reset method has been called.

        close may raise SAXException."""
        raise NotImplementedError("This method must be implemented!")

    def reset(self):
        """This method is called after close has been called to reset
        the parser so that it is ready to parse new documents. The
        results of calling parse or feed after close without calling
        reset are undefined."""
        raise NotImplementedError("This method must be implemented!")

#============================================================================
#
# SAX 1.0 COMPATIBILITY CLASSES
# Note that these are all deprecated.
#
#============================================================================

# ===== ATTRIBUTELIST =====

class AttributeList:
    """Interface for an attribute list. This interface provides
    information about a list of attributes for an element (only
    specified or defaulted attributes will be reported). Note that the
    information returned by this object will be valid only during the
    scope of the DocumentHandler.startElement callback, and the
    attributes will not necessarily be provided in the order declared
    or specified."""

    def getLength(self):
	"Return the number of attributes in list."

    def getName(self, i):
	"Return the name of an attribute in the list."

    def getType(self, i):
	"""Return the type of an attribute in the list. (Parameter can be
	either integer index or attribute name.)"""

    def getValue(self, i):
	"""Return the value of an attribute in the list. (Parameter can be
	either integer index or attribute name.)"""

    def __len__(self):
	"Alias for getLength."

    def __getitem__(self, key):
	"Alias for getName (if key is an integer) and getValue (if string)."

    def keys(self):
	"Returns a list of the attribute names."

    def has_key(self, key):
	"True if the attribute is in the list, false otherwise."

    def get(self, key, alternative=None):
        """Return the value associated with attribute name; if it is not
        available, then return the alternative."""

    def copy(self):
        "Return a copy of the AttributeList."

    def items(self):
        "Return a list of (attribute_name,value) pairs."

    def values(self):
        "Return a list of all attribute values."

        
# ===== DOCUMENTHANDLER =====

class DocumentHandler:
    """Handle general document events. This is the main client
    interface for SAX: it contains callbacks for the most important
    document events, such as the start and end of elements. You need
    to create an object that implements this interface, and then
    register it with the Parser. If you do not want to implement
    the entire interface, you can derive a class from HandlerBase,
    which implements the default functionality. You can find the
    location of any document event using the Locator interface
    supplied by setDocumentLocator()."""

    def characters(self, ch, start, length):
	"Handle a character data event."

    def endDocument(self):
	"Handle an event for the end of a document."

    def endElement(self, name):
	"Handle an event for the end of an element."

    def ignorableWhitespace(self, ch, start, length):
	"Handle an event for ignorable whitespace in element content."

    def processingInstruction(self, target, data):
	"Handle a processing instruction event."

    def setDocumentLocator(self, locator):
	"Receive an object for locating the origin of SAX document events."

    def startDocument(self):
	"Handle an event for the beginning of a document."

    def startElement(self, name, atts):
	"Handle an event for the beginning of an element."

        
# ===== HANDLERBASE =====
        
class HandlerBase(EntityResolver, DTDHandler, DocumentHandler,\
		     ErrorHandler):
    """Default base class for handlers. This class implements the
    default behaviour for four SAX interfaces: EntityResolver,
    DTDHandler, DocumentHandler, and ErrorHandler: rather
    than implementing those full interfaces, you may simply extend
    this class and override the methods that you need. Note that the
    use of this class is optional (you are free to implement the
    interfaces directly if you wish)."""


# ===== PARSER =====

class Parser:
    """Basic interface for SAX (Simple API for XML) parsers. All SAX
    parsers must implement this basic interface: it allows users to
    register handlers for different types of events and to initiate a
    parse from a URI, a character stream, or a byte stream. SAX
    parsers should also implement a zero-argument constructor."""

    def __init__(self):
	self.doc_handler = DocumentHandler()
	self.dtd_handler = DTDHandler()
	self.ent_handler = EntityResolver()
	self.err_handler = ErrorHandler()

    def parse(self, systemId):
	"Parse an XML document from a system identifier."

    def parseFile(self, fileobj):
        "Parse an XML document from a file-like object."

    def setDocumentHandler(self, handler):
	"Register an object to receive basic document-related events."
	self.doc_handler=handler

    def setDTDHandler(self, handler):
	"Register an object to receive basic DTD-related events."
	self.dtd_handler=handler

    def setEntityResolver(self, resolver):
	"Register an object to resolve external entities."
	self.ent_handler=resolver

    def setErrorHandler(self, handler):
	"Register an object to receive error-message events."
	self.err_handler=handler

    def setLocale(self, locale):
        """Allow an application to set the locale for errors and warnings. 
   
        SAX parsers are not required to provide localisation for errors
        and warnings; if they cannot support the requested locale,
        however, they must throw a SAX exception. Applications may
        request a locale change in the middle of a parse."""
        raise SAXNotSupportedException("Locale support not implemented")

        
#============================================================================
#
# CORE FEATURES
#
#============================================================================

feature_namespaces = "http://xml.org/sax/features/namespaces"
# true: Perform Namespace processing (default).
# false: Optionally do not perform Namespace processing
#        (implies namespace-prefixes).
# access: (parsing) read-only; (not parsing) read/write

feature_namespace_prefixes = "http://xml.org/sax/features/namespace-prefixes"
# true: Report the original prefixed names and attributes used for Namespace
#       declarations.
# false: Do not report attributes used for Namespace declarations, and
#        optionally do not report original prefixed names (default).
# access: (parsing) read-only; (not parsing) read/write

feature_string_interning = "http://xml.org/sax/features/string-interning"
# true: All element names, prefixes, attribute names, Namespace URIs, and
#       local names are interned using the built-in intern function.
# false: Names are not necessarily interned, although they may be (default).
# access: (parsing) read-only; (not parsing) read/write

feature_validation = "http://xml.org/sax/features/validation"
# true: Report all validation errors (implies external-general-entities and
#       external-parameter-entities).
# false: Do not report validation errors.
# access: (parsing) read-only; (not parsing) read/write

feature_external_ges = "http://xml.org/sax/features/external-general-entities"
# true: Include all external general (text) entities.
# false: Do not include external general entities.
# access: (parsing) read-only; (not parsing) read/write

feature_external_pes = "http://xml.org/sax/features/external-parameter-entities"
# true: Include all external parameter entities, including the external
#       DTD subset.
# false: Do not include any external parameter entities, even the external
#        DTD subset.
# access: (parsing) read-only; (not parsing) read/write

all_features = [feature_namespaces,
                feature_namespace_prefixes,
                feature_string_interning,
                feature_validation,
                feature_external_ges,
                feature_external_pes]


#============================================================================
#
# CORE PROPERTIES
#
#============================================================================

property_lexical_handler = "http://xml.org/sax/properties/lexical-handler"
# data type: xml.sax.sax2lib.LexicalHandler
# description: An optional extension handler for lexical events like comments.
# access: read/write

property_declaration_handler = "http://xml.org/sax/properties/declaration-handler"
# data type: xml.sax.sax2lib.DeclHandler
# description: An optional extension handler for DTD-related events other
#              than notations and unparsed entities.
# access: read/write

property_dom_node = "http://xml.org/sax/properties/dom-node"
# data type: org.w3c.dom.Node
# description: When parsing, the current DOM node being visited if this is
#              a DOM iterator; when not parsing, the root DOM node for
#              iteration.
# access: (parsing) read-only; (not parsing) read/write

property_xml_string = "http://xml.org/sax/properties/xml-string"
# data type: String
# description: The literal string of characters that was the source for
#              the current event.
# access: read-only

all_properties = [property_lexical_handler,
                  property_dom_node,
                  property_declaration_handler,
                  property_xml_string]
