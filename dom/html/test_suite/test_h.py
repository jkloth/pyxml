from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLHeadingElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	h = doc.createElement('H1')

	print 'testing get/set'
	testAttribute(h,'align')
	print 'get/set works'

if __name__ == '__main__':
	test()
