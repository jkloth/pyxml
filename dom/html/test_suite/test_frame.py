from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLFrameElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	f = doc.createElement('Frame')

	print 'testing get/set'
	testAttribute(f,'frameBorder')
	testAttribute(f,'longDesc')
	testAttribute(f,'marginHeight')
	testAttribute(f,'marginWidth')
	testIntAttribute(f,'noResize')
	testAttribute(f,'scrolling')
	testAttribute(f,'src')
	print 'get/set works'

if __name__ == '__main__':
	test()
