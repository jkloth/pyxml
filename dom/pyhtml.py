"""HTML elements.

Clases representing HTML4.0 elements, subclassed from DOM.core.Element.
"""

from pydom import makeElementClass

def makeAll():
	empties = ['BR', 'HR', 'IMG']
	non_empties = [
		'HTML', 
		'HEAD', 'META', 'TITLE',
		'BODY', 
		'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
		'FONT', 'BASEFONT', 'ADDRESS', 'DIV',
		'CENTER', # deprecated
		'A', 'MAP', 'AREA', 'LINK',
		'APPLET', 'OBJECT', 'SCRIPT',
		'PRE', 
		'P',
		'OL', 'UL', 'LI'
	]
	
	for name in empties:
		c = makeElementClass(name)
		c.is_empty = 1
		globals()[name] = c
	
	for name in non_empties:
		c = makeElementClass(name)
		globals()[name] = c
	
makeAll()
del makeAll

if __name__ == '__main__':
	t = HTML(HEAD(), BODY(H1('this is a test'), "don't panic."))
	print t.getChildren()
	from writer import HtmlWriter, XmlWriter, XmlLineariser

	l = XmlWriter()
	l.write(t)

