from util import testAttribute
from util import testIntAttribute

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLFormElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	f = doc.createElement('Form')

	print 'testing get/set'

	testAttribute(f,'name')
	testAttribute(f,'acceptCharset')
	testAttribute(f,'action')
	testAttribute(f,'encType')
	testAttribute(f,'method')
	testAttribute(f,'target')

	print 'get/sets work'
	print 'test getElements'
	i = doc.createElement('IsIndex')
	f.appendChild(i)
	hc = f._get_elements()
	if hc.length != 1:
		error('getElements failed')
	if f._get_length() != 1:
		error('getLength failed')
	print 'getElements works'


if __name__ == '__main__':
	test()
