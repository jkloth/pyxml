
from generic import *

# XXX how to marshal iso8601 dates?

# XML-RPC, like WDDX, has a Boolean type.  We need to generate such
# variables, so this defines a class representing a truth value, and
# then creates TRUE and FALSE.

class TruthValue:
    def __init__(self, value): self.value = value
    def __nonzero__(self): return self.value
    
TRUE = TruthValue(1)
FALSE = TruthValue(0)

class XMLRPCMarshaller(Marshaller):
    tag_root = "methodCall"
    tag_int = 'int'
    tag_float = 'double'

    def m_instance(self, value, dict):
        if value not in [TRUE, FALSE]:
            self.m_unimplemented(value, dict)
        if value is TRUE: return ['<boolean>1</boolean>']
        else: return ['<boolean>0</boolean>']

    def m_list(self, value, dict):
        L = []
        i = str(id(value)) ; dict[ i ] = 1
        L.append( '<array><data>' )
        for elem in value:
            L = L + ['<value>'] + self._marshal(elem, dict) + ['</value>']
        L.append( '</data></array>')
        return L

    m_tuple = m_list
    
    def m_dictionary(self, value, dict):
        L = []
        i = str( id(value) ) ; dict[ i ] = 1
        L.append( '<struct>' )
        for key, v in value.items():
            assert type(key) == type("")
            L = L + ['<member><name>' + key + '</name>']
            L = L + ['<value>'] + self._marshal(v, dict) + ['</value></member>']
        L.append( '</struct>')
        return L

class XMLRPCUnmarshaller(Unmarshaller):
    unmarshal_meth = {
        'methodCall': ('um_start_root', None),
        'i4': ('um_start_int', 'um_end_int'),
        'int': ('um_start_int', 'um_end_int'),
        'boolean': ('um_start_boolean', 'um_end_boolean'),
        'string': ('um_start_string', 'um_end_string'),
        'name': ('um_start_string', 'um_end_string'),
        'double': ('um_start_float', 'um_end_float'),
        'datetime.iso8601': ('um_start_iso8601', 'um_end_iso8601'),
        'array': ('um_start_list', 'um_end_list'),
        'value': ('um_start_ignore', 'um_end_ignore'),
        'data': ('um_start_ignore', 'um_end_ignore'),
        'member': ('um_start_ignore', 'um_end_ignore'),
        'struct': ('um_start_dictionary', 'um_end_dictionary'),
        }
    
    um_start_boolean = Unmarshaller.um_start_generic
    def um_end_boolean(self, name):
        ds = self.data_stack
        if ds[-1][0]=='1': ds[-1] = TRUE
        else: ds[-1] = FALSE

    # Some elements in XML-RPC are redundant
    def um_start_ignore(self, name, attrs): pass
    def um_end_ignore(self, name): pass

    def um_end_member(self, name, attrs):
        # Take the top two items off the stack (a string and something else),
        # turn them into a tuple, and put them back.
        ds = self.data_stack
        self.ds[-2:] = [ (self.ds[-2], self.ds[-1] ) ]

    um_start_iso8601 = Unmarshaller.um_start_generic
    def um_end_iso8601(self, name):
        from xml.utils import iso8601
        ds = self.data_stack
        date = string.join( ds[-1], "")
        ds[-1] = iso8601.parse( date )

    def um_end_dictionary(self, name):
        ds = self.data_stack
        for index in range(len(ds)-1, -1, -1):
            if ds[index] is DICT: break
        assert index!=-1
        d = ds[index+1]
        print ds[index+2:]
        for i in range(index+2, len(ds), 2):
            key = ds[i] ; value =ds[i+1]
            d[key] = value
        ds[index:] = [ d ]

        
_m = XMLRPCMarshaller()
dump = _m.dump ; dumps = _m.dumps
_um = XMLRPCUnmarshaller()
load = _um.load ; loads = _um.loads

if __name__ == '__main__':
    print "Testing XML-RPC marshalling..."
    test(load, loads, dump, dumps,
         [TRUE, FALSE, 1, 19.72,  
          "here is a string & a <fake tag>",
          [12, 'Egypt', FALSE, -31],
#          ('alpha', 'beta', 'gamma', 5),
          {'lowerBound':18, 'upperBound': 139,
           'eggs':['rhode island red', 'bantam']}
         ]
        )


