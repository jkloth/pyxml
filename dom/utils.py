
import re
from xml.dom import core

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


class FileReader:
    """This class makes it really easy to get a DOM tree from a 
    file.  

    The following subclass would allow an HTML or XML file to be
    pretty printed with a single line of code (a pretty silly example
    but it's just an example):

    class DomDumper(FileReader)
         def __init__(self,filename):
              FileReader.__init__(self,filename)
              self.document.dump()

    d = DomDumper(sys.argv[1])
    """

    def __init__(self,filename=None):
        self.filename = filename
        if filename is not None:
            self.document = self.readFile(filename)

    def readFile(self, filename, file = None):
        """Given an XML, HTML, or SGML filename with appropriate
        file extension, return the DOM document."""

        type = self.getFileType(filename)
        if file is None:
            file = open(filename,'r')
            document = self.readStream(file,type)
            file.close()
        else:
            document = self.readStream(file,type)
        return document

    def readStream(self,stream, type='XML'):
        if type == 'XML':
            document = self.readXml(stream)
        elif type == 'HTML':
            document = self.readHtml(stream)
        elif type == 'SGML':
            document = self.readSgml(stream)
        else:
            document = None
        self.document = document
        return document

    def readXml(self,stream,parserName=None):
        """parserName could be 'pyexpat', 'sgmlop', etc."""
        from xml.sax import saxexts
        from xml.dom.sax_builder import SaxBuilder
        p = saxexts.make_parser(parserName)
        dh = SaxBuilder()
        p.setDocumentHandler(dh)
        p.feed(stream.read())
        doc = dh.document
        p.close()
        return doc

    def readHtml(self,stream):
        from xml.dom import html_builder
        b = html_builder.HtmlBuilder()
        b.feed(stream.read())
        b.close()
        doc = b.document
        # There was some bug that prevents the builder from
        # freeing itself (maybe it has already been fixed?).
        # The next two lines break its references to the DOM
        # tree so that it can be freed.
        b.document = None
        b.current_element = None
        return doc
    
    def readSgml(self, stream):
        # Don't know much about this part.  This could call SX to
        # convert the SGML to XML, then read it in.  That's what I
        # do for some SGML files I need to convert.  Any suggestions?
        raise RuntimeError, "This is not implemented."

    def getFileType(self,filename):
        """Given a filename, figure out if the file contains XML,
        HTML, or SGML.  For now, use the file extension to make the
        determination.""" 

        import os
        filename = string.lower(filename)
        (name,ext) = os.path.splitext(filename)
        
        if ext in ('.htm','.html'):
            type = 'HTML'
        elif ext in ('.sgm','.sgml'):
            type = 'SGML'
        elif ext == '.xml':
            type = 'XML'
        else:
            type = '' # should this return None instead?
        return type


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        d = FileReader()
        dom = d.readFile(sys.argv[1])
        print dom.toxml()
#        dom.dump()
    else:
        print "Usage: python %s <?ML filename>" % sys.argv[0]


