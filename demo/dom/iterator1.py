"""Demonstrates basic walking using DOM level 2 iterators"""

from xml.dom.ext import ReleaseNode
from xml.dom.ext.reader import Sax2
from xml.dom.Node import Node
from xml.dom.NodeFilter import NodeFilter

def iterate(xml_dom_object):
    print "Printing all nodes:"
    nit = xml_dom_object.ownerDocument.createNodeIterator(xml_dom_object, NodeFilter.SHOW_ALL, None, 0)

    curr_node =  nit.nextNode()
    while curr_node:
        print "%s node %s\n"%(curr_node.nodeType, curr_node.nodeName)
        curr_node =  nit.nextNode()

    print "\n\n\nPrinting only element nodes:"
    snit = xml_dom_object.ownerDocument.createNodeIterator(xml_dom_object, NodeFilter.SHOW_ELEMENT, None, 0)

    curr_node =  snit.nextNode()
    while curr_node:
        print "%s node %s\n"%(curr_node.nodeType, curr_node.nodeName)
        curr_node = snit.nextNode()


if __name__ == '__main__':
    import sys
    try:
        xml_dom_object = Sax2.FromXmlFile(sys.argv[1], validate=0)
    except Sax.saxlib.SAXException, msg:
        print "SAXException caught:", msg
    except Sax.saxlib.SAXParseException, msg:
        print "SAXParseException caught:", msg

    iterate(xml_dom_object)
    ReleaseNode(xml_dom_object)

    
