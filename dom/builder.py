'''
Event-driven, almost-SAXish, grove builder.


'''

from xml.dom.core import *

class Builder:

	def __init__(self, factory=None):
		self.dom_factory = factory or DOMFactory()
		self.document = self.dom_factory.createDocument()
		self.current_element = None


	def push(self, node):
		"Add node to current node and move to new node."

		if self.current_element:
			self.current_element.insertBefore(node, None)
		elif node.NodeType == ELEMENT:
			self.document.setDocumentElement(node)

		if node.NodeType == ELEMENT:
			self.current_element = node

	def pop(self):
		"Move to current node's parent."

		self.current_element = self.current_element.getParentNode()
		

	def startElement(self, name, attrs):
		if hasattr(self, 'start_' + name):
			getattr(self, 'start_' + name)(elm)
		else:
			element = self.dom_factory.createElement(name, attrs)
			self.push(element)
	
	def endElement(self, name):
		assert name == self.current_element.tagName
		self.pop()


	def text(self, s):
		if self.current_element:
			text_node = self.dom_factory.createTextNode(s)
			self.current_element.insertBefore(text_node, None)


