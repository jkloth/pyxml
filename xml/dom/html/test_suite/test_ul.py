from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLUListElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	u = doc.createElement('UL')

	print 'testing get/set'
	testIntAttribute(u,'compact')
	testAttribute(u,'type')

	print 'get/set works'


if __name__ == '__main__':
	test()
