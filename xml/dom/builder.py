'''
Event-driven, almost-SAXish, grove builder.


'''

from xml.dom.core import *

class Builder:

	def __init__(self):
		self.document = createDocument()
		self.current_element = None


	def push(self, node):
		"Add node to current node and move to new node."

		if self.current_element:
			self.current_element.insertBefore(node, None)
		elif node.get_nodeType() == ELEMENT:
#			cur_root = self.document.get_firstChild()
			self.document.appendChild(node)

		if node.get_nodeType() == ELEMENT:
			self.current_element = node

	def pop(self):
		"Move to current node's parent."

		self.current_element = self.current_element.get_parentNode()
		

	def startElement(self, name, attrs):
		if hasattr(self, 'start_' + name):
			getattr(self, 'start_' + name)(elm)
		else:
			element = self.document.createElement(name)
			for key, value in attrs.items():
				element.setAttribute(key, value)
			self.push(element)
	
	def endElement(self, name):
		assert name == self.current_element.get_nodeName()
		self.pop()


	def text(self, s):
		if self.current_element:
			text_node = self.document.createTextNode(s)
			self.current_element.insertBefore(text_node, None)


