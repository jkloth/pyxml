from xml.dom.core import *

def explode(nodes, condition):
	for node in nodes:
		explode_node(node, condition)

	return nodes

def explode_node(node, condition):
	if node.NodeType != ELEMENT:
		return node

	explode(node.getChildren(), condition)

	if eval(condition, {}, {'this': node}):
		parent = node.getParentNode()
		for child in node.getChildren():
			parent.insertBefore(child, node)
		parent.removeChild(node)

	return node
		
		
if __name__ == '__main__':
	from xml.dom.pyhtml import *
	from xml.dom.writer import HtmlWriter

	tree = HTML(BODY(H1(A({'href':'blah'}, 'blah blah'))))
	w = HtmlWriter()
	w.write(tree)

	explode_node(tree, 'this.GI == "A"')
	w.write(tree)



			
			

