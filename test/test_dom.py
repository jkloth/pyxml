
import StringIO
from xml.dom import core, sax_builder
from xml.sax import saxexts

# Internal test function: traverse a DOM tree, then verify that all
# the parent pointers are correct.  Do NOT take this function as an
# example of using the Python DOM interface; it knows about the hidden
# details of the DOM implementation in order to check them.

def _check_dom_tree(t):
    "Verify that all the parent pointers in a DOM tree are correct"
    parent = {}     # Dict mapping _nodeData instances to their parent
    nodes = []      # Cumulative list of all the _nodeDatas encountered
    Queue = [t]     # Queue for breadth-first traversal of tree

    # Do a breadth-first traversal of the DOM tree t
    while Queue:
        node = Queue[0]
	children = node.childNodes

        for c in children:
            # Store this node as the parent of each child
            parent[ c._node ] = node._node

            # Add each child to the cumulative list
	    nodes.append( c._node )

            # Append each child to the queue
	    Queue.append(c)

        # Remove the node we've just processed
        Queue = Queue[1:]

    # OK, now walk over all the children, building a proxy for the naked
    # _nodeData instance, and checking that .parentNode is correct.
    count = 0
    for n in nodes:
        n = core.NODE_CLASS[ n.type ](n, t._node)
	p = n.get_parentNode()
	if p is None:
            assert not parent.has_key(n._node)
        else:
	    assert p._node == parent[ n._node ]
        count = count + 1

test_text = """<?xml version="1.0"?>
<doc>
<title>This is a test</title>
<h1>Don't panic</h1>
<p>Maybe it will work.</p>
<h2>We can handle it</h2>
<h3>Yes we can</h3>
<h3>Or maybe not</h3>
End of test.
</doc>
"""

p = saxexts.make_parser()
h = sax_builder.SaxBuilder()
p.setDocumentHandler( h )
file = StringIO.StringIO( test_text )
p.parseFile( file )

doc = h.document
_check_dom_tree(doc)
print 'Simple document'
print doc.toxml()

# Example from the docstring at the top of xml.dom.core.py
doc = core.createDocument()                  
html = doc.createElement('html')
html.setAttribute('attr', 'value')
head = doc.createElement('head')
title = doc.createElement('title')

text = doc.createTextNode("Title goes here")
title.appendChild(text)
head.appendChild(title)                
html.appendChild(head)
doc.appendChild (html)                 

_check_dom_tree(doc)
print '\nOutput of docstring example'
print doc.toxml()

# Detailed test suite for the DOM

print '\nRunning detailed test suite'
def check(cond, explanation):
    truth = eval(cond)
    if not truth:
        print ' *** Failed:', explanation, '\n\t', cond

doc = core.createDocument()
check( 'isinstance(doc, core.Document)', 'createDocument returns a Document')
check( 'doc.parentNode == None', 'Documents have no parent')

# Check that documents can only have one child

n1 = doc.createElement('n1') ; n2 = doc.createElement('n2')
pi = doc.createProcessingInstruction("Processing", "Instruction")
doc.appendChild(pi)
doc.appendChild(n1)
doc.appendChild(n1)  # n1 should be removed, and then added again
try: doc.appendChild(n2)
except core.HierarchyRequestException: pass
else:
    print " *** Failed: Document.insertBefore didn't raise HierarchyRequestException"

doc.replaceChild(n2, n1)    # Should work
try: doc.replaceChild(n1, pi)    
except core.HierarchyRequestException: pass
else:
    print " *** Failed: Document.replaceChild didn't raise HierarchyRequestException"
doc.replaceChild(n2, pi)    # Should also work

check('pi.parentNode == None', 
      'Document.replaceChild: PI should have no parent')
doc.removeChild(n2)
check('n2.parentNode == None', 
      'Document.removeChild: n2 should have no parent')

# Check adding and deletion with DocumentFragments

fragment = doc.createDocumentFragment() ; fragment.appendChild( n1 )
doc.appendChild( fragment )
check('fragment.parentNode == None', 
      'Doc.appendChild: fragment has no parent')
check('n1.parentNode.nodeType == core.DOCUMENT_NODE', 
      'Doc.appendChild: n1 now has document as parent')

fragment = doc.createDocumentFragment() ; fragment.appendChild( n1 )
fragment.appendChild( doc.createElement('n2') )
try: doc.appendChild( fragment )
except core.HierarchyRequestException: pass
else:
    print " *** Failed: Document.fragment.appendChild didn't raise HierarchyRequestException"

doc.appendChild( n1 ) ; doc.appendChild( pi )
try: doc.replaceChild(fragment, pi)
except core.HierarchyRequestException: pass
else:
    print " *** Failed: Document.fragment.replaceChild didn't raise HierarchyRequestException"

