# Test the modules in the utils/ subpackage

from xml.utils import *

print 'Testing utils.escape'
print 'These pairs of strings should all be identical'

print escape('&<>'), '&amp;&lt;&gt;'
print escape('foo&amp;bar'), 'foo&amp;amp;bar'
print escape('< test > &', {'test': '&myentity;'}), '&lt; &myentity; &gt; &amp;'

# XXX add test suite for is-8601
