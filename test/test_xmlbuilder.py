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
            raise AssertionError, "\n" + pprint.pformat(info)

    def run_checks(self, attributes):
        document = self.builder.parse(self.makeSource(DOCUMENT_SOURCE))

        if document.doctype.internalSubset != INTERNAL_SUBSET:
            raise ValueError, (
                "internalSubset not properly initialized; found:\n"
                + repr(document.doctype.internalSubset))
        if document.doctype.entities.length != 1:
            raise ValueError, "entity not stored in doctype"
        node = document.doctype.entities['e']
        if (  node.notationName is not None
              or node.publicId is not None
              or node.systemId != 'http://xml.python.org/entity/e'):
            raise ValueError, "bad entity information"
        if document.doctype.notations.length != 1:
            raise ValueError, "notation not stored in doctype"
        node = document.doctype.notations['x']
        if (  node.publicId is not None
              or node.systemId != 'http://xml.python.org/notation/x'):
            raise ValueError, "bad notation information"
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


def test_main():
    import test_support
    test_support.run_suite(unittest.makeSuite(Tests))
