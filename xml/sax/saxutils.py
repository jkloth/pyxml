"""A library of useful subclasses to the saxlib classes, for the
convenience of application and driver writers."""

import types,saxlib,string,sys,saxexts

# --- Location

class Location:
    """Represents a location in an XML entity. Initialized by being passed
    a locator, from which it reads off the current location, which is then
    stored internally."""

    def __init__(self, locator):
	self.__col=locator.getColumnNumber()
	self.__line=locator.getLineNumber()
	self.__pubid=locator.getPublicId()
	self.__sysid=locator.getSystemId()
    
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

    def __init__(self,level=0,outfile=sys.stderr):
        self.level=level
        self.outfile=outfile
    
    def error(self, exception):
        if self.level>1:
            return
        
	self.outfile.write("ERROR in %s: %s\n" % (self.__getpos(exception),\
                                                  exception.getMessage()))

    def fatalError(self, exception):
        if self.level>2:
            return
        
	self.outfile.write("FATAL ERROR in %s: %s\n" % \
                           (self.__getpos(exception),exception.getMessage()))

    def warning(self, exception):
        if self.level>0:
            return
        
	self.outfile.write("WARNING in %s: %s\n" % (self.__getpos(exception),\
                                                    exception.getMessage()))

    def __getpos(self, exception):
	return "%s:%s:%s" % (exception.getSystemId(),\
			     exception.getLineNumber(),\
			     exception.getColumnNumber())

# --- ErrorRaiser

class ErrorRaiser:
    "A simple class that just raises the exceptions it is passed."

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception

    def warning(self, exception):
        raise exception
    
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
	return len(self.map.keys())

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

# ESIS document handler

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

    def endDocument(self):
        try:
            pass
            # self.writer.close()
        except NameError:
            pass # It's OK, if the method isn't there we probably don't need it
        
# XML canonizer

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
	
    def endDocument(self):
        try:
            pass #self.writer.close()
        except NameError:
            pass # It's OK, if the method isn't there we probably don't need it

# --- mllib

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

class mllib:
    """A re-implementation of the htmllib, sgmllib and xmllib interfaces as a
    SAX DocumentHandler."""

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
