from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLDivElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	d = doc.createElement('Div')

	print 'testing get/set'
	testAttribute(d, 'align');
	print 'get/set works'


if __name__ == '__main__':

	test();
