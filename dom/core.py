'''
core.py: `light' implementation of the Document Objet Model (core) level 1.

Reference: http://www.w3.org/TR/WD-DOM/level-one-core

Deviations froc the specs:

-- there are no classes NodeList, EditableNodeList and NodeEnumerator,
since node lists are simply implemented as lists.

-- there are no Attributes nor AttributeList classes, as attrubutes are
currently implemented by a dictionnary.

-- there is currently no DocumentContext.

So, useful classes in this module are Node (abstract) and its (concrete)
subclasses -- Document, Element, Text, Comment, PI -- all of
which should be instanciated though a DOMFactory instance.

I have added an alias, ``GI'' for ``tagName'', for compatibility
with previous work.

Typical usage (create document with empty <html> element):

from xml.dom.core import *

dom_factory = DOMFactory()
document = dom_factory.createDocument()
html_node = dom_factory.createElement('html', {})
document.insertBefore(html_node, None)
...

'''

import string

# Exceptions.
NoSuchNodeException = 'No such node'
NotMyChildException = 'Not my child'
NotImplemented = 'Not implemented'

# Node types.

DOCUMENT = 0
ELEMENT = 1
ATTRIBUTE = 1
PI = 3
COMMENT = 4
TEXT = 5

class Node:
	'''Base class for grove nodes in DOM model.'''

	GI = None # Alias for tagName

	def __init__(self, **d):
		self._children = []
		self._parent = None

		for key, value in d.items():
			setattr(self, key, value)
		if hasattr(self, 'tagName'):
			self.GI = self.tagName

	def index(self):
		if self._parent:
			return self._parent._children.index(self)
		else:
			return -1

	# get/set
	def getParentNode(self):
		return self._parent
	
	def getChildren(self):
		# XXX: should return a NodeList.
		return self._children

	def hasChildren(self):
		return len(self._children) > 0

	def getFirstChild(self):
		if self.hasChildren():
			return self._children[0]
		else:
			return None

	def getPreviousSibling(self):
		i = self.index()
		if i <= 0:
			return None
		else:
			return self._parent._children[i - 1]

	def getNextSibling(self):
		i = self.index()
		assert self._parent._children[i] == self
		if i == -1 or i == len(self._parent._children) - 1:
			return None
		else:
			return self._parent._children[i + 1]

	def appendChild(self, new_child):
		'XXX: not in interface.'

		self._children.append(new_child)
		new_child._parent = self
		#new_child.document = self.document

	def insertBefore(self, new_child, ref_child):
		if ref_child == None:
			self.appendChild(new_child)
			return
		for i in range(0, len(self._children)):
			if self._children[i] == ref_child:
				self._children[i:i] = [new_child]
				new_child._parent = self
				#new_child.document = self.document
				return
		raise NotMyChildException
			
	def replaceChild(self, old_child, new_child):
		for i in range(0, len(self._children)):
			if self._children[i] == old_child:
				self._children[i] = new_child
				new_child._parent = self
				return old_child
		raise NotMyChildException
			
	def removeChild(self, old_child):
		try:
			i = self._children.index(old_child)
			del self._children[i]
		except ValueError:
			raise NotMyChildException
			

	def __str__(self):
		from xml.dom.writer import XmlLineariser
		w = XmlLineariser()
		return w.linearise(self)
			

class Document(Node):
	NodeType = DOCUMENT
	GI = "#DOCUMENT"

	def __init__(self):
		Node.__init__(self)
		self.elements_dict = None
		self.documentElement = None
	
	# XXX: experimental, not in DOM.
	#def add_element(self, node):
	#	l = self.elements_dict.get(node.tagName)
	#	if l:
	#		l.append(node)
	#	else:
	#		self.elements_dict[node.tagName] = [node]
	
	def getElementsByTagName(self, name):
		if self.elements_dict is not None:
			return self.elements_dict.get(name, [])
		else:
			return self.documentElement.getElementsByTagName(name)

	def getDocumentElement(self):
	    return self.documentElement

	def setDocumentElement(self, node):
	    self.documentElement = node


class Element(Node):
	NodeType = ELEMENT

	def __init__(self, tagName):
		Node.__init__(self, tagName=tagName)
		self.attributes = {}

	def getTagName(self):
	    return self.tagName
		
	def setAttribute(self, attribute):
		# XXX
		raise NotImplemented

	def getElementsByTagName(self, name):
		# XXX: Return list instead of NodeEnumerator.
		l = []
		for child in self._children:
			if child.NodeType == ELEMENT:
				l = l + child.getElementsByTagName(name)
				if child.tagName == name:
					l.append(child)
		return l

	# XXX: not in DOM.
	def set_attr(self, name, value):
		self.attributes[name] = value


class Attribute(Node):
	# XXX: not used!!!
	NodeType = ATTRIBUTE
	GI = "#ATTR"


class Text(Node):
	GI = "#PCDATA"
	NodeType = TEXT

	def __str__(self):
		return self.data


class Comment(Node):
	GI = "#COMMENT"
	NodeType = COMMENT
	data = ''

	def __str__(self):
		return '<-- ?? -->' % self.data


class PI(Node):
	GI = "#PI"
	NodeType = PI
	data = ''

	def __str__(self):
		return '<? %s ?>' % self.data


# Auxiliary types.

class DOMFactory:
	def createDocumentContext(self):
		return DocumentContext()

	def createDocument(self):
		return Document()

	def createElement(self, tagName, attributes):
		e = Element(tagName)
		e.attributes = attributes
		return e

	def createAttribute(self, name, value):
		a = Attribute()
		a.name = name
		a.value = value
		
	def createTextNode(self, data):
		return Text(data=data)
		
	def createComment(self, data):
		return Comment(data=data)
		

# vim:ts=2:ai
