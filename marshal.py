# xml.marshal : Marshals simple Python data types into an XML-based
# format.  The interface is the same as the built-in module of the
# same name, with four functions: 
#   dump(value, file), load(file)
#   dumps(value), loads(string)

from types import *
import string

__dtd__ = """
<!ELEMENT marshal (integer | string | float | long | complex | code | none 
                     | tuple | list | dictionary)>
<!ELEMENT none EMPTY>
<!ELEMENT reference EMPTY>
<!ELEMENT integer (#PCDATA)>
<!ELEMENT string (#PCDATA)>
<!ELEMENT float (#PCDATA)>
<!ELEMENT long (#PCDATA)>
<!ELEMENT code (#PCDATA)>

<!ELEMENT complex (float, float)>
<!ELEMENT tuple (integer | string | float | long | complex | code | none
                     | tuple | list | dictionary | reference)*>
<!ELEMENT list (integer | string | float | long | complex | code | none
                     | tuple | list | dictionary | reference)*>
<!ELEMENT dictionary ( 
  (integer | string | long | float | complex | code | tuple | reference ),
  (integer | string | float | long | complex | code | none
                     | tuple | list | dictionary | reference) )* >

<!ATTLIST list id ID #REQUIRED>
<!ATTLIST dictionary id ID #REQUIRED>
<!ATTLIST reference id IDREF #REQUIRED>
"""

# Dictionary mapping some of the simple types to the corresponding tag
_mapping = {StringType:'string', IntType:'integer', 
	   FloatType:'float'}

# XML version and DOCTYPE declaration
PROLOGUE = """<?xml version="1.0"?>
<!DOCTYPE marshal SYSTEM "marshal.dtd">
"""

def _marshal(value, dict):
    L = []
    t = type(value) ; i = str( id(value) )
    if dict.has_key( i ):
        # This object has already been marshalled, so
        # emit a reference element.
        L.append( '<reference id="i%s"/>' % (i, ) )            

    elif _mapping.has_key( t ):
        # Some simple type: integer, string, or float
	name = _mapping[t]
        L.append( '<'+name + '>')
        s = str(value)
        if '&' in s or '>' in s or '<' in s:
            s = string.replace(s, '&', '&amp;')
            s = string.replace(s, '<', '&lt;')
            s = string.replace(s, '>', '&gt;')
	L.append( s )
	L.append( '</' + name + '>')
        
    elif t == LongType:
	L.append('<long>%s</long>' % (str(value)[:-1],) )

    elif t == TupleType:
	L.append( '<tuple>')
	for elem in value:
            L = L + _marshal(elem, dict)
	L.append( '</tuple>')

    elif t == ListType:
        dict[ i ] = 1
	L.append( '<list id="i%s">' %(i,) )
	for elem in value:
            L = L + _marshal(elem, dict)
	L.append( '</list>')

    elif t == DictType:
        dict[ i ] = 1
	L.append( '<dictionary id="i%s">' %(i,) )
	for key, v in value.items():
	    L = L + _marshal(key, dict)
	    L = L + _marshal(v, dict)
	L.append( '</dictionary>')

    elif t == NoneType:
	L.append( '<none/>')

    elif t == ComplexType:
        # XXX should it be <complex><real>...</real><imag>...</imag></complex>?
        L.append( '<complex><float>' )

	L.append( str(value.real) )
        L.append( '</float><float>' )
	L.append( str(value.imag) )
        L.append( '</float>' )

        L.append( '</complex>' )

    elif t == CodeType:
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
        dict[ i ] = 'code'

    return L

from xml.sax import saxlib
DICT = 'dict' ; LIST = 'list' ; TUPLE='tuple'

