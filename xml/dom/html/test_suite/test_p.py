from util import testAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLParagraphElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	p = doc.createElement('P')

	print 'testing get/set'
	testAttribute(p,'align')
	print 'get/set works'


if __name__ == '__main__':
	test()
