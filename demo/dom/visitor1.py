"""Demonstrates basic, pre-order DOM walking using the default, bare-bones visitor"""

from xml.dom import Node
from xml.dom.ext import Visitor
from xml.dom.ext.reader import Sax2
from xml.dom.ext import ReleaseNode

class NsVisitor(Visitor.Visitor):
    def visit(self, node):
        print "Node %s namespaceURI: '%s' qualified name: '%s' localName: '%s' prefix: '%s'\n"%(str(node), node.namespaceURI, node.nodeName, node.localName, node.prefix)
        if node.nodeType == Node.ELEMENT_NODE:
            for k in node.attributes.keys():
                print "Node %s namespaceURI: '%s' qualified name: '%s' localName: '%s' prefix: '%s'\n"%(str(node.attributes[k]), node.attributes[k].namespaceURI, node.attributes[k].nodeName, node.attributes[k].localName, node.attributes[k].prefix)
        return None


def walk(xml_dom_object):
    visitor = Visitor.Visitor()
    walker = Visitor.Walker(visitor, xml_dom_object)
    walker.run()

    visitor = NsVisitor()
    walker = Visitor.Walker(visitor, xml_dom_object)
    walker.run()


if __name__ == '__main__':
    import sys
    try:
        xml_dom_object = Sax2.FromXmlFile(sys.argv[1], validate=0)
    except Sax.saxlib.SAXException, msg:
        print "SAXException caught:", msg
    except Sax.saxlib.SAXParseException, msg:
        print "SAXParseException caught:", msg
    else:
        walk(xml_dom_object)
    ReleaseNode(xml_dom_object)

