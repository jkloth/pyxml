
import re

# Various utility functions that are often handy.

def tree_print(node, indent = 0):
    """Print a representation of a tree that makes the tree structure explicit.
    Intended mostly for debugging use, so it's a lossy printout."""
    s = indent*' ' + repr(node) + '\n'
    for n in node.get_childNodes():
        s = s + tree_print(n, indent + 2)
    return s
    
# this should grow up into a general-purpose whitespace post-processor,
# options to include:
#   - whether to strip (s/\s+//) or collapse (s/\s+/ /)
#   - where to do it: head, tail, or interior of text nodes, or
#                     all-whitespace nodes only
# Initial implementation by Greg Ward; modified and collapse_whitespace added
# by AMK.

import string
WS_LEFT, WS_BOTH, WS_RIGHT, WS_INTERNAL = [1,2,3,4]

strip_func = {WS_LEFT: string.lstrip,
              WS_BOTH: string.strip,
              WS_RIGHT: string.rstrip }

collapse_pat = {WS_LEFT: '^\s+',
                WS_BOTH: '(^\s+)|(\s+$)',
                WS_RIGHT: '\s+$',
                WS_INTERNAL: '\s+'}
                
def strip_whitespace (node, func = WS_BOTH):
    """Remove leading and/or trailing whitespace from a DOM tree.
    node -- top node; its subtree will be traversed
    func -- one of WS_LEFT, WS_RIGHT, WS_BOTH telling which whitespace to strip
    """
    if func == WS_INTERNAL:
        raise ValueError, "WS_INTERNAL not acceptable value for strip_whitespace()"
    func = strip_func[func]
    if node.nodeType == core.DOCUMENT_NODE:
        node = node.documentElement

    stack = [node]

    while (stack):
        # get the top node from the stack
        node = stack[-1]
        # XXX a general-purpose "visit" operation could go right here

        # walk this node's list of children, deleting those that are
        # all whitespace and saving the rest to be pushed onto the stack
        children = []
        for child in node.childNodes[:] :
            if child.nodeType == core.TEXT_NODE:
                orig = child.get_nodeValue()
                v = func( orig )
                if v == "":
                    node.removeChild (child)
                elif v != orig:
                    child.set_nodeValue( v )
            elif child.hasChildNodes():
                children.append (child)
        children.reverse()
        stack[-1:] = children
        
    # end: while stack not empty

# end strip_whitespace

def collapse_whitespace (node, func = WS_BOTH):
    """Collapse runs of whitespace down to a single space.
    
    node -- top node; its subtree will be traversed
    func -- one of WS_LEFT, WS_RIGHT, WS_BOTH, WS_INTERNAL telling which
            whitespace should be collapsed.  
    """
    pat = collapse_pat[ func ]
    pat = re.compile( pat )
    if node.nodeType == core.DOCUMENT_NODE:
        node = node.documentElement

    stack = [node]

    while (stack):
        # get the top node from the stack
        node = stack[-1]
        # XXX a general-purpose "visit" operation could go right here

        # walk this node's list of children, deleting those that are
        # all whitespace and saving the rest to be pushed onto the stack
        children = []
        
        for child in node.childNodes[:] :
            if child.nodeType == core.TEXT_NODE:
                orig = child.get_nodeValue()
                v = pat.sub(' ', orig)
                if v != orig:
                    child.set_nodeValue( v )
            elif child.hasChildNodes():
                children.append (child)
        children.reverse()
        stack[-1:] = children
        
    # end: while stack not empty

# end collapse_whitespace
