#! /usr/bin/env python
'''XML Canonicalization

This module generates canonical XML, as defined in
    http://www.w3.org/TR/xml-c14n

It is limited in that it can only canonicalize an element and all its
children; general document subsets are not supported.
'''

_copyright = '''Copyright 2001, Zolera Systems Inc.  All Rights Reserved.
Distributed under the terms of the Python 2.0 Copyright.'''

from xml.dom import Node
from xml.ns import XMLNS
import re
import StringIO

_attrs = lambda E: E._get_attributes() or []
_children = lambda E: E._get_childNodes() or []

def _sorter(n1, n2):
    '''Sorting predicate for non-NS attributes.'''
    i = cmp(n1._get_namespaceURI(), n2._get_namespaceURI())
    if i: return i
    return cmp(n1._get_localName(), n2._get_localName())

class _implementation:
    '''Implementation class for C14N.'''

    # Handlers for each node, by node type.
    handlers = {}

    # pattern/replacement list for whitespace stripping.
    repats = (
	( re.compile(r'[ \t]+'), ' ' ),
	( re.compile(r'[\r\n]+'), '\n' ),
    )

    def __init__(self, node, write, nsdict={}, stripspace=0, nocomments=1):
	'''Create and run the implementation.'''
	if node._get_nodeType() != Node.ELEMENT_NODE:
	    raise TypeError, 'Non-element node'
	self.write, self.stripspace, self.nocomments = \
		write, stripspace, nocomments

	if nsdict == None or nsdict == {}:
	    nsdict = { 'xml': XMLNS.XML, 'xmlns': XMLNS.BASE }
	self.ns_stack = [ nsdict ]

	# Collect the initial list of xml:XXX attributes.
	xmlattrs = []
	for a in _attrs(node):
	    if a._get_namespaceURI() == XMLNS.XML:
		n = a._get_localName()
		xmlattrs.append(n)

	# Walk up and get all xml:XXX attributes we inherit.
	parent, inherited = node._get_parentNode(), []
	while parent:
	    if parent._get_nodeType() != Node.ELEMENT_NODE: break
	    for a in _attrs(parent):
		if a._get_namespaceURI() != XMLNS.XML: continue
		n = a._get_localName()
		if n not in xmlattrs:
		    xmlattrs.append(n)
		    inherited.append(a)
	    parent = parent._get_parentNode()

	self._do_element(node, inherited)
	self.ns_stack.pop()

    def _do_text(self, node):
	'Process a text node.'
	s = node._get_data() \
		.replace("&", "&amp;") \
		.replace("<", "&lt;") \
		.replace(">", "&gt;") \
		.replace("\015", "&#xD;")
	if self.stripspace:
	    for pat,repl in _implementation.repats: s = re.sub(pat, repl, s)
	if s: self.write(s)
    handlers[Node.TEXT_NODE] =_do_text
    handlers[Node.CDATA_SECTION_NODE] =_do_text

    def _do_pi(self, node):
	'''Process a PI node.  Since we start with an element, we're
	never a child of the root, so we never write leading or trailing
	#xA.
	'''
	W = self.write
	W('<?')
	W(node._get_nodeName())
	s = node._get_data()
	if s:
	    W(' ')
	    W(s)
	W('?>')
    handlers[Node.PROCESSING_INSTRUCTION_NODE] =_do_pi

    def _do_comment(self, node):
	'''Process a comment node.  Since we start with an element, we're
	never a child of the root, so we never write leading or trailing
	#xA.
	'''
	if self.nocomments: return
	W = self.write
	W('<!--')
	W(node._get_data())
	W('-->')
    handlers[Node.COMMENT_NODE] =_do_comment

    def _do_attr(self, n, value):
	'Process an attribute.'
	W = self.write
	W(' ')
	W(n)
	W('="')
	s = value \
	    .replace("&", "&amp;") \
	    .replace("<", "&lt;") \
	    .replace('"', '&quot;') \
	    .replace('\011', '&#9') \
	    .replace('\012', '&#A') \
	    .replace('\015', '&#D')
	W(s)
	W('"')

    def _do_element(self, node, initialattrlist = []):
	'Process an element (and its children).'
	name = node._get_nodeName()
	parent_ns = self.ns_stack[-1]
	my_ns = { 'xmlns': parent_ns.get('xmlns', XMLNS.BASE) }
	W = self.write
	W('<')
	W(name)

	# Divide attributes into NS definitions and others.
	nsnodes, others = [], initialattrlist[:]
	for a in _attrs(node):
	    if a._get_namespaceURI() == XMLNS.BASE:
		nsnodes.append(a)
	    else:
		others.append(a)

	# Namespace attributes: update dictionary; if not already
	# in parent, output it.
	nsnodes.sort(lambda n1, n2: \
		cmp(n1._get_localName(), n2._get_localName()))
	for a in nsnodes:
	    n = a._get_nodeName()
	    if n == "xmlns:":
		key, n = "", "xmlns"
	    else:
		key = a._get_localName()
	    v = my_ns[key] = a._get_nodeValue()
	    pval = parent_ns.get(key, None)
	    if v != pval: self._do_attr(n, v)

	# Other attributes: sort and output.
	others.sort(_sorter)
	for a in others: self._do_attr(a._get_nodeName(), a._get_value())

	W('>')

	self.ns_stack.append(my_ns)
	for c in _children(node):
	    _implementation.handlers[c._get_nodeType()](self, c)
	    # XXX Ignore unknown node types?
	    #handler = _implementation.handlers.get(c._get_nodeType(), None)
	    #if handler: handler(self, c)
	self.ns_stack.pop()
	W('</%s>' % (name,))
    handlers[Node.ELEMENT_NODE] =_do_element

