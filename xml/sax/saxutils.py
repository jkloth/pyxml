"""
A library of useful helper classes to the saxlib classes, for the
convenience of application and driver writers.

$Id: saxutils.py,v 1.9 2000/09/26 14:43:10 loewis Exp $
"""

from xml.utils import escape  # FIXME!
import types, saxlib, string, sys, saxexts, urllib, codecs

# --- DefaultHandler

class DefaultHandler(saxlib.EntityResolver, saxlib.DTDHandler,
                     saxlib.ContentHandler, saxlib.ErrorHandler):
    """Default base class for SAX2 event handlers. Implements empty
    methods for all callback methods, which can be overridden by
    application implementors. Replaces the deprecated SAX1 HandlerBase
    class."""

# --- Location

class Location:
    """Represents a location in an XML entity. Initialized by being passed
    a locator, from which it reads off the current location, which is then
    stored internally."""

    def __init__(self, locator):
	self.__col = locator.getColumnNumber()
	self.__line = locator.getLineNumber()
	self.__pubid = locator.getPublicId()
	self.__sysid = locator.getSystemId()
    
    def getColumnNumber(self):
	return self.__col

    def getLineNumber(self):
	return self.__line

    def getPublicId(self):
	return self.__pubid

    def getSystemId(self):
	return self.__sysid

# --- ErrorPrinter
    
class ErrorPrinter:
    "A simple class that just prints error messages to standard out."

    def __init__(self, level=0, outfile=sys.stderr):
        self._level = level
        self._outfile = outfile
    
    def warning(self, exception):
        if self._level <= 0:
            self._outfile.write("WARNING in %s: %s\n" %
                               (self.__getpos(exception),
                                exception.getMessage()))
        
    def error(self, exception):
        if self._level <= 1:
            self._outfile.write("ERROR in %s: %s\n" %
                               (self.__getpos(exception),
                                exception.getMessage()))

    def fatalError(self, exception):
        if self._level <= 2:
            self._outfile.write("FATAL ERROR in %s: %s\n" % 
                               (self.__getpos(exception),
                                exception.getMessage()))

    def __getpos(self, exception):
        if isinstance(exception, saxlib.SAXParseException):
            return "%s:%s:%s" % (exception.getSystemId(),
                                 exception.getLineNumber(),
                                 exception.getColumnNumber())
        else:
            return "<unknown>"

# --- ErrorRaiser

class ErrorRaiser:
    "A simple class that just raises the exceptions it is passed."

    def __init__(self, level = 0):
        self._level = level
        
    def error(self, exception):
        if self._level <= 1:
            raise exception

    def fatalError(self, exception):
        if self._level <= 2:
            raise exception

    def warning(self, exception):
        if self._level <= 0:
            raise exception

# --- AttributesImpl

class AttributesImpl:

    def __init__(self, attrs, rawnames):
        self._attrs = attrs
        self._rawnames = rawnames

    def getLength(self):
        return len(self._attrs)

    def getType(self, name):
        return "CDATA"

    def getValue(self, name):
        return self._attrs[name]

    def getValueByQName(self, name):
        return self._attrs[self._rawnames[name]]

    def getNameByQName(self, name):
        return self._rawnames[name]

    def getNames(self):
        return self._attrs.keys()

    def getQNames(self):
        return self._rawnames.keys()    
    
    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, name):
        return self._attrs[name]

    def keys(self):
        return self._attrs.keys()

    def has_key(self, name):
        return self._attrs.has_key(name)

    def get(self, name, alternative=None):
        return self._attrs.get(name, alternative)

    def copy(self):
        return self.__class__(self._attrs, self._rawnames)

    def items(self):
        return self._attrs.items()

    def values(self):
        return self._attrs.values()

# --- ContentGenerator, now called XMLGenerator in Python 2
    
