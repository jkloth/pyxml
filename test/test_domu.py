# Test the dom.util module

from xml.dom import core, util

# Build a test DOM tree
from xml.dom.builder import Builder
b = Builder()
b.startElement("top")
b.text("     ")
b.text("\n\n\n\n\n")
b.text("real text")
b.text("     ")
b.text("more text")
b.startElement('subthing')
b.text("  text     with        spaces ")
b.endElement('subthing')
b.text("\n\n\n\n\n")
b.endElement('top')

t = b.document
t2 = t.cloneNode(1)

print 'strip_whitespace test'
print t.toxml()
util.strip_whitespace(t, util.WS_LEFT)
print '=========='
print t.toxml()

print '======================'

print 'collapse_whitespace test'
print t2.toxml()
util.collapse_whitespace(t2, util.WS_INTERNAL)

print '=========='
print t2.toxml()
print

t2.documentElement.normalize()
util.collapse_whitespace(t2, util.WS_INTERNAL)
print t2.toxml()


