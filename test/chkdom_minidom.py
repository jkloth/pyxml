import unittest

import xml.dom.expatbuilder
import xml.dom.minidom

from domapi import DOMImplementationTestSuite


def DOMParseString(self, xml):
    return xml.dom.expatbuilder.parseString(xml)

def test_suite():
    """Return a test suite for the Zope testing framework."""
    return DOMImplementationTestSuite(xml.dom.minidom.getDOMImplementation(),
                                      DOMParseString)

def main():
    unittest.TextTestRunner().run(test_suite())

if __name__ == "__main__":
    main()