n1.appendChild(fragment) ; _check_dom_tree(doc)

# Check adding and deleting children for ordinary nodes

n1 = doc.createElement('n1') ; n2 = doc.createElement('n2')
check( 'n1.parentNode == None', 'newly created Element has no parent')
e1 = doc.createText('e1') ; e2 = doc.createText('e2')
e3 = doc.createText('e3')
n1.appendChild( e1 ) ; n1.appendChild( e2 ) ; n2.appendChild(e3)

# Test .insertBefore with refChild set to a node
n2.insertBefore(e1, e3)
check('len(n1.childNodes) == 1', "insertBefore: node1 has 1 child")
check('len(n2.childNodes) == 2', "insertBefore: node2 has 2 children")
check('n1.firstChild.toxml()=="e2"', "insertBefore: node1's child is e2")
check('n2.firstChild.toxml()=="e1"', "insertBefore: node2's first child is e1")
check('n2.lastChild.toxml()=="e3"', "insertBefore: node2's last child is e3")

check('e1.parentNode.tagName == "n2"', "insertBefore: e1's parent is n2")
check('e2.parentNode.tagName == "n1"', "insertBefore: e2's parent is n1")
check('e3.parentNode.tagName == "n2"', "insertBefore: e3's parent is n3")

try: n2.insertBefore(e1, e2)
except core.NotFoundException: pass
else:
    print " *** Failed: insertBefore didn't raise NotFoundException"

# Test .insertBefore with refChild==None
n2.insertBefore(e1, None)
check('len(n2.childNodes) == 2', "None insertBefore: node1 has 2 children")
check('n2.firstChild.toxml()=="e3"', "None insertBefore: node2's first child is e3")
check('n2.lastChild.toxml()=="e1"', "None insertBefore: node2's last child is e1")

# Test replaceChild
ret = n1.replaceChild(e1, e2)
check('e2.parentNode == None', "replaceChild: e2 has no parent")
check('len(n1.childNodes) == 1', "replaceChild: node1 has 1 child")
check('n1.firstChild.toxml()=="e1"', "replaceChild: node1's only child is e1")
check('ret.toxml() == "e2"', "replaceChild: returned value node1's only child is e1")

try: n1.replaceChild(e2, e2)
except core.NotFoundException: pass
else:
    print " *** Failed: insertBefore didn't raise NotFoundException"

# Test removeChild
ret = n1.removeChild( e1 )
check('e1.parentNode == None', "removeChild: e1 has no parent")
check('ret.toxml() == "e1"', "removeChild: e1 is the returned value")

try: n1.removeChild(e2)
except core.NotFoundException: pass
else:
    print " *** Failed: removeChild didn't raise NotFoundException"

# XXX two more cases for adding stuff: normal, Document, DocumentFragment

# Test the functions in the CharacterData interface

text = doc.createText('Hello world')
check('text[0:5].value == "Hello"', 'text: slicing a node')

try: text.substringData(-5, 5)
except core.IndexSizeException: pass
else:
    print " *** Failed: substringData didn't raise IndexSizeException (negative)"

try: text.substringData(200, 5)
except core.IndexSizeException: pass
else:
    print " *** Failed: substringData didn't raise IndexSizeException (larger)"

try: text.substringData(5, -5)
except core.IndexSizeException: pass
else:
    print " *** Failed: substringData didn't raise IndexSizeException (negcount)"

text.appendData('!')
check('text.value == "Hello world!"', 'text: appendData')

try: text.insertData(-5, 'string')
except core.IndexSizeException: pass
else:
    print " *** Failed: insertData didn't raise IndexSizeException (negative)"

try: text.insertData(200, 'string')
except core.IndexSizeException: pass
else:
    print " *** Failed: insertData didn't raise IndexSizeException (larger)"

text.insertData(5, ',')
check('text.value == "Hello, world!"', 'text: insertData of ","')

try: text.deleteData(-5, 5)
except core.IndexSizeException: pass
else:
    print " *** Failed: deleteData didn't raise IndexSizeException (negative)"

try: text.deleteData(200, 5)
except core.IndexSizeException: pass
else:
    print " *** Failed: deleteData didn't raise IndexSizeException (larger)"

text.deleteData(0, 5)
check('text.value == ", world!"', 'text: deleteData of first 5 chars')

try: text.replaceData(-5, 5, 'Top of the')
except core.IndexSizeException: pass
else:
    print " *** Failed: replaceData didn't raise IndexSizeException (negative)"

try: text.replaceData(200, 5, 'Top of the')
except core.IndexSizeException: pass
else:
    print " *** Failed: replaceData didn't raise IndexSizeException (larger)"

text.replaceData(0, 1, 'Top of the')
check('text.value == "Top of the world!"', 'text: deleteData of first 5 chars')

