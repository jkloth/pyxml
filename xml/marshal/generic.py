
# Generic class for marshalling simple Python data types into an XML-based
# format.  The interface is the same as the built-in module of the
# same name, with four functions: 
#   dump(value, file), load(file)
#   dumps(value), loads(string)

from types import *
import string
from xml.sax import saxlib

# These values are used as markers in the stack when unmarshalling
# one of the structures below.  When a <tuple> tag is encountered, for
# example, the TUPLE object is pushed onto the stack, and further
# objects are processed.  When the </tuple> tag is found, the code
# looks back into the stack until TUPLE is found; all the higher
# objects are then collected into a tuple.  Ditto for lists...
 
TUPLE = {} ; LIST = {} ; DICT = {}

# Basic marshaller class, customizable by overriding it and
# changing various attributes and methods.
# It's also used as a SAX handler, which may be a good idea but may
# also be a stupid hack.

class Marshaller(saxlib.HandlerBase):
    # XML version and DOCTYPE declaration
    PROLOGUE = '<?xml version="1.0"?>'
    DTD = ""

    # Names of elements.  These are specified as class attributes
    # because simple things like integers are often handled in the
    # same way, and only the element names change.
    tag_root = 'marshal'
    tag_int = 'int'
    tag_float = 'float'
    tag_long = 'long'
    tag_string = 'string'
    tag_tuple = 'tuple'
    tag_list = 'list'
    tag_dictionary = 'dictionary'
    tag_complex = 'complex'
    tag_reference = 'reference'
    tag_code = 'code'
    tag_none = 'none'

    # This dictionary maps element names to the names of starting and ending
    # functions to call when unmarshalling them.  My convention is to
    # name them um_start_foo and um_end_foo, but do whatever you like.
    
    unmarshal_meth = {
        'marshal': ('um_start_root', 'um_end_root'),
        'int': ('um_start_int', 'um_end_int'),
        'float': ('um_start_float', 'um_end_float'),
        'long': ('um_start_long', 'um_end_long'),
        'string': ('um_start_string', 'um_end_string'),
        'tuple': ('um_start_tuple', 'um_end_tuple'),
        'list': ('um_start_list', 'um_end_list'),
        'dictionary': ('um_start_dictionary', 'um_end_dictionary'),
        'complex': ('um_start_complex', 'um_end_complex'),
        'reference': ('um_start_reference', 'um_end_reference'),
        'code': ('um_start_code', 'um_end_code'),
        'none': ('um_start_none', 'um_end_none'),
        }

    def __init__(self):
        saxlib.HandlerBase.__init__(self)

        # Find the named methods, and convert them to the actual
        # method object.
        d = {}
        for key, (sm, em) in self.unmarshal_meth.items():
            meth1 = meth2 = None
            if hasattr(self, sm): meth1 = getattr(self, sm)
            if hasattr(self, em): meth2 = getattr(self, em)
            d[ key ] = meth1, meth2
        self.unmarshal_meth = d

    # The four basic functions that form the caller's interface
    def dump(self, value, file):
        "Write the value on the open file"
        L = self._marshal(value, {} )
        L = ( [self.PROLOGUE + self.DTD + '<' + self.tag_root + '>'] +
              L +
              ['</' + self.tag_root + '>'] )
        
        # XXX should this just loop through the L and call file.write
        # for each item?
        file.write( string.join(L, "") )

    def dumps(self, value):
        "Marshal value, returning the resulting string"
        L = self._marshal(value, {} )
        L = ( [self.PROLOGUE + self.DTD + '<' + self.tag_root + '>'] +
              L +
              ['</' + self.tag_root + '>'] )
        return string.join(L, "") 

    def load(self, file):
        "Unmarshal one value, reading it from a file-like object"
        # Instatiate a new object; unmarshalling isn't thread-safe
        # because it modifies attributes on the object.
        m = self.__class__()
        return m._load(file)

    def loads(self, string):
        "Unmarshal one value from a string"
        # Instatiate a new object; unmarshalling isn't thread-safe
        # because it modifies attributes on the object.
        m = self.__class__()
        import StringIO
        file = StringIO.StringIO(string)
        return m._load(file)

    # Entry point for marshalling.  This function gets the name of the 
    # type of the object being marshalled, and calls the
    # m_<typename> method.  This method must return a list of strings,
    # which will be returned to the caller.
    #
    # (This function can be called recursively, so it shouldn't
    # return just a single.  The top-level caller will perform a
    # single string.join to get the resulting XML document.
    # 
    # dict is a dictionary whose keys are used to store the IDs of
    # objects that have already been marshalled, in order to allow
    # writing a reference to them.
    #
    # XXX there should be some way to disable the automatic generation of
    # references to already-marshalled objects

    def _marshal(self, value, dict):
        t = type(value) ; i = str( id(value) )
        if dict.has_key( i ):
            return self.m_reference( value, dict ) 
        else:
            if type(value) == type(1L): meth = 'm_long'
            else: meth = "m_" + type(value).__name__
            return getattr(self,meth)(value, dict) 

    # Utility function, used for types that aren't implemented
    def m_unimplemented(self, value, dict):
        raise ValueError, ("Marshalling of object " + repr(value) +
                           " unimplemented or not supported in this DTD")

    #
    # All the generic marshalling functions for various Python types
    #
    def m_reference(self, value, dict):
        # This object has already been marshalled, so
        # emit a reference element.
        i = str( id(value) )
        return [ '<' + self.tag_reference + ' id="i%s"/>' % (i, ) ]

    def m_string(self, value, dict):
        name = self.tag_string
        L = [ '<' + name + '>' ]
        s = str(value)
        if '&' in s or '>' in s or '<' in s:
            s = string.replace(s, '&', '&amp;')
            s = string.replace(s, '<', '&lt;')
            s = string.replace(s, '>', '&gt;')
        L.append( s )
        L.append( '</' + name + '>')
        return L
    
    def m_int(self, value, dict):
        name = self.tag_int ; L = []
        L.append( '<' + name + '>' + str(value) + '</' + name + '>' )
        return L

    def m_float(self, value, dict):
        name = self.tag_float ; L = []
        L.append( '<' + name + '>' + str(value) + '</' + name + '>' )
        return L

    def m_long(self, value, dict):
        name = self.tag_long ; L = []
        L.append( '<' + name + '>' + str(value)[:-1] + '</' + name + '>' )
        return L

    def m_tuple(self, value, dict):
        name = self.tag_tuple ; L = []
        i = str(id(value))
        dict[ i ] = 1
        L.append( '<' + name + ' id="i%s">' % (i,))
        for elem in value:
            L = L + self._marshal(elem, dict)
        L.append( '</' + name + '>')
        return L

    def m_list(self, value, dict):
        name = self.tag_list ; L = []
        i = str(id(value))
        dict[ i ] = 1
        L.append( '<' + name + ' id="i%s">' % (i,))
        for elem in value:
            L = L + self._marshal(elem, dict)
        L.append( '</' + name + '>')
        return L

    def m_dictionary(self, value, dict):
        name = self.tag_dictionary ; L = []
        i = str( id(value) )
        dict[ i ] = 1
        L.append( '<' + name + ' id="i%s">' %(i,) )
        for key, v in value.items():
            L = L + self._marshal(key, dict)
            L = L + self._marshal(v, dict)
        L.append( '</' + name + '>')
        return L

    def m_None(self, value, dict):
        return ['<' + self.tag_none + '/>']

    def m_complex(self, value, dict):
        name = self.tag_complex ; L = []
        return [ '<' + name + '>' + str(value.real) + ' ' + str(value.imag)
                 + '</' + name + '>' ]

    def m_code(self, value, dict):
        name = self.tag_code ; L = []

        # The full information about code objects is only available
        # from the C level, so we'll use the built-in marshal module
        # to convert the code object into a string, and include it in
        # the HTML.
        import marshal, base64
        L.append( '<code>' )
        s = marshal.dumps(value)
        s = base64.encodestring(s)
        L.append( s )
        L.append( '</code>' )
        i = str( id(value) )
        return L

    # Basic unmarshalling routine; it creates a SAX XML parser,
    # registers self as the SAX handler, parses it, and returns
    # the only thing on the data stack.
    
    def _load(self, file):
        "Read one value from the open file"
        from xml.sax import saxexts
        p=saxexts.make_parser()
        p.setDocumentHandler(self)
        p.parseFile(file)
        assert len(self.data_stack) == 1
        return self.data_stack[0]
    
    # SAXlib handler methods.
    #
    # Unmarshalling is done by creating a stack (a Python list) on
    # starting the root element.  When the .character() method may be
    # called, the last item on the stack must be a list; the
    # characters will be appended to that list.
    #
    # The starting methods must, at minimum, push a single list onto
    # the stack, as um_start_generic does.
    #
    # The ending methods can then do string.join() on the list on the
    # top of the stack, and convert it to whatever Python type is
    # required.  The resulting Python object then replaces the list on 
    # the top of the stack.
    # 
        
    def startElement(self, name, attrs):
        # Call the start unmarshalling method, if specified
        sm, em = self.unmarshal_meth[ name ]
        if sm is not None: return sm(name,attrs)

    def characters(self, ch, start, length):
        self.data_stack[-1].append(ch[start:start+length])

    def endElement(self, name):
        # Call the ending method
        sm, em = self.unmarshal_meth[ name ]
        if em is not None: em(name)

    def um_start_root(self, name, attrs):
	self.dict = {}
	self.data_stack = []

    def um_start_reference(self, name, attrs):
	assert attrs.has_key('id')
        id = attrs['id']
        assert self.dict.has_key(id)
        self.data_stack.append( self.dict[id] )

    def um_start_generic(self, name, attrs):
        self.data_stack.append( [] )

    um_start_float = um_start_long = um_start_string = um_start_generic
    um_start_complex = um_start_code = um_start_none = um_start_generic
    um_start_int = um_start_generic
    
    def um_end_string(self, name):
        ds = self.data_stack
        ds[-1] = string.join(ds[-1], "")

    def um_end_int(self, name):
        ds = self.data_stack
        ds[-1] = string.join(ds[-1], "")
        ds[-1] = string.atoi( ds[-1] )

    def um_end_long(self, name):
        ds = self.data_stack
        ds[-1] = string.join(ds[-1], "")
        ds[-1] = string.atol( ds[-1] )

    def um_end_float(self, name):
        ds = self.data_stack
        ds[-1] = string.join(ds[-1], "")
        ds[-1] = string.atof( ds[-1] )

    def um_end_none(self, name):
        ds = self.data_stack
        ds[-1] = None

    def um_end_complex(self, name):
        ds = self.data_stack
        c = string.join(ds[-1], "")
        c = string.split(c)
        c = float(c[0]) + float(c[1])*1j
        ds[-1:] = [c]

    def um_end_code(self, name):
        import marshal, base64
        ds = self.data_stack
        s = string.join(ds[-1], "")
        s = base64.decodestring( s )
        ds[-1] = marshal.loads(s)

    # Trickier stuff: dictionaries, lists, tuples.
    def um_start_list(self, name, attrs):
        self.data_stack.append(LIST)
        L = []
        if attrs.has_key('id'):
            id = attrs[ 'id']
            self.dict[ id ] = L
        self.data_stack.append( L )

    def um_end_list(self, name):
        ds = self.data_stack
        for index in range(len(ds)-1, -1, -1):
            if ds[index] is LIST: break
        assert index!=-1
        L = ds[index+1]
        L[:] = ds[index+2 : len(ds)]
        ds[index:] = [ L ]

    def um_start_tuple(self, name, attrs):
        self.data_stack.append(TUPLE)

    def um_end_tuple(self, name):
        ds = self.data_stack
        for index in range(len(ds)-1, -1, -1):
            if ds[index] is TUPLE: break
        assert index!=-1
        t = tuple( ds[index+1 : len(ds)] )
        ds[index:] = [ t ]

    # Dictionary elements, in the generic format, must always have an
    # even number of objects contained inside them.  These objects are
    # treated as alternating keys and values.
    def um_start_dictionary(self, name, attrs):
        self.data_stack.append(DICT)
        d = {}
        if attrs.has_key('id'):
            id = attrs[ 'id']
            self.dict[ id ] = d
        self.data_stack.append( d )

    def um_end_dictionary(self, name):
        ds = self.data_stack
        for index in range(len(ds)-1, -1, -1):
            if ds[index] is DICT: break
        assert index!=-1
        d = ds[index+1]
        for i in range(index+2, len(ds), 2):
            key = ds[i] ; value =ds[i+1]
            d[key] = value
        ds[index:] = [ d ]


_m = Marshaller()
dump = _m.dump ; dumps = _m.dumps
load = _m.load ; loads = _m.loads


def test(load, loads, dump, dumps, test_values,
         do_assert = 1):
    # Try all the above bits of data
    import StringIO

    for item in test_values:
	s = dumps(item)
        print item, s
	output = loads(s)
	# Try it from a file
	file = StringIO.StringIO()
	dump(item, file)
	file.seek(0)
	output2 = load(file)

##        print repr(item)
##         print repr(output)
##         print repr(output2)
        if do_assert:
            assert item==output and item==output2 and output==output2


if __name__ == '__main__':
    print "Testing XML marshalling..."
    L = [None, 1, pow(2,123L), 19.72, 1+5j, 
         "here is a string & a <fake tag>",
         (1,2,3), 
         ['alpha', 'beta', 'gamma'],
         {'key':'value', 1:2}, 
         test.func_code ]
    test(load, loads, dump, dumps, L)

    recursive_list = [None, 1, pow(3,65L), {1:'spam', 2:'eggs'},
	              '<fake tag>', 1+5j]
    recursive_list.append( recursive_list )
    test(load, loads, dump, dumps, [ recursive_list ], do_assert=0)
