import string, re
from xml.dom.core import *

def quote(s):
	s = re.sub('&', '&amp;', s)
	s = re.sub('<', '&lt;', s)
	s = re.sub('>', '&gt;', s)
	return s
	

class XmlLineariser :

	def __init__(self) :
		self.empties = []
		self.strip = []
		self.xml_style_endtags = 1
		self.add_newline_before = []
		self.add_newline_after = []

	def linearise(self, root) :
		if root.NodeType == DOCUMENT:
			assert root.documentElement.NodeType == ELEMENT
			return self.linearise_element(root.documentElement)
		else:
			return self.linearise_element(root)

	def linearise_element(self, element) :
		assert element.NodeType == ELEMENT
		s = ''
		if element.GI in self.add_newline_before:
			s = s + '\n'
		s = s + '<%s' % element.GI
		
		# XXX use DOM interface here.
		for name, value in element.attributes.items() :
			s = s + ' %s="%s"' % (name, value)

		if self.xml_style_endtags and not element.children:
			return s + '/>'
		s = s + '>'

		s1 = ''
		for child in element.children :
			if child.NodeType is ELEMENT:
				s1 = s1 + self.linearise_element(child)
			elif child.NodeType is TEXT:
				s1 = s1 + quote(child.data)
			else :
				s1 = s1 + str(child)

		if element.GI in self.strip :
			s = s + string.strip(s1)
		else :
			s = s + s1
			
		if not element.GI in self.empties :
			s = s + '</%s>' % element.GI
		if element.GI in self.add_newline_after:
			s = s + '\n'

		return s


class HtmlLineariser(XmlLineariser):
	def __init__(self):
		self.xml_style_endtags = 0
		self.empties = [
			'img', 'br', 'hr', 'include', 'li', 'meta', 'input',
			'IMG', 'BR', 'HR', 'INCLUDE', 'LI', 'META', 'INPUT',
		]
		self.strip = [
			'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
			'li', 'br', 'p', 'a', 'title', 'font',
			'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 
			'LI', 'BR', 'P', 'A', 'TITLE', 'FONT',
		]
		self.add_newline_before = [
			'head', 'body', 'title', 'ul', 'li',
			'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
			'HEAD', 'BODY', 'TITLE', 'UL', 'LI',
			'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
		]
		self.add_newline_after = [
			'html', 'p', 'br', 'hr', 'head', 'body', 'title', 'meta', 'li', 'ul',
			'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
			'HTML', 'P', 'BR', 'HR', 'HEAD', 'BODY', 'TITLE', 'META', 'LI', 'UL',
			'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
		]


class ASPLineariser(XmlLineariser):
	def __init__(self, rep_file):
		self.rep_dict = {}
		self.parseRepFile(rep_file)
		

	def parseRepFile(self, rep_file):
		s = ''
		for l in open(rep_file).readlines():
			if l[0] == '<':
				plus_before = 0
				plus_after = 0
				n = string.index(l, '>')
				tag_name = l[1:n]
				rep = string.strip(l[n+1:])
				if rep and rep[0] == '+':
					plus_before = 1
					rep = string.strip(rep[1:])
				if rep and rep[-1] == '+':
					plus_after = 1
					rep = string.strip(rep[:-1])
				if rep:
					self.rep_dict[tag_name] = (plus_before, plus_after, eval(rep))
				else:
					self.rep_dict[tag_name] = (plus_before, plus_after, '')
					

	def linearise_element(self, element) :
		assert element.NodeType == ELEMENT
		s = ''
		
		# Start tag
		plus_before, plus_after, repl = self.rep_dict[element.getTagName()]

		if s and s[-1] != '\n' and plus_before:
			s = s + '\n'
		s = s + repl
		if s and s[-1] != '\n' and plus_after:
			s = s + '\n'

		s1 = ''
		for child in element.children :
			if child.NodeType is ELEMENT:
				s1 = s1 + self.linearise_element(child)
			elif child.NodeType is TEXT:
				#s1 = s1 + quote(child.data)
				s1 = s1 + child.data
			else :
				s1 = s1 + str(child)
		
		s = s + s1

		# End tag.
		plus_before, plus_after, repl = self.rep_dict['/' + element.getTagName()]
		if s and s[-1] != '\n' and plus_before:
			s = s + '\n'
		s = s + repl
		if s and s[-1] != '\n' and plus_after:
			s = s + '\n'


		return s