class XMLGenerator(saxlib.ContentHandler):

    def __init__(self, out = sys.stdout, encoding = "iso-8859-1"):
        saxlib.ContentHandler.__init__(self)
        writerclass = codecs.lookup(encoding)[3]
        self._out = writerclass(out)
        self._ns_contexts = [{}] # contains uri -> prefix dicts
        self._current_context = self._ns_contexts[-1]
        self._encoding = encoding

    # ContentHandler methods
        
    def startDocument(self):
        self._out.write(u'<?xml version="1.0" encoding="%s"?>\n' %
                        self._encoding)

    def startPrefixMapping(self, prefix, uri):
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[uri] = prefix

    def endPrefixMapping(self, prefix):
        del self._current_context[-1]

    def startElement(self, name, attrs):
        self._out.write(u'<' + name)
        for (name, value) in attrs.items():
            self._out.write(u' %s="%s"' % (name, escape(value)))
        self._out.write(u'>')

    def endElement(self, name):
        self._out.write(u'</%s>' % name)

    def startElementNS(self, name, qname, attrs):
        if qname is None:
            qname = self._current_context[name[0]] + ":" + name[1]
        self._out.write(u'<' + qname)
        for (name, value) in attrs.items():
            name = self._current_context[name[0]] + ":" + name[1]
            self._out.write(u' %s="%s"' % (name, escape(value)))
        self._out.write(u'>')

    def endElementNS(self, name, qname):
        if qname is None:
            qname = self._current_context[name[0]] + ":" + name[1]
        self._out.write(u'</%s>' % qname)

    def characters(self, content):
        self._out.write(escape(content))

    def ignorableWhitespace(self, content):
        self._out.write(content)
        
    def processingInstruction(self, target, data):
        self._out.write(u'<?%s %s?>' % (target, data))

# --- FIXME: remove backwards compatibility name when not needed anymore
ContentGenerator = XMLGenerator

# --- XMLFilterImpl

