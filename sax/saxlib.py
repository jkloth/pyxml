"""A Python translation of the SAX parser API. This file provides only
default classes with absolutely minimum functionality, from which
drivers and applications can be subclassed.

Many of these classes are empty and are included only as documentation
of the interfaces."""

# --- Locator

class Locator:
    """Interface for associating a SAX event with a document
    location. A locator object will return valid results only during
    calls to SAXDocumentHandler methods; at any other time, the
    results are unpredictable."""
    
    def getColumnNumber(self):
        "Return the column number where the current event ends."
        return -1

    def getLineNumber(self):
        "Return the line number where the current event ends."
        return -1

    def getPublicId(self):
        "Return the public identifier for the current event."
        return ""

    def getSystemId(self):
        "Return the system identifier for the current event."
        return ""

# --- SAXException

import sys
if sys.platform[0:4] == 'java':
    from exceptions import Exception

class SAXException(Exception):
    """Encapsulate an XML error or warning. This class can contain
    basic error or warning information from either the XML parser or
    the application: you can subclass it to provide additional
    functionality, or to add localization. Note that although you will
    receive a SAXException as the argument to the handlers in the
    ErrorHandler interface, you are not actually required to throw
    the exception; instead, you can simply read the information in
    it."""
    
    def __init__(self, msg, exception):
        """Creates an exception. The message is required, but the exception
        can be None."""
        self.msg=msg
        self.exception=exception

    def getMessage(self):
        "Return a message for this exception."
        return self.msg

    def getException(self):
        "Return the embedded exception, if any."
        return self.exception

    def __str__(self):
        "Create a string representation of the exception."
        return self.msg

# --- SAXParseException

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
        SAXException.__init__(self,msg,exception)
        self.locator=locator
        
    def getColumnNumber(self):
        """The column number of the end of the text where the exception
        occurred."""
        return self.locator.getColumnNumber()

    def getLineNumber(self):
        "The line number of the end of the text where the exception occurred."
        return self.locator.getLineNumber()

    def getPublicId(self):
        "Get the public identifier of the entity where the exception occurred."
        return self.locator.getPublicId()

    def getSystemId(self):
        "Get the system identifier of the entity where the exception occurred."
        return self.locator.getSystemId()

    def __str__(self):
        "Create a string representation of the exception."
        return "%s at %s:%d:%d" % (self.msg,self.getSystemId(),
                                   self.getLineNumber(),self.getColumnNumber())
    
# --- EntityResolver

class EntityResolver:
    """Basic interface for resolving entities. If you create an object
    implementing this interface, then register the object with your
    Parser, the parser will call the method in your object to
    resolve all external entities. Note that HandlerBase implements
    this interface with the default behaviour."""
    
    def resolveEntity(self, publicId, systemId):
        "Resolve the system identifier of an entity."
        return systemId

# --- ErrorHandler

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
        pass

    def fatalError(self, exception):
        "Handle a non-recoverable error."
        pass

    def warning(self, exception):
        "Handle a warning."
        pass

# --- AttributeList

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
        pass

    def getName(self, i):
        "Return the name of an attribute in the list."
        pass

    def getType(self, i):
        """Return the type of an attribute in the list. (Parameter can be
        either integer index or attribute name.)"""
        pass

    def getValue(self, i):
        """Return the value of an attribute in the list. (Parameter can be
        either integer index or attribute name.)"""
        pass

    def __len__(self):
        "Alias for getLength."
        pass

    def __getitem__(self, key):
        "Alias for getName (if key is an integer) and getValue (if string)."
        pass

    def keys(self):
        "Returns a list of the attribute names."
        pass

    def has_key(self, key):
        "True if the attribute is in the list, false otherwise."
        pass

# --- DTDHandler

class DTDHandler:
    """Handle DTD events. This interface specifies only those DTD
    events required for basic parsing (unparsed entities and
    attributes). If you do not want to implement the entire interface,
    you can extend HandlerBase, which implements the default
    behaviour."""

    def notationDecl(self, name, publicId, systemId):
        "Handle a notation declaration event."
        pass

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        "Handle an unparsed entity declaration event."
        pass

# --- DocumentHandler

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
        pass

    def endDocument(self):
        "Handle an event for the end of a document."
        pass

    def endElement(self, name):
        "Handle an event for the end of an element."
        pass

    def ignorableWhitespace(self, ch, start, length):
        "Handle an event for ignorable whitespace in element content."
        pass

    def processingInstruction(self, target, data):
        "Handle a processing instruction event."
        pass

    def setDocumentLocator(self, locator):
        "Receive an object for locating the origin of SAX document events."
        pass

    def startDocument(self):
        "Handle an event for the beginning of a document."
        pass

    def startElement(self, name, atts):
        "Handle an event for the beginning of an element."
        pass

# --- Parser

class Parser:
    """Basic interface for SAX (Simple API for XML) parsers. All SAX
    parsers must implement this basic interface: it allows users to
    register handlers for different types of events and to initiate a
    parse from a URI, a character stream, or a byte stream. SAX
    parsers should also implement a zero-argument constructor."""

    def __init__(self):
        self.doc_handler=DocumentHandler()
        self.dtd_handler=DTDHandler()
        self.ent_handler=EntityResolver()
        self.err_handler=ErrorHandler()

    def parse(self, systemId):
        "Parse an XML document from a system identifier."
        pass

    def parseFile(self, fileobj):
        "Parse an XML document from a file-like object."
        pass

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
        raise SAXException("Locale support not implemented",None)

# --- HandlerBase

class HandlerBase(EntityResolver, DTDHandler, DocumentHandler,\
                     ErrorHandler):
    """Default base class for handlers. This class implements the
    default behaviour for four SAX interfaces: EntityResolver,
    DTDHandler, DocumentHandler, and ErrorHandler: rather
    than implementing those full interfaces, you may simply extend
    this class and override the methods that you need. Note that the
    use of this class is optional (you are free to implement the
    interfaces directly if you wish)."""

    def __init__(self):
        pass
