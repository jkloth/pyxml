
from xml.dom.dc_parser import InferEndTags, Scanner
from xml.dom.core import DOMFactory
from xml.dom.builder import Builder


class DcBuilder(InferEndTags, Builder):
	
	def __init__(self):
		Builder.__init__(self)
		InferEndTags.__init__(self)
		self.scanner(Scanner())

	
	def feed(self, s):
		self.p.feed(s)
		self.p.next(self)
		self.eof()


	def startElement(self, elm):
		Builder.startElement(self, elm.name, elm.attrs)

	def endElement(self, elm):
		Builder.endElement(self, elm.name)


	def text(self, s):
		InferEndTags.text(self, s)
		Builder.text(self, s)

