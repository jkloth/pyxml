from util import testAttribute
from util import error

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLTableRowElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	r = doc.createElement('TR')

	#Row index and section row index tested in section

	print 'testing get/set'
	testAttribute(r,'align');
	testAttribute(r,'bgColor');
	testAttribute(r,'ch');
	testAttribute(r,'chOff');
	testAttribute(r,'vAlign');
	print 'get/set works'

	print 'testing insertCell,deleteCell, getCells, and TD.cellIndex'

	c1 = r.insertCell(-1)

	if c1 != None:
		error('insertCell(-1) does not return None');

	c1 = r.insertCell(0)
	if c1 == None:
		error('insertCell(0) failed');

	c2 = r.insertCell(10)
	if c1 == None:
		error('insertCell(10) failed');

	if c2._get_cellIndex() != 10:
		error('getCellIndex Failed');

	cells = r._get_cells()
	if cells._get_length() != 11:
		error('getCells failed');

	if cells.item(0).nodeName != c1.nodeName:
		error('getCells failed');

	if cells.item(10).nodeName != c2.nodeName:
		error('item failed');

	r.deleteCell(-1);
	if r._get_cells().length != 11:
		error('deleteCell(-1) failed');

	r.deleteCell(10);
	if c2._get_cellIndex() != -1:
		error('deleted cell still in tree');

	if r._get_cells().length != 10:
		error('deleteCell failed');

	r.deleteCell(10);
	if r._get_cells()._get_length() != 10:
		error('deleteCell(10) failed');

	print 'insertCell, deleteCell, getCells, and TD.getCellIndex works' 


if __name__ == '__main__':
	test();

