
from generic import *

# WDDX has a Boolean type.  We need to generate such variables, so
# this defines a class representing a truth value, and then creates
# TRUE and FALSE.

class TruthValue:
    def __init__(self, value): self.value = value
    def __nonzero__(self): return self.value
    def __repr__(self):
        if self.value: return "<TruthValue instance: True>" 
        else: return "<TruthValue instance: False>" 

TRUE = TruthValue(1)
FALSE = TruthValue(0)

RECORDSET = {}
import UserDict
class RecordSet(UserDict.UserDict):
    def __init__(self, fields, *lists):
	UserDict.UserDict.__init__(self)	
        if len(fields) != len(lists):
	    raise ValueError, "Number of fields and lists must be the same"
        for L in lists[1:]:
            if len(L) != len(lists[0]): 
                raise ValueError, "Number of entries in each list must be the same"
	self.fields = fields
	for i in range(len(fields)):
            f = fields[i] ; L = lists[i]
	    self.data[ f ] = L

class WDDXMarshaller(Marshaller):
    DTD = '<!DOCTYPE wddxPacket SYSTEM "wddx_0090.dtd">'
    tag_root = 'wddxPacket'
    tag_float = tag_int = tag_long = 'number'
    tag_instance = 'boolean'
    wddx_version = "0.9"

    m_reference = m_tuple = Marshaller.m_unimplemented
    m_dictionary = m_None = m_code = Marshaller.m_unimplemented
    m_complex = Marshaller.m_unimplemented
    
    def m_root(self, value, dict):
        return ['<%s version="%s">' % (self.tag_root, self.wddx_version) ]

    def m_instance(self, value, dict):
        if isinstance(value, RecordSet):
            return self.m_recordset(value, dict)

        if value not in [TRUE, FALSE]:
            self.m_unimplemented(value, dict)
        if value is TRUE: return ['<boolean value="true"/>']
        elif value is FALSE: return ['<boolean value="false"/>']

    def m_recordset(self, value, dict):
        L = ['<recordSet rowCount="%i" fieldNames="%s">' % 
	     (len(value), string.join( value.fields, ',') )]
        for f in value.fields:
            recs = value[f]
            L.append('<field name="%s">' % (f))
            for r in recs: L = L + self._marshal(r, dict)
            L.append('</field>')

	L.append('</recordSet>')
	return L
	     
    def m_list(self, value, dict):
        L = []
        i = str(id(value)) ; dict[ i ] = 1
        L.append( '<array length="%i">' % (len(value),))
        for elem in value:
            L = L + self._marshal(elem, dict)
        L.append( '</array>')
        return L
    m_tuple = m_list

    def m_dictionary(self, value, dict):
        L = []
        i = str( id(value) ) ; dict[ i ] = 1
        L.append( '<struct>' )
        for key, v in value.items():
	    L.append('<var name="%s">' % ( key,) )
            L = L + self._marshal(v, dict)
	    L.append('</var>')
        L.append( '</struct>')
        return L


class WDDXUnmarshaller(Unmarshaller):
    unmarshal_meth = {
        'wddxPacket': ('um_start_root', None),
        'boolean': ('um_start_boolean', 'um_end_boolean'),
        'number': ('um_start_number', 'um_end_number'),
        'string': ('um_start_string', 'um_end_string'),
        'array': ('um_start_list', 'um_end_list'),
        'struct': ('um_start_dictionary', 'um_end_dictionary'),
        'var': ('um_start_var', None),
        'recordSet': ('um_start_recordset', 'um_end_recordset'),
        'field': ('um_start_field', 'um_end_field'),
        }

    def um_start_boolean(self, name, attrs):
        v = attrs['value']
        self.data_stack.append( [v] )

    def um_end_boolean(self, name):
        ds = self.data_stack
        if ds[-1][0]=='true': ds[-1] = TRUE
        else: ds[-1] = FALSE

    um_start_number = Unmarshaller.um_start_generic
    um_end_number = Unmarshaller.um_end_float 

    def um_start_var(self, name, attrs):
        name = attrs['name']
        self.data_stack.append( name )

    def um_start_recordset(self, name, attrs):
        fields = string.split( attrs['fieldNames'], ',')
        rowCount = int( attrs['rowCount'] )
        self.data_stack.append( RECORDSET )
        self.data_stack.append( (rowCount,fields) )
    def um_end_recordset(self, name):
        ds = self.data_stack
        for index in range(len(ds)-1, -1, -1):
            if ds[index] is RECORDSET: break
        assert index!=-1
        rowCount, fields = ds[index+1]
	lists = [None] * len(fields)
        for i in range(index+2, len(ds), 2):
            field = ds[i] ; value = ds[i+1]
            pos = fields.index( field )
            lists[ pos ] = value
        ds[index:] = [ apply(RecordSet, tuple([fields]+lists) ) ]

    def um_start_field(self, name, attrs):
        field = attrs['name']
        self.data_stack.append( field )
        self.data_stack.append(LIST)
        self.data_stack.append( [] )
    um_end_field = Unmarshaller.um_end_list

_m = WDDXMarshaller()
dump = _m.dump ; dumps = _m.dumps
_um = WDDXUnmarshaller()
load = _um.load ; loads = _um.loads
    
def runtests():
    print "Testing WDDX marshalling..."
    recordset = RecordSet( ['NAME', 'AGE'],
	                   ['John Doe', 'Jane Doe'],
	                   [34, 31] )
    test(load, loads, dump, dumps,
         [TRUE, FALSE, 1, pow(2,123L), 19.72,  
          "here is a string & a <fake tag>",
	  [1,2,3,"foo"], recordset,
          {'lowerBound':18, 'upperBound': 139,
           'eggs':['rhode island red', 'bantam']},
	  {'s': 'a string',
	   'obj':{'s':'a string', 'n':-12.456},
	   'n': -12.456, 'b':TRUE, 'a': [10,'second element'],
	  }
         ]
        )

    test(load, loads, dump, dumps,
	 [(1,3,"five",7)], do_assert=0
	)

if __name__ == '__main__':
    runtests()
