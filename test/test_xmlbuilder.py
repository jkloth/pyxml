"""Tests of the extended features of xml.dom.expatbuilder."""

import pprint
import sys

from cStringIO import StringIO

from xml.dom import XMLNS_NAMESPACE
from xml.dom import xmlbuilder


INTERNAL_SUBSET = "<!ELEMENT doc EMPTY>"
DOCUMENT_SOURCE = '<!DOCTYPE doc [' + INTERNAL_SUBSET + ''']>
<doc xmlns:a="http://xml.python.org/a"
     xmlns:A="http://xml.python.org/a"
     xmlns:b="http://xml.python.org/b"
     a:a="a" b:b="b"/>
'''


def check_attrs(atts, expected):
    assert atts.length == len(expected)
    info = atts.itemsNS()
    info.sort()
    if info != expected:
        raise AssertionError, "\n" + pprint.pformat(info)

def run_checks(document, attributes):
    source = xmlbuilder.DOMInputSource()
    source.byteStream = StringIO(DOCUMENT_SOURCE)
    document = builder.parse(source)

    if document.doctype.internalSubset != INTERNAL_SUBSET:
        raise ValueError, "internalSubset not properly initialized"
    check_attrs(document.documentElement.attributes, attributes)


builder = xmlbuilder.DOMBuilder()
builder.setFeature("namespace_declarations", 1)

run_checks(builder,
           [((XMLNS_NAMESPACE, "A"), "http://xml.python.org/a"),
            ((XMLNS_NAMESPACE, "a"), "http://xml.python.org/a"),
            ((XMLNS_NAMESPACE, "b"), "http://xml.python.org/b"),
            (("http://xml.python.org/a", "a"), "a"),
            (("http://xml.python.org/b", "b"), "b"),
            ])


builder.setFeature("namespace_declarations", 0)

run_checks(builder,
           [(("http://xml.python.org/a", "a"), "a"),
            (("http://xml.python.org/b", "b"), "b"),
            ])
