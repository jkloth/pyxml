# test for xml.dom.minidom

import os.path
import sys
import traceback
from StringIO import StringIO
from test.test_support import verbose

import xml.dom
import xml.dom.minidom
import xml.parsers.expat

from xml.dom.minidom import parse, Node, Document, parseString


if __name__ == "__main__":
    base = sys.argv[0]
else:
    base = __file__
tstfile = os.path.join(os.path.dirname(base), "test.xml")
del base

def confirm(test, testname="Test"):
    if not test:
        print "Failed " + testname
        raise Exception

def testParseFromFile():
    dom = parse(StringIO(open(tstfile).read()))
    dom.unlink()
    confirm(isinstance(dom,Document))

def testGetElementsByTagName():
    dom = parse(tstfile)
    confirm(dom.getElementsByTagName("LI") == \
            dom.documentElement.getElementsByTagName("LI"))
    dom.unlink()

def testInsertBefore():
    dom = parseString("<doc><foo/></doc>")
    root = dom.documentElement
    elem = root.childNodes[0]
    nelem = dom.createElement("element")
    root.insertBefore(nelem, elem)
    confirm(len(root.childNodes) == 2
            and root.childNodes[0] is nelem
            and root.childNodes[1] is elem
            and root.firstChild is nelem
            and root.lastChild is elem
            and root.toxml() == "<doc><element/><foo/></doc>"
            , "testInsertBefore -- node properly placed in tree")
    nelem = dom.createElement("element")
    root.insertBefore(nelem, None)
    confirm(len(root.childNodes) == 3
            and root.childNodes[1] is elem
            and root.childNodes[2] is nelem
            and root.lastChild is nelem
            and nelem.previousSibling is elem
            and root.toxml() == "<doc><element/><foo/><element/></doc>"
            , "testInsertBefore -- node properly placed in tree")
    nelem2 = dom.createElement("bar")
    root.insertBefore(nelem2, nelem)
    confirm(len(root.childNodes) == 4
            and root.childNodes[2] is nelem2
            and root.childNodes[3] is nelem
            and nelem2.nextSibling is nelem
            and nelem.previousSibling is nelem2
            and root.toxml() == "<doc><element/><foo/><bar/><element/></doc>"
            , "testInsertBefore -- node properly placed in tree")
    dom.unlink()

def testAppendChild():
    dom = parse(tstfile)
    dom.documentElement.appendChild(dom.createComment( "Hello"))
    confirm(dom.documentElement.childNodes[-1].nodeName == "#comment")
    confirm(dom.documentElement.childNodes[-1].data == "Hello")
    dom.unlink()

def testLegalChildren():
    dom = Document()
    elem = dom.createElement('element')
    text = dom.createTextNode('text')

    try: dom.appendChild(text)
    except xml.dom.HierarchyRequestErr: pass
    else:
        print "dom.appendChild didn't raise HierarchyRequestErr"

    dom.appendChild(elem)
    try: dom.insertBefore(text, elem)
    except xml.dom.HierarchyRequestErr: pass
    else:
        print "dom.appendChild didn't raise HierarchyRequestErr"

    try: dom.replaceChild(text, elem)
    except xml.dom.HierarchyRequestErr: pass
    else:
        print "dom.appendChild didn't raise HierarchyRequestErr"

    nodemap = elem.attributes
    try: nodemap.setNamedItem(text)
    except xml.dom.HierarchyRequestErr: pass
    else:
        print "NamedNodeMap.setNamedItem didn't raise HierarchyRequestErr"

    try: nodemap.setNamedItemNS(text)
    except xml.dom.HierarchyRequestErr: pass
    else:
        print "NamedNodeMap.setNamedItemNS didn't raise HierarchyRequestErr"

    elem.appendChild(text)
    dom.unlink()

def testNonZero():
    dom = parse(tstfile)
    confirm(dom)# should not be zero
    dom.appendChild(dom.createComment("foo"))
    confirm(not dom.childNodes[-1].childNodes)
    dom.unlink()

def testUnlink():
    dom = parse(tstfile)
    dom.unlink()

