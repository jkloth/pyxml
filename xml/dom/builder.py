'''
Event-driven, almost-SAXish, grove builder.


'''

from xml.dom.core import *
import string

_LEGAL_DOCUMENT_CHILDREN = (ELEMENT_NODE, PROCESSING_INSTRUCTION_NODE,
                COMMENT_NODE)


class Builder:

    def __init__(self):
        self.document = createDocument()
        self.fragment = None
        self.target = self.document
        self.current_element = None

    def buildFragment(self):
        if self.fragment or len(self.document.childNodes):
            raise RuntimeError, \
                  "cannot build fragment once document has been started"
        self.fragment = self.document.createDocumentFragment()
        self.target = self.fragment
        return self.fragment

    def push(self, node):
        "Add node to current node and move to new node."

        nodetype = node.get_nodeType()
        if self.current_element is not None:
            self.current_element.insertBefore(node, None)
        elif self.fragment or nodetype in _LEGAL_DOCUMENT_CHILDREN:
            if nodetype == TEXT_NODE:
                if string.strip(node.get_nodeValue()) != "":
                    self.target.appendChild(node)
            else:
                self.target.appendChild(node)

        if nodetype == ELEMENT_NODE:
            self.current_element = node
        
    def pop(self):
        "Move to current node's parent."

        self.current_element = self.current_element.get_parentNode()
        

    def startElement(self, name, attrs = {}):
        if hasattr(self, 'start_' + name):
            getattr(self, 'start_' + name)(name, attrs)
        else:
            element = self.document.createElement(name)
            for key, value in attrs.items():
                element.setAttribute(key, value)
            self.push(element)
    
    def endElement(self, name):
        assert name == self.current_element.get_nodeName()
        self.pop()

    def comment(self,s):
        if self.current_element is not None:
            comment_node = self.document.createComment(s)
            self.current_element.insertBefore(comment_node, None)
    
    def processingInstruction(self, target, data):
        node = self.document.createProcessingInstruction(target, data)
        self.push(node)

    def entityref(self, name):
        node = self.document.createEntityReference(name)
        self.push(node)

    def text(self, s):
        if self.current_element is not None:
            text_node = self.document.createTextNode(s)
            if (self.current_element == self.document and
                string.strip(s) == ""):
                return

            self.current_element.insertBefore(text_node, None)


