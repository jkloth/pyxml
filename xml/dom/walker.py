from xml.dom.core import *

class Walker:

	def walk(self, root):
		if root.get_nodeType() == DOCUMENT_NODE:
			c = root.get_documentElement()
			assert c.get_nodeType() == ELEMENT_NODE
			return self.walk1(c)
		else:
			return self.walk1(root)
		
	def walk1(self, node):
		if node.get_nodeType() == ELEMENT_NODE:
			self.startElement(node)
			for child in node.get_childNodes():
				self.walk1(child)
			self.endElement(node)
		else:
			self.doText(node)