def testElement():
    dom = Document()
    dom.appendChild(dom.createElement("abc"))
    confirm(dom.documentElement)
    dom.unlink()

def testAAA():
    dom = parseString("<abc/>")
    el = dom.documentElement
    el.setAttribute("spam", "jam2")
    confirm(el.toxml() == '<abc spam="jam2"/>', "testAAA")
    dom.unlink()

def testAAB():
    dom = parseString("<abc/>")
    el = dom.documentElement
    el.setAttribute("spam", "jam")
    el.setAttribute("spam", "jam2")
    confirm(el.toxml() == '<abc spam="jam2"/>', "testAAB")
    dom.unlink()

def testAddAttr():
    dom = Document()
    child = dom.appendChild(dom.createElement("abc"))

    child.setAttribute("def", "ghi")
    confirm(child.getAttribute("def") == "ghi")
    confirm(child.attributes["def"].value == "ghi")

    child.setAttribute("jkl", "mno")
    confirm(child.getAttribute("jkl") == "mno")
    confirm(child.attributes["jkl"].value == "mno")

    confirm(len(child.attributes) == 2)

    child.setAttribute("def", "newval")
    confirm(child.getAttribute("def") == "newval")
    confirm(child.attributes["def"].value == "newval")

    confirm(len(child.attributes) == 2)
    dom.unlink()

def testDeleteAttr():
    dom = Document()
    child = dom.appendChild(dom.createElement("abc"))

    confirm(len(child.attributes) == 0)
    child.setAttribute("def", "ghi")
    confirm(len(child.attributes) == 1)
    del child.attributes["def"]
    confirm(len(child.attributes) == 0)
    dom.unlink()

def testRemoveAttr():
    dom = Document()
    child = dom.appendChild(dom.createElement("abc"))

    child.setAttribute("def", "ghi")
    confirm(len(child.attributes) == 1)
    child.removeAttribute("def")
    confirm(len(child.attributes) == 0)

    dom.unlink()

def testRemoveAttrNS():
    dom = Document()
    child = dom.appendChild(
            dom.createElementNS("http://www.python.org", "python:abc"))
    child.setAttributeNS("http://www.w3.org", "xmlns:python",
                                            "http://www.python.org")
    child.setAttributeNS("http://www.python.org", "python:abcattr", "foo")
    confirm(len(child.attributes) == 2)
    child.removeAttributeNS("http://www.python.org", "abcattr")
    confirm(len(child.attributes) == 1)

    dom.unlink()

def testRemoveAttributeNode():
    dom = Document()
    child = dom.appendChild(dom.createElement("foo"))
    child.setAttribute("spam", "jam")
    confirm(len(child.attributes) == 1)
    node = child.getAttributeNode("spam")
    child.removeAttributeNode(node)
    confirm(len(child.attributes) == 0)

    dom.unlink()

def testChangeAttr():
    dom = parseString("<abc/>")
    el = dom.documentElement
    el.setAttribute("spam", "jam")
    confirm(len(el.attributes) == 1)
    el.setAttribute("spam", "bam")
    confirm(len(el.attributes) == 1)
    el.attributes["spam"] = "ham"
    confirm(len(el.attributes) == 1)
    el.setAttribute("spam2", "bam")
    confirm(len(el.attributes) == 2)
    el.attributes[ "spam2"] = "bam2"
    confirm(len(el.attributes) == 2)
    dom.unlink()

def testGetAttrList():
    pass

def testGetAttrValues(): pass

def testGetAttrLength(): pass

def testGetAttribute(): pass

def testGetAttributeNS(): pass

def testGetAttributeNode(): pass

def testGetElementsByTagNameNS():
    d="""<foo xmlns:minidom="http://pyxml.sf.net/minidom">
    <minidom:myelem/>
    </foo>"""
    dom = parseString(d)
    elem = dom.getElementsByTagNameNS("http://pyxml.sf.net/minidom","myelem")
    confirm(len(elem) == 1)
    dom.unlink()

def testGetEmptyNodeListFromElementsByTagNameNS(): pass

def testElementReprAndStr():
    dom = Document()
    el = dom.appendChild(dom.createElement("abc"))
    string1 = repr(el)
    string2 = str(el)
    confirm(string1 == string2)
    dom.unlink()

