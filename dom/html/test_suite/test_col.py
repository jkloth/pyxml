from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLTableColElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	c = doc.createElement('COL');

	print 'testing get/set'
	testAttribute(c,'align');
	testAttribute(c,'ch');
	testAttribute(c,'chOff');
	testIntAttribute(c,'span');
	testAttribute(c,'vAlign');
	testAttribute(c,'width');
	print 'get/set works'


if __name__ == '__main__':

	test();
