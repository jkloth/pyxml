"""
Demonstrates some advanced DOM manipulation.
This function looks for XLL-compliant simple links to an xml document,
and replaces the node containing such links with the contents of the referenced
document.
"""

from xml.dom.Node import Node
from xml.dom.NodeFilter import NodeFilter
from xml.dom import ext
from xml.dom.ext.reader import Sax2

def xll_replace(start_node):
    owner_doc = start_node.ownerDocument
    snit = owner_doc.createNodeIterator(start_node, NodeFilter.SHOW_ELEMENT, None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #Only empty nodes are allowed to have Links
        if not curr_node.childNodes.length and curr_node.attributes:
            is_link = 0
            href = None
            for k in curr_node.attributes.keys():
                if (curr_node.attributes[k].localName, curr_node.attributes[k].namespaceURI) == ("link", "http://www.w3.org/XML/XLink/0.9"):
                    is_link = 1
                elif (curr_node.attributes[k].localName, curr_node.attributes[k].namespaceURI) == ("href", "http://www.w3.org/XML/XLink/0.9"):
                    href = curr_node.attributes[k].value
            if is_link and href:
               #Then make a tree of the new file and insert it
                f = open(href, "r")
                str = f.read()
                new_df = Sax2.FromXml(str, ownerDocument=start_node.ownerDocument, validate=0)

                #Get the first element node and assume it's the document node
                for a_node in new_df.childNodes:
                    if a_node.nodeType == Node.ELEMENT_NODE:
                        doc_root = a_node
                        break
                curr_node.parentNode.replaceChild(doc_root, curr_node)
        curr_node = snit.nextNode()

    return start_node

if __name__ == "__main__":
    import sys
    xml_dom_tree = Sax2.FromXmlUrl(sys.argv[1], validate=0)
    xll_replace(xml_dom_tree)
    ext.PrettyPrint(xml_dom_tree)
    ext.ReleaseNode(xml_dom_tree)

