from xml.dom.core import *

class Walker:
    def walk(self, root):
        if root.get_nodeType() == DOCUMENT_NODE:
            c = root.get_documentElement()
            assert c.get_nodeType() == ELEMENT_NODE
            return self.walk1(c)
        else:
            return self.walk1(root)
                
    def walk1(self, node):
        type = node.get_nodeType()
        if type == ELEMENT_NODE:
            self.startElement(node)
            for child in node.get_childNodes():
                self.walk1(child)
            self.endElement(node)
        elif type == COMMENT_NODE:
            self.doComment(node)
        elif type == TEXT_NODE:
            self.doText(node)
        else:
            self.doOtherNode( node )

    def startElement(self, node):
        pass

    def endElement(self, node):
        pass
    
    def doText(self, node):
        pass

    def doComment(self, node):
        pass

    def doOtherNode(self, node):
        pass

        
