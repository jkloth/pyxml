from xml.dom.core import *

class Walker:

	def walk(self, root):
		if root.NodeType == DOCUMENT:
			assert root.documentElement.NodeType == ELEMENT
			return self.walk1(root.documentElement)
		else:
			return self.walk1(root)
		
	def walk1(self, node):
		if node.NodeType == ELEMENT:
			self.startElement(node)
			for child in node.getChildren():
				self.walk1(child)
			self.endElement(node)
		else:
			self.doText(node)

