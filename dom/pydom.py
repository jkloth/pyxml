"""DOM elements construction using Python syntax.
"""

from xml.dom import core

class Element(core.Element):
	tagName = GI = '???'
	is_empty = 0

	def __init__(self, *t, **d):
		core.Element.__init__(self, tagName=self.tagName)

		for name, value in d.items():
			self.set_attr(name, value)
			
		for x in t:
			if type(x) == type({}):
				for name, value in x.items():
					self.set_attr(name, value)
			elif type(x) in (type(()), type([])):
				for y in x:
					self.appendChild(y)
			elif type(x) == type(''):
				child = core.Text()
				child.data = x
				self.appendChild(child)
			else:
				self.appendChild(x)

	def __lshift__(self, other):
		self.insertBefore(other, None)


def makeElementClass(tagName):
	d = {}
	exec(
		'class %s(Element): tagName = GI = "%s"' % (tagName, tagName), 
		globals(), d
	)
	return d[tagName]


if __name__ == '__main__':
	HTML = makeElementClass('HTML')
	HEAD = makeElementClass('HEAD')
	BODY = makeElementClass('BODY')
	H1 = makeElementClass('H1')

	t = HTML(HEAD(), BODY(H1('this is a test'), "don't panic."))
	from xml.dom.writer import HtmlWriter
	l = HtmlWriter()
	l.write(t)