def Canonicalize(node, output=None, **kw):
    '''Canonicalize a DOM element node and everything underneath it.
    Return the text; if output is specified then output.write will
    be called to output the text and None will be returned
    Keyword parameters:
	stripspace -- remove extra (almost all) whitespace from text nodes
	nsdict -- a dictionary of prefix:uri namespace entries assumed
	    to exist in the surrounding context
	comments -- keep comments if non-zero (default is zero)
    '''

    if not output: s = StringIO.StringIO()
    _implementation(node,
	(output and output.write) or s.write,
	nsdict=kw.get('nsdict', {}),
	stripspace=kw.get('stripspace', 0),
	nocomments=kw.get('comments', 0) == 0,
    )
    if not output: return (s.getvalue(), s.close())[0]

if __name__ == '__main__':
    text = '''<SOAP-ENV:Envelope xml:lang='en'
      xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
      xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
      xmlns:xsi="http://www.w3.org/2001/XMLSchemaInstance"
      xmlns:xsd="http://www.w3.org/2001/XMLSchemaZ" xmlns:spare='foo'
      SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
	<SOAP-ENV:Body xmlns='test-uri'><?MYPI spenser?>
	    <zzz xsd:foo='xsdfoo' xsi:a='xsi:a'/>
	    <SOAP-ENC:byte>44</SOAP-ENC:byte>	<!-- 1 -->
	    <Name xml:lang='en-GB'>This is the name</Name>Some
content here on two lines.
	    <n2><![CDATA[<greeting>Hello</greeting>]]></n2> <!-- 3 -->
	    <n3 href='z&amp;zz' xsi:type='SOAP-ENC:string'>
	    more content.  indented    </n3>
	    <a2 xmlns:f='z' xmlns:aa='zz'><i xmlns:f='z'>12</i><t>rich salz</t></a2> <!-- 8 -->
	</SOAP-ENV:Body>
      <z xmlns='myns' id='zzz'>The value of n3</z>
      <zz xmlns:spare='foo' xmlns='myns2' id='tri2'><inner>content</inner></zz>
</SOAP-ENV:Envelope>'''

    print _copyright
    from xml.dom.ext.reader import PyExpat
    reader = PyExpat.Reader()
    dom = reader.fromString(text)
    for e in _children(dom):
	if e._get_nodeType() != Node.ELEMENT_NODE: continue
	for ee in _children(e):
	    if ee._get_nodeType() != Node.ELEMENT_NODE: continue
	    print '\n', '=' * 60
	    print Canonicalize(ee, nsdict={'spare':'foo'}, stripspace=1)
	    print '-' * 60
	    print Canonicalize(ee, stripspace=0)
	    print '-' * 60
	    print Canonicalize(ee, comments=1)
	    print '=' * 60
