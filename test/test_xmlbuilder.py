"""Tests of the extended features of xml.dom.expatbuilder."""

import pprint
import unittest

from cStringIO import StringIO

from xml.dom import XMLNS_NAMESPACE
from xml.dom import xmlbuilder


INTERNAL_SUBSET = ("<!NOTATION x SYSTEM 'http://xml.python.org/notation/x'>\n"
                   "<!ENTITY e SYSTEM 'http://xml.python.org/entity/e'>")
DOCUMENT_SOURCE = (
    '<!DOCTYPE doc [' + INTERNAL_SUBSET.replace('\n', '\r\n') + ''']>
<doc xmlns:a="http://xml.python.org/a"
     xmlns:A="http://xml.python.org/a"
     xmlns:b="http://xml.python.org/b"
     a:a="a" b:b="b"/>
''')


class Tests(unittest.TestCase):

    def setUp(self):
        self.builder = xmlbuilder.DOMBuilder()

    def makeSource(self, text):
        source = xmlbuilder.DOMInputSource()
        source.byteStream = StringIO(text)
        return source

    def check_attrs(self, atts, expected):
        self.assertEqual(atts.length, len(expected))
        info = atts.itemsNS()
        info.sort()
        if info != expected:
            self.fail("bad attribute information:\n" + pprint.pformat(info))

    def run_checks(self, attributes):
        document = self.builder.parse(self.makeSource(DOCUMENT_SOURCE))

        self.assertEqual(document.doctype.internalSubset, INTERNAL_SUBSET)
        self.assertEqual(document.doctype.entities.length, 1,
                         "entity not stored in doctype")

        node = document.doctype.entities['e']
        self.assert_(node.notationName is None)
        self.assert_(node.publicId is None)
        self.assertEqual(node.systemId, 'http://xml.python.org/entity/e')
        self.assertEqual(document.doctype.notations.length, 1)

        node = document.doctype.notations['x']
        self.assert_(node.publicId is None)
        self.assertEqual(node.systemId, 'http://xml.python.org/notation/x')

        self.check_attrs(document.documentElement.attributes, attributes)

    def test_namespace_decls_on(self):
        self.builder.setFeature("namespace_declarations", 1)
        self.run_checks(#((nsuri, localName), value),
                        [((XMLNS_NAMESPACE, "A"), "http://xml.python.org/a"),
                         ((XMLNS_NAMESPACE, "a"), "http://xml.python.org/a"),
                         ((XMLNS_NAMESPACE, "b"), "http://xml.python.org/b"),
                         (("http://xml.python.org/a", "a"), "a"),
                         (("http://xml.python.org/b", "b"), "b"),
                         ])

    def test_namespace_decls_off(self):
        self.builder.setFeature("namespace_declarations", 0)
        self.run_checks(#((nsuri, localName), value),
                        [(("http://xml.python.org/a", "a"), "a"),
                         (("http://xml.python.org/b", "b"), "b"),
                         ])

    def test_get_element_by_id(self):
        ID_PREFIX = "<!DOCTYPE doc [ <!ATTLIST e id ID #IMPLIED> ]>"
        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + "<doc id='foo'><e id='foo'/></doc>"))
        self.assert_(doc.getElementById("bar") is None,
                     "received unexpected node")
        self.assertEqual(doc.getElementById("foo").nodeName, "e",
                         "did not get expected node")

        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + "<doc id='foo'><d id='foo'/><e id='foo'/></doc>"))
        self.assertEqual(doc.getElementById("foo").nodeName, "e",
                         "did not get expected node")

        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + ("<doc id='foo'><e id='foo' name='a'/>"
                         "<e id='bar' name='b'/></doc>")))
        self.assertEqual(doc.getElementById("foo").getAttribute("name"), "a",
                         "did not get expected node")

    def check_resolver(self, content_type, encoding):
        resolver = TestingResolver(content_type)
        source = resolver.resolveEntity(None, DUMMY_URL)
        self.assertEqual(source.encoding, encoding,
                         "wrong encoding; expected %s, got %s"
                         % (repr(encoding), repr(source.encoding)))

    def test_entity_resolver_encodings(self):
        self.check_resolver((None, None, []), None)
        self.check_resolver(("text", "plain", []), None)
        self.check_resolver(("text", "plain", ["charset=iso-8859-1"]),
                            "iso-8859-1")
        self.check_resolver(("text", "plain", ["charset=UTF-8"]), "utf-8")

    def test_internal_subset_isolation(self):
        document = self.builder.parse(self.makeSource(
            "<!DOCTYPE doc ["
            "<!-- comment --> <?pi foo?>"
            "]><doc/>"
            ))
        s = document.toxml()
        self.assertEqual(s, '<?xml version="1.0" ?>\n<doc/>')


DUMMY_URL = "http://xml.python.org/dummy.xml"

class TestingResolver(xmlbuilder.DOMEntityResolver):
    def __init__(self, content_type):
        self._content_type = content_type

    def _create_opener(self):
        return FakeOpener(self._content_type)

class FakeOpener:
    def __init__(self, content_type):
        self._content_type = content_type

    def open(self, url):
        if url != DUMMY_URL:
            raise ValueError, "unexpected URL: " + repr(url)
        return FakeFile(open("/dev/null", "rb"), self._content_type)

class FakeFile:
    def __init__(self, file, content_type):
        self._file = file
        self._content_type = content_type

    def info(self):
        return FakeMessage(self._content_type)

    def __getattr__(self, name):
        return getattr(self._file, name)

class FakeMessage:
    def __init__(self, content_type):
        self._maintype, self._subtype, self._plist = content_type

    def has_key(self, name):
        name = name.lower()
        if name != "content-type":
            raise ValueError, "unexpected has_key(%s)" % repr(name)
        return self._maintype is not None

    def getplist(self):
        return self._plist

    def getmaintype(self):
        return self._maintype or "text"

    def getsubtype(self):
        return self._subtype or "plain"

    def gettype(self):
        return "%s/%s" % (self.getmaintype(), self.getsubtype())


def test_suite():
    return unittest.makeSuite(Tests)

def test_main():
    import test_support
    test_support.run_suite(test_suite())

if __name__ == "__main__":
    import test_support
    test_support.verbose = 1
    test_main()