class XMLFilterBase(saxlib.XMLFilter):
    """This class is designed to sit between an XMLReader and the
    client application's event handlers.  By default, it does nothing
    but pass requests up to the reader and events on to the handlers
    unmodified, but subclasses can override specific methods to modify
    the event stream or the configuration requests as they pass
    through."""

    # ErrorHandler methods

    def error(self, exception):
        self._err_handler.error(exception)

    def fatalError(self, exception):
        self._err_handler.fatalError(exception)

    def warning(self, exception):
        self._err_handler.warning(exception)

    # ContentHandler methods
        
    def setDocumentLocator(self, locator):
        self._cont_handler.setDocumentLocator(locator)
        
    def startDocument(self):
        self._cont_handler.startDocument()

    def endDocument(self):
        self._cont_handler.endDocument()

    def startPrefixMapping(self, prefix, uri):
        self._cont_handler.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix):
        self._cont_handler.endPrefixMapping(prefix)

    def startElement(self, name, attrs):
        self._cont_handler.startElement(name, attrs)

    def endElement(self, name):
        self._cont_handler.endElement(name)

    def startElementNS(self, name, qname, attrs):
        self._cont_handler.startElementNS(name, qname, attrs)

    def endElementNS(self, name, qname):
        self._cont_handler.endElementNS(name, qname)

    def characters(self, content):
        self._cont_handler.characters(content)

    def ignorableWhitespace(self, chars, start, end):
        self._cont_handler.ignorableWhitespace(chars, start, end)

    def processingInstruction(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def skippedEntity(self, name):
        self._cont_handler.skippedEntity(name)

    # DTDHandler methods

    def notationDecl(self, name, publicId, systemId):
        self._dtd_handler.notationDecl(name, publicId, systemId)

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        self._dtd_handler.unparsedEntityDecl(name, publicId, systemId, ndata)

    # EntityResolver methods

    def resolveEntity(self, publicId, systemId):
        self._ent_handler.resolveEntity(publicId, systemId)

    # XMLReader methods

    def parse(self, source):
        self._parent.setContentHandler(self)
        self._parent.setErrorHandler(self)
        self._parent.setEntityResolver(self)
        self._parent.setDTDHandler(self)
        self._parent.parse(source)

    def setLocale(self, locale):
        self._parent.setLocale(locale)
    
    def getFeature(self, name):
        return self._parent.getFeature(name)

    def setFeature(self, name, state):
        self._parent.setFeature(name, state)

    def getProperty(self, name):
        return self._parent.getProperty(name)

    def setProperty(self, name, value):
        self._parent.setProperty(name, value)

# FIXME: remove this backward compatibility hack when not needed anymore
XMLFilterImpl = XMLFilterBase
        
# --- BaseIncrementalParser

class BaseIncrementalParser(saxlib.IncrementalParser):
    """This class implements the parse method of the XMLReader
    interface using the feed, close and reset methods of the
    IncrementalParser interface as a convenience to SAX 2.0 driver
    writers."""

    def parse(self, source):
        source = prepare_input_source(source)
        self.prepareParser(source)

        self._cont_handler.startDocument()

        # FIXME: what about char-stream?
        inf = source.getByteStream()
        buffer = inf.read(16384)
        while buffer != "":
            self.feed(buffer)
            buffer = inf.read(16384)

        self.close()
        self.reset()
        
        self._cont_handler.endDocument()

    def prepareParser(self, source):
        """This method is called by the parse implementation to allow
        the SAX 2.0 driver to prepare itself for parsing."""
        raise NotImplementedError("prepareParser must be overridden!")
        
# --- Utility functions

def prepare_input_source(source):

    if type(source) == types.StringType:
        source = saxlib.InputSource(source)

    try:
        if type(source) == types.UnicodeType:
            source = saxlib.InputSource(source)
    except AttributeError:
        # pre-2.0, no UnicodeType
        pass

    if hasattr(source,"read"):
        # It's a file-like object
        f = source
        source = saxlib.InputSource()
        source.setByteStream(f)

    if source.getByteStream() == None:
        source.setByteStream(urllib.urlopen(source.getSystemId()))
        
    return source
    
# ===========================================================================
#
# DEPRECATED SAX 1.0 CLASSES
#
# ===========================================================================
        
# --- AttributeMap

class AttributeMap:
    """An implementation of AttributeList that takes an (attr,val) hash
    and uses it to implement the AttributeList interface."""    

    def __init__(self, map):
	self.map=map
    
    def getLength(self):
	return len(self.map.keys())
	
    def getName(self, i):
        try:
            return self.map.keys()[i]
        except IndexError,e:
            return None

    def getType(self, i):
	return "CDATA"

    def getValue(self, i):
        try:
            if type(i)==types.IntType:
                return self.map[self.getName(i)]
            else:
                return self.map[i]
        except KeyError,e:
            return None

    def __len__(self):
	return len(self.map)

    def __getitem__(self, key):
	if type(key)==types.IntType:
            return self.map.keys()[key]
	else:
            return self.map[key]

    def items(self):
        return self.map.items()
        
    def keys(self):
	return self.map.keys()

    def has_key(self,key):
	return self.map.has_key(key)
    
    def get(self, key, alternative=None):
        return self.map.get(key, alternative)

    def copy(self):
        return AttributeMap(self.map.copy())

    def values(self):
        return self.map.values()
    
# --- Event broadcasting object

class EventBroadcaster:    
    """Takes a list of objects and forwards any method calls received
    to all objects in the list. The attribute list holds the list and
    can freely be modified by clients."""

    class Event:
        "Helper objects that represent event methods."

        def __init__(self,list,name):
            self.list=list
            self.name=name
        
        def __call__(self,*rest):
            for obj in self.list:
                apply(getattr(obj,self.name), rest)
    
    def __init__(self,list):
        self.list=list

    def __getattr__(self,name):
        return self.Event(self.list,name)

    def __repr__(self):
        return "<EventBroadcaster instance at %d>" % id(self)

# --- ESIS document handler

class ESISDocHandler(saxlib.HandlerBase):
    "A SAX document handler that produces naive ESIS output."

    def __init__(self,writer=sys.stdout):
	self.writer=writer
    
    def processingInstruction (self,target, remainder):
	"""Receive an event signalling that a processing instruction
	has been found."""
	self.writer.write("?"+target+" "+remainder+"\n")

    def startElement(self,name,amap):
	"Receive an event signalling the start of an element."
	self.writer.write("("+name+"\n")
	for a_name in amap.keys():
	    self.writer.write("A"+a_name+" "+amap[a_name]+"\n")

    def endElement(self,name):
	"Receive an event signalling the end of an element."
	self.writer.write(")"+name+"\n")

    def characters(self,data,start_ix,length):
	"Receive an event signalling that character data has been found."
	self.writer.write("-"+data[start_ix:start_ix+length]+"\n")
        
# --- XML canonizer

class Canonizer(saxlib.HandlerBase):
    "A SAX document handler that produces canonized XML output."

    def __init__(self,writer=sys.stdout):
	self.elem_level=0
	self.writer=writer
    
    def processingInstruction (self,target, remainder):
	if not target=="xml":
	    self.writer.write("<?"+target+" "+remainder+"?>")

    def startElement(self,name,amap):
	self.writer.write("<"+name)
	
	a_names=amap.keys()
	a_names.sort()

	for a_name in a_names:
	    self.writer.write(" "+a_name+"=\"")
	    self.write_data(amap[a_name])
	    self.writer.write("\"")
	self.writer.write(">")
	self.elem_level=self.elem_level+1

    def endElement(self,name):
	self.writer.write("</"+name+">")
	self.elem_level=self.elem_level-1

    def ignorableWhitespace(self,data,start_ix,length):
	self.characters(data,start_ix,length)
	
    def characters(self,data,start_ix,length):
	if self.elem_level>0:
            self.write_data(data[start_ix:start_ix+length])
	    
    def write_data(self,data):
	"Writes datachars to writer."
	data=string.replace(data,"&","&amp;")
	data=string.replace(data,"<","&lt;")
	data=string.replace(data,"\"","&quot;")
	data=string.replace(data,">","&gt;")
        data=string.replace(data,chr(9),"&#9;")
        data=string.replace(data,chr(10),"&#10;")
        data=string.replace(data,chr(13),"&#13;")
	self.writer.write(data)
	
# --- mllib

class mllib:
    """A re-implementation of the htmllib, sgmllib and xmllib interfaces as a
    SAX DocumentHandler."""

# Unsupported:
# - setnomoretags
# - setliteral
# - translate_references
# - handle_xml
# - handle_doctype
# - handle_charref
# - handle_entityref
# - handle_comment
# - handle_cdata
# - tag_attributes

    def __init__(self):
        self.reset()

    def reset(self):
        self.parser=saxexts.XMLParserFactory.make_parser()
        self.handler=mllib.Handler(self.parser,self)
        self.handler.reset()

    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()

    def get_stack(self):
        return self.handler.get_stack()

    # --- Handler methods (to be overridden)

    def handle_starttag(self,name,method,atts):
        method(atts)

    def handle_endtag(self,name,method):
        method()
    
    def handle_data(self,data):
        pass

    def handle_proc(self,target,data):
        pass

    def unknown_starttag(self,name,atts):
        pass
    
    def unknown_endtag(self,name):
        pass

    def syntax_error(self,message):
        pass
    
    # --- The internal handler class
      
    class Handler(saxlib.DocumentHandler,saxlib.ErrorHandler):
        """An internal class to handle SAX events and translate them to mllib
        events."""

        def __init__(self,driver,handler):
            self.driver=driver
            self.driver.setDocumentHandler(self)
            self.driver.setErrorHandler(self)
            self.handler=handler
            self.reset()

        def get_stack(self):
            return self.stack

        def reset(self):
            self.stack=[]

        # --- DocumentHandler methods
            
        def characters(self, ch, start, length):
            self.handler.handle_data(ch[start:start+length])

        def endElement(self, name):
            if hasattr(self.handler,"end_"+name):
                self.handler.handle_endtag(name,
                                          getattr(self.handler,"end_"+name))
            else:
                self.handler.unknown_endtag(name)

            del self.stack[-1]

        def ignorableWhitespace(self, ch, start, length):
            self.handler.handle_data(ch[start:start+length])

        def processingInstruction(self, target, data):
            self.handler.handle_proc(target,data)

        def startElement(self, name, atts):
            self.stack.append(name)
            
            if hasattr(self.handler,"start_"+name):
                self.handler.handle_starttag(name,
                                            getattr(self.handler,
                                                    "start_"+name),
                                             atts)
            else:
                self.handler.unknown_starttag(name,atts)
            
        # --- ErrorHandler methods

        def error(self, exception):
            self.handler.syntax_error(str(exception))

        def fatalError(self, exception):
            raise RuntimeError(str(exception))
