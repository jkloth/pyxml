from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLIFrameElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	f = doc.createElement('IFrame')

	print 'testing get/set'
	testAttribute(f,'align');
	testAttribute(f,'frameBorder');
	testAttribute(f,'height');
	testAttribute(f,'longDesc');
	testAttribute(f,'marginHeight');
	testAttribute(f,'marginWidth');
	testAttribute(f,'scrolling');
	testAttribute(f,'src');
	testAttribute(f,'width');
	print 'get/set works'


if __name__ == '__main__':
	test()
