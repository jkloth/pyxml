from util import testAttribute
from util import testIntAttribute
from util import error

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLTableElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	t = doc.createElement('TABLE')

	print 'testing get/set'
	testAttribute(t,'align');
	testAttribute(t,'bgColor');
	testAttribute(t,'border');
	testAttribute(t,'cellPadding');
	testAttribute(t,'cellSpacing');
	testAttribute(t,'frame');
	testAttribute(t,'rules');
	testAttribute(t,'summary');
	testAttribute(t,'width');
	print 'get/set works'

	print 'testing create and delete of THead'
	h = t.createTHead()
	h2 = t.createTHead()

	if t.childNodes.length != 1:
		error('create THead failed');

	if h.nodeName != h2.nodeName:
		error('create a second THead fails');

	t.deleteTHead()

	if t.childNodes.length != 0:
		error('deleteTHead fails')

	t.deleteTHead()

	print 'create and delete thead works'

	print 'testing create and delete TFoot'
	f = t.createTFoot()
	f2 = t.createTFoot()

	if t.childNodes.length != 1:
		error('create TFoot failed');

	if f.nodeName != f2.nodeName:
		error('create a second TFoot fails');

	t.deleteTFoot();
	if t.childNodes.length != 0:
		error('deleteTFoot fails')

	t.deleteTFoot()

	print 'create and delete of tfoot works'

	print 'testing create and delete of caption'

	c = t.createCaption()
	c2 = t.createCaption()

	if t.childNodes.length != 1:
		error('create Caption failed');
	
	if c.nodeName != c2.nodeName:
		error('second Create caption fails');

	t.deleteCaption()

	if t.childNodes.length != 0:
		error('delete of Caption failed');

	t.deleteCaption()

	print 'create and delete of caption works'

	print 'testing get Caption'

	c = t.createCaption()

	if t._get_caption().nodeName != c.nodeName:
		error('get caption failed');

	print 'getCaption works'
	print 'testing getTHead'

	h = t.createTHead();

	if t._get_tHead().nodeName != h.nodeName:
		error('get THead failed');

	print 'getTHead works'
	print 'testing getTFoot'

	f = t.createTFoot();

	if t._get_tFoot().nodeName != f.nodeName:
		error('get TFoot failed');


	print 'getTFoot works'	

	print 'testing getRows,insertRow, and deleteRow'

	if t._get_rows().length != 0:
		error('getRows failed');

	r1 = t.insertRow(0);

	if t._get_rows().length != 1:
		error('getRows failed');

	if t._get_rows()[0].nodeName != r1.nodeName:
		error('insertRow Failed');

	r2 = t.insertRow(10)

	if t._get_rows().length != 11:
		error('insertRows(10) failed');

	r3 = t.insertRow(-1);

	if t._get_rows().length != 11:
		error('insertRows(-1) failed');

	t.deleteRow(0)

	if t._get_rows().length != 10:
		error('deleteRow failed');

	if t._get_rows()[9].nodeName != r2.nodeName:
		error('deleteRow failed');

	print 'insertRow, deleteRow, getRows works';

	print 'testing getTBodies'

	if t._get_tBodies().length != 1:
		error('getTBodies');

	print 'getTBodies works'

	print 'testing TR.getRowIndex'

	if r2._get_rowIndex() != 9:
		error('getRowIndex failed');

	print 'TR.getRowIndex works'


if __name__ == '__main__':
	test()
