
from generic import *

# WDDX has a Boolean type.  We need to generate such variables, so
# this defines a class representing a truth value, and then creates
# TRUE and FALSE.

class TruthValue:
    def __init__(self, value): self.value = value
    def __nonzero__(self): return self.value
    
TRUE = TruthValue(1)
FALSE = TruthValue(0)

class WDDXMarshaller(Marshaller):
    tag_root = 'wddxPacket'
    tag_float = tag_int = tag_long = 'number'
    tag_instance = 'boolean'

    unmarshal_meth = {
        'wddxPacket': ('um_start_root', 'um_end_root'),
        'boolean': ('um_start_boolean', 'um_end_boolean'),
        'number': ('um_start_number', 'um_end_number'),
        'string': ('um_start_string', 'um_end_string'),
        }
    m_reference = m_tuple = m_list = Marshaller.m_unimplemented
    m_dictionary = m_None = m_code = Marshaller.m_unimplemented
    m_complex = Marshaller.m_unimplemented
    
    def m_instance(self, value, dict):
        if value not in [TRUE, FALSE]:
            self.m_unimplemented(value, dict)
        if value is TRUE: return ['<boolean value="true"/>']
        else: return ['<boolean value="false"/>']

    def um_start_boolean(self, name, attrs):
        v = attrs['value']
        self.data_stack.append( [v] )

    def um_end_boolean(self, name):
        ds = self.data_stack
        if ds[-1][0]=='true': ds[-1] = TRUE
        else: ds[-1] = FALSE

    um_start_number = Marshaller.um_start_generic
    um_end_number = Marshaller.um_end_float 
    
_m = WDDXMarshaller()
dump = _m.dump ; dumps = _m.dumps
load = _m.load ; loads = _m.loads
    
if __name__ == '__main__':
    print "Testing WDDX marshalling..."
    test(load, loads, dump, dumps,
         [TRUE, FALSE, 1, pow(2,123L), 19.72,  
          "here is a string & a <fake tag>"
         ]
        )

