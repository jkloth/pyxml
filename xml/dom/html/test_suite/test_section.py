from util import testAttribute
from util import error

def test():
	print 'testing source code syntax'
	from xml.dom.html import HTMLTableSectionElement
	from xml.dom import implementation
	doc = implementation.createHTMLDocument('Title')
	s = doc.createElement('TFOOT')

	#Row index and section row index tested in section
	print 'testing get/set'
	testAttribute(s,'align')
	testAttribute(s,'ch')
	testAttribute(s,'chOff')
	testAttribute(s,'vAlign')
	print 'get/set works'

	print 'testing insertRow,deleteRow, getRows, and TR.getRowSelectionIndex'

	r1 = s.insertRow(-1)

	if r1 != None:
		error('insertRow(-1) does not return None');

	r1 = s.insertRow(0)
	if r1 == None:
		error('insertRow(0) failed');

	r2 = s.insertRow(10)
	if r2 == None:
		error('insertRow(10) failed');

	if r2._get_sectionRowIndex() != 10:
		error('getSectionRowIndex Failed');

	rows = s._get_rows()
	if rows._get_length() != 11:
		error('getRows failed')

	if rows.item(0).nodeName != r1.nodeName:
		error('getRows failed')

	if rows.item(10).nodeName != r2.nodeName:
		error('getRows failed')

	s.deleteRow(-1)
	if s._get_rows()._get_length() != 11:
		error('deleteRow(-1) failed')

	s.deleteRow(10)
	if r2._get_rowIndex() != -1:
		error('deleted row still in tree')

	if s._get_rows()._get_length() != 10:
		error('deleteRow failed');

	s.deleteRow(10)
	if s._get_rows()._get_length() != 10:
		error('deleteRow(10) failed')

	print 'insertRow, deleteRow, getRows, and TR.getSelectionRowIndex works' 


if __name__ == '__main__':
	test()