# commented out until Fredrick's fix is checked in
def _testElementReprAndStrUnicode():
    dom = Document()
    el = dom.appendChild(dom.createElement( "abc"))
    string1 = repr(el)
    string2 = str(el)
    confirm(string1 == string2)
    dom.unlink()

# commented out until Fredrick's fix is checked in
def _testElementReprAndStrUnicodeNS():
    dom = Document()
    el = dom.appendChild(
        dom.createElementNS( "http://www.slashdot.org",  "slash:abc"))
    string1 = repr(el)
    string2 = str(el)
    confirm(string1 == string2)
    confirm(string1.find("slash:abc") != -1)
    dom.unlink()

def testAttributeRepr():
    dom = Document()
    el = dom.appendChild(dom.createElement( "abc"))
    node = el.setAttribute("abc", "def")
    confirm(str(node) == repr(node))
    dom.unlink()

def testTextNodeRepr(): pass

def testWriteXML():
    str = '<?xml version="1.0" ?>\n<a b="c"/>'
    dom = parseString(str)
    domstr = dom.toxml()
    dom.unlink()
    confirm(str == domstr)

def testProcessingInstruction(): pass

def testProcessingInstructionRepr(): pass

def testTextRepr(): pass

def testWriteText(): pass

def testDocumentElement(): pass

def testTooManyDocumentElements():
    doc = parseString("<doc/>")
    elem = doc.createElement("extra")
    try:
        doc.appendChild(elem)
    except xml.dom.HierarchyRequestErr:
        pass
    else:
        print "Failed to catch expected exception when" \
              " adding extra document element."
    elem.unlink()
    doc.unlink()

def testCreateElementNS(): pass

def testCreateAttributeNS(): pass

def testParse(): pass

def testParseString(): pass

def testComment(): pass

def testAttrListItem(): pass

def testAttrListItems(): pass

def testAttrListItemNS(): pass

def testAttrListKeys(): pass

def testAttrListKeysNS(): pass

def testAttrListValues(): pass

def testAttrListLength(): pass

def testAttrList__getitem__(): pass

def testAttrList__setitem__(): pass

def testSetAttrValueandNodeValue(): pass

def testParseElement(): pass

def testParseAttributes(): pass

def testParseElementNamespaces(): pass

def testParseAttributeNamespaces(): pass

def testParseProcessingInstructions(): pass

def testChildNodes(): pass

def testFirstChild(): pass

def testHasChildNodes(): pass

def testCloneElementShallow():
    dom, clone = _setupCloneElement(0)
    confirm(len(clone.childNodes) == 0
            and clone.parentNode is None
            and clone.toxml() == '<doc attr="value"/>'
            , "testCloneElementShallow")
    dom.unlink()

def testCloneElementDeep():
    dom, clone = _setupCloneElement(1)
    confirm(len(clone.childNodes) == 1
            and clone.parentNode is None
            and clone.toxml() == '<doc attr="value"><foo/></doc>'
            , "testCloneElementDeep")
    dom.unlink()

def _setupCloneElement(deep):
    dom = parseString("<doc attr='value'><foo/></doc>")
    root = dom.documentElement
    clone = root.cloneNode(deep)
    _testCloneElementCopiesAttributes(
        root, clone, "testCloneElement" + (deep and "Deep" or "Shallow"))
    # mutilate the original so shared data is detected
    root.tagName = root.nodeName = "MODIFIED"
    root.setAttribute("attr", "NEW VALUE")
    root.setAttribute("added", "VALUE")
    return dom, clone

def _testCloneElementCopiesAttributes(e1, e2, test):
    attrs1 = e1.attributes
    attrs2 = e2.attributes
    keys1 = attrs1.keys()
    keys2 = attrs2.keys()
    keys1.sort()
    keys2.sort()
    confirm(keys1 == keys2, "clone of element has same attribute keys")
    for i in range(len(keys1)):
        a1 = attrs1.item(i)
        a2 = attrs2.item(i)
        confirm(a1 is not a2
                and a1.value == a2.value
                and a1.nodeValue == a2.nodeValue
                and a1.namespaceURI == a2.namespaceURI
                and a1.localName == a2.localName
                , "clone of attribute node has proper attribute values")
        confirm(a2.ownerElement is e2,
                "clone of attribute node correctly owned")