class _unmarshalHandler(saxlib.HandlerBase):
    def __init__(self):
        saxlib.HandlerBase.__init__(self)
        
    def startElement(self, name, attrs):
        if name == 'marshal':
            self.dict = {}
            self.data_stack = []
            return
        elif name == 'reference':
            assert attrs.has_key('id')
            id = attrs['id']
            assert self.dict.has_key(id)
            self.data_stack.append( self.dict[id] )
        
        if name=='dictionary':
            self.data_stack.append(DICT)
            d = {}
            id = attrs[ 'id']
            self.dict[ id ] = d
            self.data_stack.append( d )
        elif name=='list':
            self.data_stack.append(LIST)
            L = []
            id = attrs[ 'id']
            self.dict[ id ] = L
            self.data_stack.append( L )
        elif name=='tuple':
            self.data_stack.append(TUPLE)
        else:
            self.data_stack.append( [] )

    def characters(self, ch, start, length):
        self.data_stack[-1].append(ch[start:start+length])

    def endElement(self, name):
        ds = self.data_stack
        if name == 'string':
            ds[-1] = string.join(ds[-1], "")
        elif name == 'integer':
            ds[-1] = string.join(ds[-1], "")
            ds[-1] = string.atoi( ds[-1] )
        elif name == 'long':
            ds[-1] = string.join(ds[-1], "")
            ds[-1] = string.atol( ds[-1] )
        elif name == 'float':
            ds[-1] = string.join(ds[-1], "")
            ds[-1] = string.atof( ds[-1] )
        elif name == 'none':
            ds[-1] = None
        elif name == 'complex':
            c = ds[-2] + ds[-1]*1j
            ds[-3:] = [c]
        elif name == 'code':
            import marshal, base64
            s = string.join(ds[-1], "")
            s = base64.decodestring( s )
            ds[-1] = marshal.loads(s)
        elif name == 'dictionary':
            for index in range(len(ds)-1, -1, -1):
                if ds[index] is DICT: break
            assert index!=-1
            d = ds[index+1]
            for i in range(index+2, len(ds), 2):
                key = ds[i] ; value =ds[i+1]
                d[key] = value
            ds[index:] = [ d ]
            
        elif name == 'list':
            for index in range(len(ds)-1, -1, -1):
                if ds[index] is LIST: break
            assert index!=-1
            L = ds[index+1]
            
            L[:] = ds[index+2 : len(ds)]
            ds[index:] = [ L ]
        elif name == 'tuple':
            for index in range(len(ds)-1, -1, -1):
                if ds[index] is TUPLE: break
            assert index!=-1
            t = tuple( ds[index+1 : len(ds)] )
            ds[index:] = [ t ]
            
            
def dump(value, file):
    "Write the value on the open file"
    L = _marshal(value, {} )
    L = [PROLOGUE + '<marshal>'] + L + ['</marshal>']
    file.write( string.join(L, "") )

def load(file):
    "Read one value from the open file"
    h = _unmarshalHandler()
    from xml.sax import saxexts
    p=saxexts.make_parser()
    p.setDocumentHandler(h)
    p.parseFile(file)
    return h.data_stack[0]
    
def dumps(value):
    "Marshal value, returning the resulting string"
    L = _marshal(value, {} )
    L = [PROLOGUE + '<marshal>'] + L + ['</marshal>']
    return string.join(L, "")

def loads(string):
    "Read one value from the string"
    import StringIO
    file = StringIO.StringIO(string)
    return load(file)

if __name__ == '__main__':
    print "Testing XML marshalling..."
    L=[None, 1, pow(2,123L), 19.72, 1+5j, 
       "here is a string & a <fake tag> ",
       (1,2,3), 
       ['alpha', 'beta', 'gamma'],
       {'key':'value', 1:2}, 
       dumps.func_code ]

    # Try all the above bits of data
    import StringIO

    for item in L + [ L ]:
	s = dumps(item)
        print s
	output = loads(s)
	# Try it from a file
	file = StringIO.StringIO()
	dump(item, file)
	file.seek(0)
	output2 = load(file)

        print repr(item)
        assert item==output and item==output2 and output==output2

    recursive_list = [None, 1, pow(3,65L), '<fake tag>', 1+5j]
    recursive_list.append( recursive_list )
    s = dumps(recursive_list)
    print s
    output = loads(s)
    print repr(output)

   
