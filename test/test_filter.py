import pprint
import sys

from xml.dom import xmlbuilder, expatbuilder, Node
from xml.dom.NodeFilter import NodeFilter

class Filter(xmlbuilder.DOMBuilderFilter):
    whatToShow = NodeFilter.SHOW_ELEMENT

    def startNode(self, node):
        assert node.nodeType == Node.ELEMENT_NODE
        if node.tagName == "skipthis":
            return xmlbuilder.SKIP
        elif node.tagName == "rejectbefore":
            return xmlbuilder.REJECT
        else:
            return xmlbuilder.ACCEPT

    def endNode(self, node):
        assert node.nodeType == Node.ELEMENT_NODE
        if node.tagName == "rejectafter":
            return xmlbuilder.REJECT
        else:
            return xmlbuilder.ACCEPT


class RecordingFilter:
    whatToShow = NodeFilter.SHOW_ALL

    def __init__(self):
        self.events = []

    def startNode(self, node):
        self.events.append(("start", node.nodeType, str(node.nodeName)))
        return xmlbuilder.ACCEPT

    def endNode(self, node):
        self.events.append(("end", node.nodeType, str(node.nodeName)))
        return xmlbuilder.ACCEPT


simple_options = xmlbuilder.Options()
simple_options.filter = Filter()
simple_options.namespaces = 0

record_options = xmlbuilder.Options()
record_options.namespaces = 0

def checkResult(src):
    print
    dom = expatbuilder.makeBuilder(simple_options).parseString(src)
    print dom.toxml()
    dom.unlink()

def checkFilterEvents(src, record, what=NodeFilter.SHOW_ALL):
    record_options.filter = RecordingFilter()
    record_options.filter.whatToShow = what
    dom = expatbuilder.makeBuilder(record_options).parseString(src)
    if record != record_options.filter.events:
        print
        print "Received filter events:"
        pprint.pprint(record_options.filter.events)
        print
        print "Expected filter events:"
        pprint.pprint(record)
    dom.unlink()


# a simple case of skipping an element
checkResult("<doc><e><skipthis>text<e/>more</skipthis>abc</e>xyz</doc>")

# skip an element nested indirectly within another skipped element
checkResult('''\
<doc>Text.
  <skipthis>Nested text.
    <skipthis>Nested text in skipthis element.</skipthis>
    More nested text.
  </skipthis>Outer text.</doc>
''')

# skip an element nested indirectly within another skipped element
checkResult('''\
<doc>Text.
  <skipthis>Nested text.
    <nested-element>
      <skipthis>Nested text in skipthis element.</skipthis>
      More nested text.
    </nested-element>
    More text.
  </skipthis>Outer text.</doc>
''')

checkResult("<doc><rejectbefore/></doc>")

checkResult("<doc><rejectafter/></doc>")

checkResult('''\
<doc><rejectbefore>
  Text.
  <?my processing instruction?>
  <more stuff="foo"/>
  <!-- a comment -->
</rejectbefore></doc>
''')

checkResult('''\
<doc><rejectafter>
  Text.
  <?my processing instruction?>
  <more stuff="foo"/>
  <!-- a comment -->
</rejectafter></doc>
''')

# Make sure the document element is not passed to the filter:
checkResult("<rejectbefore/>")
checkResult("<rejectafter/>")

checkFilterEvents("<doc/>", [])
checkFilterEvents("<doc attr='value'/>", [])
checkFilterEvents("<doc><e/></doc>", [
    ("start", Node.ELEMENT_NODE, "e"),
    ("end", Node.ELEMENT_NODE, "e"),
    ])

src = "<doc><e><?pi data?><!--comment--></e></doc>"

checkFilterEvents(src, [
    ("start", Node.ELEMENT_NODE, "e"),
    ("start", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("end", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("start", Node.COMMENT_NODE, "#comment"),
    ("end", Node.COMMENT_NODE, "#comment"),
    ("end", Node.ELEMENT_NODE, "e"),
    ])

# Show everything except a couple of things to the filter, to check
# that whatToShow is implemented.  This isn't sufficient to be a
# black-box test, but will get us started.

checkFilterEvents(src, [
    ("start", Node.ELEMENT_NODE, "e"),
    ("start", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("end", Node.PROCESSING_INSTRUCTION_NODE, "pi"),
    ("end", Node.ELEMENT_NODE, "e"),
    ], what=NodeFilter.SHOW_ALL & ~NodeFilter.SHOW_COMMENT)

checkFilterEvents(src, [
    ("start", Node.ELEMENT_NODE, "e"),
    ("start", Node.COMMENT_NODE, "#comment"),
    ("end", Node.COMMENT_NODE, "#comment"),
    ("end", Node.ELEMENT_NODE, "e"),
    ], what=NodeFilter.SHOW_ALL & ~NodeFilter.SHOW_PROCESSING_INSTRUCTION)