def testCloneDocumentShallow(): pass

def testCloneDocumentDeep(): pass

def testCloneAttributeShallow(): pass

def testCloneAttributeDeep(): pass

def testClonePIShallow(): pass

def testClonePIDeep(): pass

def testNormalize():
    doc = parseString("<doc/>")
    root = doc.documentElement
    root.appendChild(doc.createTextNode("first"))
    root.appendChild(doc.createTextNode("second"))
    confirm(len(root.childNodes) == 2, "testNormalize -- preparation")
    doc.normalize()
    confirm(len(root.childNodes) == 1
            and root.firstChild is root.lastChild
            and root.firstChild.data == "firstsecond"
            , "testNormalize -- result")
    doc.unlink()

    doc = parseString("<doc/>")
    root = doc.documentElement
    root.appendChild(doc.createTextNode(""))
    doc.normalize()
    confirm(len(root.childNodes) == 0,
            "testNormalize -- single empty node removed")
    doc.unlink()

def testSiblings():
    doc = parseString("<doc><?pi?>text?<elm/></doc>")
    root = doc.documentElement
    (pi, text, elm) = root.childNodes

    confirm(pi.nextSibling is text and
            pi.previousSibling is None and
            text.nextSibling is elm and
            text.previousSibling is pi and
            elm.nextSibling is None and
            elm.previousSibling is text, "testSiblings")

    doc.unlink()

def testParents():
    doc = parseString("<doc><elm1><elm2/><elm2><elm3/></elm2></elm1></doc>")
    root = doc.documentElement
    elm1 = root.childNodes[0]
    (elm2a, elm2b) = elm1.childNodes
    elm3 = elm2b.childNodes[0]

    confirm(root.parentNode is doc and
            elm1.parentNode is root and
            elm2a.parentNode is elm1 and
            elm2b.parentNode is elm1 and
            elm3.parentNode is elm2b, "testParents")

    doc.unlink()

def testSAX2DOM():
    from xml.dom import pulldom

    sax2dom = pulldom.SAX2DOM()
    sax2dom.startDocument()
    sax2dom.startElement("doc", {})
    sax2dom.characters("text")
    sax2dom.startElement("subelm", {})
    sax2dom.characters("text")
    sax2dom.endElement("subelm")
    sax2dom.characters("text")
    sax2dom.endElement("doc")
    sax2dom.endDocument()

    doc = sax2dom.document
    root = doc.documentElement
    (text1, elm1, text2) = root.childNodes
    text3 = elm1.childNodes[0]

    confirm(text1.previousSibling is None and
            text1.nextSibling is elm1 and
            elm1.previousSibling is text1 and
            elm1.nextSibling is text2 and
            text2.previousSibling is elm1 and
            text2.nextSibling is None and
            text3.previousSibling is None and
            text3.nextSibling is None, "testSAX2DOM - siblings")

    confirm(root.parentNode is doc and
            text1.parentNode is root and
            elm1.parentNode is root and
            text2.parentNode is root and
            text3.parentNode is elm1, "testSAX2DOM - parents")

    doc.unlink()

class UserDataHandler:
    called = 0
    def handle(self, operation, key, data, src, dst):
        dst.setUserData(key, data + 1, self)
        src.setUserData(key, None, None)
        self.called = 1

def testUserData():
    n = xml.dom.minidom.Element('e')
    confirm(n.getUserData("foo") is None)
    n.setUserData("foo", None, None)
    confirm(n.getUserData("foo") is None)
    n.setUserData("foo", 12, 12)
    n.setUserData("bar", 13, 13)
    confirm(n.getUserData("foo") == 12)
    confirm(n.getUserData("bar") == 13)
    n.setUserData("foo", None, None)
    confirm(n.getUserData("foo") is None)
    confirm(n.getUserData("bar") == 13)

    handler = UserDataHandler()
    n.setUserData("bar", 12, handler)
    c = n.cloneNode(1)
    confirm(handler.called
            and n.getUserData("bar") is None
            and c.getUserData("bar") == 13)