# Test the Element class
e = doc.createElement('elem')
attr = doc.createAttribute('attr2')
attr.value = "v2"

check('e.toxml() == "<elem />"', 'Element: empty element')
check('e.tagName == "elem"', 'Element: tag name')
check('len(e.get_attributes()) == 0', 'Element: empty get_attributes')
check('e.getAttribute("dummy") == ""', 'Element: empty getAttribute')
check('e.getAttributeNode("dummy") == None', 'Element: empty getAttributeNode')

try: e.setAttribute('dummy', attr)
except TypeError: pass
else:
    print " *** Failed: setAttribute didn't raise TypeError"

e.setAttribute('dummy', 'value')
check('e.toxml() == "<elem dummy=\'value\' />"', 'Element with 1 attribute')
check('e.getAttribute("dummy") == "value"', 'Element: getAttribute w/ value')
check('e.getAttributeNode("dummy").value == "value"', 'Element: getAttributeNode w/ value')

a2 = e.getAttributeNode( 'dummy' )
check('a2.parentNode == None', 'Attribute: should have no parent')
check('a2.value == "value"', 'Attribute: value is correct')

e.removeAttribute('dummy')
check('e.toxml() == "<elem />"', 'Element: attribute removed')

e.setAttributeNode(attr)
check('e.toxml() == "<elem attr2=\'v2\' />"', 'Element: attribute node added')

a2 = doc.createAttribute('attr2')
a2.value = 'v3'

ret = e.setAttributeNode(a2)
check('e.toxml() == "<elem attr2=\'v3\' />"', 'Element: attribute node replaced')
check('ret.value == "v2"', 'Element: deleted attribute node returned')

e.removeAttributeNode(a2)
check('e.toxml() == "<elem />"', 'Element: attribute node removed')

# Check handling of namespace prefixes

e.setAttribute('xmlns', 'http://defaulturi')
e.setAttribute('xmlns:html', 'http://htmluri')
check('e.ns_prefix[""] == "http://defaulturi"',
      'Default namespace with setAttribute')
check('e.ns_prefix["html"] == "http://htmluri"',
      'Prefixed namespace with setAttribute')
e.removeAttribute('xmlns:html')
check('not e.ns_prefix.has_key("html")',
      'Prefixed namespace with removeAttribute')
e.removeAttribute('xmlns')

check('len(e.ns_prefix) == 0', 'Default namespace with removeAttribute')

default = doc.createAttribute('xmlns') ; default.value = "http://defaulturi"
html = doc.createAttribute('xmlns:html') ; html.value = "http://htmluri"

e.setAttributeNode(default) ; e.setAttributeNode(html)
check('e.ns_prefix[""] == "http://defaulturi"',
      'Default namespace with setAttributeNode')
check('e.ns_prefix["html"] == "http://htmluri"',
      'Prefixed namespace with setAttributeNode')
e.removeAttributeNode(html)
check('not e.ns_prefix.has_key("html")',
      'Prefixed namespace with removeAttribute')
e.removeAttributeNode(default)


#
# Check getElementsByTagName
#
check('len(e.getElementsByTagName("elem")) == 0', 
      "getElementsByTagName doesn't return element")

check('len(e.getElementsByTagName("*")) == 0', 
      "getElementsByTagName doesn't return element")


# Check CharacterData interfaces using Text nodes

t1 = doc.createText('first') ;  e.appendChild( t1 )
t2 = doc.createText('second') ; e.appendChild( t2 )
t3 = doc.createText('third') ;  e.appendChild( t3 )
check('e.toxml() == "<elem>firstsecondthird</elem>"', 
      "Element: content of three Text nodes as children")
check('len(e.childNodes) == 3', 'Element: three Text nodes as children')

e.normalize()
check('e.toxml() == "<elem>firstsecondthird</elem>"', 
      "Element: normalized Text nodes")

check('len(e.childNodes) == 1', 'Element: should be one normalized Text node')
check('t2.parentNode == None', 'Element: normalized t2 should have no parent')
check('t3.parentNode == None', 'Element: normalized t3 should have no parent')

# Text node

t1.splitText(5)
check('e.toxml() == "<elem>firstsecondthird</elem>"', 
      "Element: newly split Text nodes")
check('len(e.childNodes) == 2', 'Text: should be two split Text nodes')
check('e.lastChild.toxml() == "secondthird"', 
      "Element: newly split Text nodes")

# Check comparisons; e1 and e2 are different proxies for the same underlying 
# node

e1 = doc.documentElement ; e2 = doc.documentElement
check('e1 is not e2', 'Two proxies are different according to "is" operator')
check('e1 == e2', 'Two proxies are identical according to "==" operator')

# Done at last!
print 'Test suite completed'

