# built-in tests
from xml.marshal import generic, wddx, xmlrpc

generic.runtests()
wddx.runtests()
xmlrpc.runtests()

# additional tests
from test.test_support import verify

# test for correct processing of ignorable whitespace
data = """<?xml version="1.0"?>
<marshal>
  <list id="i2">
    <int>1</int>
    <int>2</int>
  </list>
</marshal>"""

verify(generic.loads(data) == [1, 2])