def testRenameAttribute():
    doc = parseString("<doc a='v'/>")
    elem = doc.documentElement
    attrmap = elem.attributes
    attr = elem.attributes['a']

    # Simple renaming
    attr = doc.renameNode(attr, xml.dom.EMPTY_NAMESPACE, "b")
    confirm(attr.name == "b"
            and attr.nodeName == "b"
            and attr.localName is None
            and attr.namespaceURI == xml.dom.EMPTY_NAMESPACE
            and attr.prefix is None
            and attr.value == "v"
            and elem.getAttributeNode("a") is None
            and elem.getAttributeNode("b").isSameNode(attr)
            and attrmap["b"].isSameNode(attr)
            and attr.ownerDocument.isSameNode(doc)
            and attr.ownerElement.isSameNode(elem))

    # Rename to have a namespace, no prefix
    attr = doc.renameNode(attr, "http://xml.python.org/ns", "c")
    confirm(attr.name == "c"
            and attr.nodeName == "c"
            and attr.localName == "c"
            and attr.namespaceURI == "http://xml.python.org/ns"
            and attr.prefix is None
            and attr.value == "v"
            and elem.getAttributeNode("a") is None
            and elem.getAttributeNode("b") is None
            and elem.getAttributeNode("c").isSameNode(attr)
            and elem.getAttributeNodeNS(
                "http://xml.python.org/ns", "c").isSameNode(attr)
            and attrmap["c"].isSameNode(attr)
            and attrmap[("http://xml.python.org/ns", "c")].isSameNode(attr))

    # Rename to have a namespace, with prefix
    attr = doc.renameNode(attr, "http://xml.python.org/ns2", "p:d")
    confirm(attr.name == "p:d"
            and attr.nodeName == "p:d"
            and attr.localName == "d"
            and attr.namespaceURI == "http://xml.python.org/ns2"
            and attr.prefix == "p"
            and attr.value == "v"
            and elem.getAttributeNode("a") is None
            and elem.getAttributeNode("b") is None
            and elem.getAttributeNode("c") is None
            and elem.getAttributeNodeNS(
                "http://xml.python.org/ns", "c") is None
            and elem.getAttributeNode("p:d").isSameNode(attr)
            and elem.getAttributeNodeNS(
                "http://xml.python.org/ns2", "d").isSameNode(attr)
            and attrmap["p:d"].isSameNode(attr)
            and attrmap[("http://xml.python.org/ns2", "d")].isSameNode(attr))

    # Rename back to a simple non-NS node
    attr = doc.renameNode(attr, xml.dom.EMPTY_NAMESPACE, "e")
    confirm(attr.name == "e"
            and attr.nodeName == "e"
            and attr.localName is None
            and attr.namespaceURI == xml.dom.EMPTY_NAMESPACE
            and attr.prefix is None
            and attr.value == "v"
            and elem.getAttributeNode("a") is None
            and elem.getAttributeNode("b") is None
            and elem.getAttributeNode("c") is None
            and elem.getAttributeNode("p:d") is None
            and elem.getAttributeNodeNS(
                "http://xml.python.org/ns", "c") is None
            and elem.getAttributeNode("e").isSameNode(attr)
            and attrmap["e"].isSameNode(attr))

    try:
        doc.renameNode(attr, "http://xml.python.org/ns", "xmlns")
    except xml.dom.NamespaceErr:
        pass
    else:
        print "expected NamespaceErr"

    checkRenameNodeSharedConstraints(doc, attr)

