from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLLegendElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	l = doc.createElement('LEGEND')

	print 'testing get/set'
	testAttribute(l,'accessKey')
	testAttribute(l,'align')
	print 'get/set works'


if __name__ == '__main__':
	test();
