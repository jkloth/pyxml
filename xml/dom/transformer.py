'''transform.py: Document / grove transformation framework.

This module provides:

- a Transformer abstract base class, meant to be subclassed with ``do_*'' 
methods, where ``*'' stands for possible element tag names.

- various helper functions.

Issues: currently, the document or grove passed to a transformer is
tranformed in place, it might be better to keep the original.

'''

from xml.dom.core import *

def having(list, condition):
	'Filter nodes in <list> having <condition>.'
	#code = compile(condition)
	res = []
	for x in list:
		try:
			if eval(condition, {'this' : x}, {}):
				res.append(x)
		except:
			pass
	return res


def cdata(list):
	'Flatten a node list.'

	s = ''
	for node in list:
		if node.NodeType == TEXT:
			s = s + node.data
		elif node.NodeType == ELEMENT:
			s = s + cdata(node.getChildren())
	return s


class Transformer:
	simple_map = {}

	def __init__(self, factory=None):
		if factory:
			self.dom_factory = factory
		else:
			self.dom_factory = DOMFactory()


	def transform(self, x):
		'Tranform document or subtree.'

		if x.NodeType == DOCUMENT:
			root_element = x.documentElement
		else:
			root_element = x

		res = self._transform_node(root_element)[0]

		if x.NodeType == DOCUMENT:
			x.documentElement = res
			return x
		else:
			return res


	def _transform_node(self, node):
		'Transform node (currently, only elements are affected).'

		if node.NodeType == ELEMENT:
			new_children = []
			for child in node.getChildren():
				new_children = new_children + self._transform_node(child)
			node._children = new_children

			repl = self.simple_map.get(node.tagName)
			if repl:
				return self.transform_simple(node, repl)

			if hasattr(self, 'do_' + node.tagName):
				return getattr(self, 'do_' + node.tagName)(node)

			if hasattr(self, 'do_ANY'):
				return self.do_ANY(node)

		return [node]


	def transform_simple(self, node, repl):
		"Transform element using `simple' replacement."

		l = string.split(repl, '/')
		l.reverse()
		new_node = None
		for tag in l:
			new_new_node = self.dom_factory.createElement(tag, {})
			if new_node:
				new_node.insertBefore(new_new_node, None)
			else:
				for child in node.getChildren():
					new_new_node.insertBefore(child, None)
			new_node = new_new_node
		return [new_node]

# vim:ts=2:ai