def testRenameElement():
    doc = parseString("<doc/>")
    elem = doc.documentElement

    # Simple renaming
    elem = doc.renameNode(elem, xml.dom.EMPTY_NAMESPACE, "a")
    confirm(elem.tagName == "a"
            and elem.nodeName == "a"
            and elem.localName is None
            and elem.namespaceURI == xml.dom.EMPTY_NAMESPACE
            and elem.prefix is None
            and elem.ownerDocument.isSameNode(doc))

    # Rename to have a namespace, no prefix
    elem = doc.renameNode(elem, "http://xml.python.org/ns", "b")
    confirm(elem.tagName == "b"
            and elem.nodeName == "b"
            and elem.localName == "b"
            and elem.namespaceURI == "http://xml.python.org/ns"
            and elem.prefix is None
            and elem.ownerDocument.isSameNode(doc))

    # Rename to have a namespace, with prefix
    elem = doc.renameNode(elem, "http://xml.python.org/ns2", "p:c")
    confirm(elem.tagName == "p:c"
            and elem.nodeName == "p:c"
            and elem.localName == "c"
            and elem.namespaceURI == "http://xml.python.org/ns2"
            and elem.prefix == "p"
            and elem.ownerDocument.isSameNode(doc))

    # Rename back to a simple non-NS node
    elem = doc.renameNode(elem, xml.dom.EMPTY_NAMESPACE, "d")
    confirm(elem.tagName == "d"
            and elem.nodeName == "d"
            and elem.localName is None
            and elem.namespaceURI == xml.dom.EMPTY_NAMESPACE
            and elem.prefix is None
            and elem.ownerDocument.isSameNode(doc))

    checkRenameNodeSharedConstraints(doc, elem)

def checkRenameNodeSharedConstraints(doc, node):
    # Make sure illegal NS usage is detected:
    try:
        doc.renameNode(node, "http://xml.python.org/ns", "xmlns:foo")
    except xml.dom.NamespaceErr:
        pass
    else:
        print "expected NamespaceErr"

    doc2 = parseString("<doc/>")
    try:
        doc2.renameNode(node, xml.dom.EMPTY_NAMESPACE, "foo")
    except xml.dom.WrongDocumentErr:
        pass
    else:
        print "expected WrongDocumentErr"

def testRenameOther():
    # We have to create a comment node explicitly since not all DOM
    # builders used with minidom add comments to the DOM.
    doc = xml.dom.minidom.getDOMImplementation().createDocument(
        xml.dom.EMPTY_NAMESPACE, "e", None)
    node = doc.createComment("comment")
    try:
        doc.renameNode(node, xml.dom.EMPTY_NAMESPACE, "foo")
    except xml.dom.NotSupportedErr:
        pass
    else:
        print "expected NotSupportedErr when renaming comment node"

def testWholeText():
    doc = parseString("<doc>a</doc>")
    elem = doc.documentElement
    text = elem.childNodes[0]
    assert text.nodeType == Node.TEXT_NODE

    def checkText(node, s):
        t = node.wholeText
        confirm(t == s, "looking for %s, found %s" % (repr(s), repr(t)))

    checkText(text, "a")
    elem.appendChild(doc.createTextNode("b"))
    checkText(text, "ab")
    elem.insertBefore(doc.createCDATASection("c"), text)
    checkText(text, "cab")

    # make sure we don't cross other nodes
    splitter = doc.createComment("comment")
    elem.appendChild(splitter)
    text2 = doc.createTextNode("d")
    elem.appendChild(text2)
    checkText(text, "cab")
    checkText(text2, "d")

    x = doc.createElement("x")
    elem.replaceChild(x, splitter)
    splitter = x
    checkText(text, "cab")
    checkText(text2, "d")

    x = doc.createProcessingInstruction("y", "z")
    elem.replaceChild(x, splitter)
    splitter = x
    checkText(text, "cab")
    checkText(text2, "d")

    elem.removeChild(splitter)
    checkText(text, "cabd")
    checkText(text2, "cabd")


# --- MAIN PROGRAM

names = globals().keys()
names.sort()

failed = []

for name in names:
    if name[:4]=="test":
        func = globals()[name]
        try:
            func()
        except:
            failed.append(name)
            oldstdout = sys.stdout
            sys.stdout = StringIO()
            try:
                print "Test Failed: " + name
                sys.stdout.flush()
                traceback.print_exc()
                print sys.exc_info()[1]
                oldstdout.write(sys.stdout.getvalue())
            finally:
                sys.stdout = oldstdout
            raise

if failed:
    print "\n\n\n**** Check for failures in these tests:"
    for name in failed:
        print "  " + name
