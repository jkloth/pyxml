"""writer: writer/lineariser classes for dumping DOM tree to file.

"""

from xml.dom.core import *
from xml.dom.walker import Walker
import string, re, sys

from xml.utils import escape
    

class OutputStream:
    def __init__(self, file):
        self.file = file
        self.new_line = 1

    def write(self, s):
        #print 'write', `s`
        self.file.write(re.sub('\n+', '\n', s))
        if s and s[-1] == '\n':
            self.new_line = 1
        else:
            self.new_line = 0

    def newLine(self):
        if not self.new_line:
            self.write('\n')

    def __del__(self):
        self.file.flush()


class XmlWriter(Walker):

    def __init__(self, stream=sys.stdout, nl_dict={}):
        self.stream = OutputStream(stream)
        self.empties = []
        self.strip = []
        self.xml_style_endtags = 1
        self.newline_before_start = []
        self.newline_after_start = []
        self.newline_before_end = []
        self.newline_after_end = []
        self.map_attr = self.map_tag = lambda x: x
        self._setNewLines(nl_dict)

    def _setNewLines(self,nl_dict):
        for k, v in nl_dict.items():
            if v[0]:
                self.newline_before_start.append(k)
                self.newline_before_start.append(string.upper(k))
            if v[1]:
                self.newline_after_start.append(k)
                self.newline_after_start.append(string.upper(k))
            if v[2]:
                self.newline_before_end.append(k)
                self.newline_before_end.append(string.upper(k))
            if v[3]:
                self.newline_after_end.append(k)
                self.newline_after_end.append(string.upper(k))

    def write(self, x):
        if type(x) == type(''):
            self.stream.write(x)
        elif type(x) in (type(()), type([])):
            for y in x:
                self.write(y)
        else:
            self.walk(x)


    def startElement(self, element) :
        assert element.get_nodeType() == ELEMENT

        s = '<%s' % self.map_tag(element.get_nodeName() )
        
        for name, value in element.get_attributes().items():
            s = s + ' %s="%s"' % (self.map_attr(name),
                          escape(value.get_nodeValue() ))

        if self.xml_style_endtags and not element.get_childNodes():
            s = s + '/>'
        else:
            s = s + '>'

        if element.get_nodeName() in self.newline_before_start:
            self.stream.newLine()
        self.stream.write(s)
        if element.get_nodeName() in self.newline_after_start:
            self.stream.newLine()


    def endElement(self, element):
        assert element.get_nodeType() == ELEMENT

        s = ''
        if element.get_nodeName() in self.empties :
            pass
        elif len(element.get_childNodes() ) == 0 and self.xml_style_endtags:
            pass
        else:
            s = s + '</%s>' % self.map_tag(element.get_nodeName() )

        if element.get_nodeName() in self.newline_before_end:
            self.stream.newLine()
        self.stream.write(s)
        if element.get_nodeName() in self.newline_after_end:
            self.stream.newLine()


    def doText(self, text_node):
        #if text_node.getParentNode().tagName in self.strip:
        #    data = string.strip(text_node.data)
        #else:
        data = text_node.get_nodeValue()
        self.stream.write(escape(data))

    def doComment(self, node):
        self.stream.write(node.toxml())


class XmlLineariser(XmlWriter):

    def __init__(self):
        import StringIO
        self.buffer = StringIO.StringIO()
        XmlWriter.__init__(self, self.buffer)

    def linearise(self, node):
        self.write(node)
        return self.buffer.getvalue()
    

class HtmlWriter(XmlWriter):
    def __init__(self, stream=sys.stdout):
        XmlWriter.__init__(self, stream)
        self.map_attr = self.map_tag = string.upper
        self.xml_style_endtags = 0

        self.empties = [
            'img', 'br', 'hr', 'include', 'li', 'meta', 'input',
            'IMG', 'BR', 'HR', 'INCLUDE', 'LI', 'META', 'INPUT',
        ]
        self.strip = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
            'li', 'br', 'p', 'a', 'title', 'font',
            'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 
            'LI', 'BR', 'P', 'A', 'TITLE', 'FONT',
        ]

        nl_dict = {
            'head': (1, 1, 1, 1),
            'body': (1, 1, 1, 1),
            'title': (1, 1, 1, 1),
            'meta': (1, 1, 0, 0),
            'ul': (1, 1, 1, 1),
            'li': (1, 0, 0, 0),
            'h1': (1, 0, 0, 1),
            'h2': (1, 0, 0, 1),
            'h3': (1, 0, 0, 1),
            'h4': (1, 0, 0, 1),
            'h5': (1, 0, 0, 1),
            'h6': (1, 0, 0, 1),
            'p': (1, 0, 0, 1),
            'br': (1, 1, 0, 0),
        }
        
        self._setNewLines(nl_dict)


class HtmlLineariser(HtmlWriter):

    def __init__(self):
        import StringIO
        self.buffer = StringIO.StringIO()
        HtmlWriter.__init__(self, self.buffer)

    def linearise(self, node):
        self.write(node)
        return self.buffer.getvalue()
    

class ASPWriter(XmlWriter):
    def __init__(self, rep_file):
        self.rep_dict = {}
        self.parseRepFile(rep_file)
        

    def parseRepFile(self, rep_file):
        s = ''
        for l in open(rep_file).readlines():
            if l[0] == '<':
                plus_before = 0
                plus_after = 0
                n = string.index(l, '>')
                tag_name = l[1:n]
                rep = string.strip(l[n+1:])
                if rep and rep[0] == '+':
                    plus_before = 1
                    rep = string.strip(rep[1:])
                if rep and rep[-1] == '+':
                    plus_after = 1
                    rep = string.strip(rep[:-1])
                if rep:
                    self.rep_dict[tag_name] = (plus_before, plus_after, eval(rep))
                else:
                    self.rep_dict[tag_name] = (plus_before, plus_after, '')
                    

    def linearise_element(self, element) :
        assert element.NodeType == ELEMENT
        s = ''
        
        # Start tag
        plus_before, plus_after, repl = self.rep_dict[element.getTagName()]

        if s and s[-1] != '\n' and plus_before:
            s = s + '\n'
        s = s + repl
        if s and s[-1] != '\n' and plus_after:
            s = s + '\n'

        s1 = ''
        for child in element.getChildren():
            if child.NodeType is ELEMENT:
                s1 = s1 + self.linearise_element(child)
            elif child.NodeType is TEXT:
                #s1 = s1 + escape(child.data)
                s1 = s1 + child.data
            else :
                s1 = s1 + str(child)
        
        s = s + s1

        # End tag.
        plus_before, plus_after, repl = self.rep_dict['/' + element.getTagName()]
        if s and s[-1] != '\n' and plus_before:
            s = s + '\n'
        s = s + repl
        if s and s[-1] != '\n' and plus_after:
            s = s + '\n'

        return s

