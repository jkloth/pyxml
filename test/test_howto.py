
# Test suite containing code from the XML HOWTO

# SAX testing code

print "SAX tests:\n"

from xml.sax import saxlib, saxexts
import StringIO
import string

comic_xml = StringIO.StringIO("""<collection>
  <comic title="Sandman" number='62'>
    <writer>Neil Gaiman</writer>
    <penciller pages='1-9,18-24'>Glyn Dillon</penciller>
    <penciller pages="10-17">Charles Vess</penciller>
  </comic>
  <comic title="Shade, the Changing Man" number="7">
    <writer>Peter Milligan</writer>
    <penciller>Chris Bachalo</penciller>
  </comic>
</collection>""")

class FindIssue(saxlib.HandlerBase):
    def __init__(self, title, number):
        self.search_title, self.search_number = title, number

    def startElement(self, name, attrs):
        # If it's not a comic element, ignore it
        if name != 'comic': return

        # Look for the title and number attributes (see text)
        title = attrs.get('title', None)
        number = attrs.get('number', None)
        if title == self.search_title and number == self.search_number:
            print title, '#'+str(number), 'found'

    def error(self, exception):
        raise exception
    def fatalError(self, exception):
        raise exception

if 1:
    # Create a parser
    parser = saxexts.make_parser()

    # Create the handler
    dh = FindIssue('Sandman', '62')

    # Tell the parser to use our handler
    parser.setDocumentHandler(dh)
    parser.setErrorHandler(dh)

    # Parse the input
    parser.parseFile( comic_xml )

    # Close the parser
    parser.close()


def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join( string.split(text), ' ')

class FindWriter(saxlib.HandlerBase):
    def __init__(self, search_name):
        # Save the name we're looking for
        self.search_name = normalize_whitespace( search_name )

        # Initialize the flag to false
        self.inWriterContent = 0

    def startElement(self, name, attrs):
        # If it's a comic element, save the title and issue
        if name == 'comic':
            title = normalize_whitespace( attrs.get('title', "") )
            number = normalize_whitespace( attrs.get('number', "") )
            self.this_title = title
            self.this_number = number

        # If it's the start of a writer element, set flag
        elif name == 'writer':
            self.inWriterContent = 1
            self.writerName = ""

    def characters(self, ch, start, length):
        if self.inWriterContent:
            self.writerName = self.writerName + ch[start:start+length]

    def endElement(self, name):
        if name == 'writer':
            self.inWriterContent = 0
            self.writerName = normalize_whitespace(self.writerName)
            if self.writerName == self.search_name:
                print self.this_title, self.this_number

if 1:
    # Create a parser
    parser = saxexts.make_parser()

    # Create the handler
    dh = FindWriter('Peter Milligan')

    # Tell the parser to use our handler
    parser.setDocumentHandler(dh)
    parser.setErrorHandler(dh)

    # Print a title
    print '\nTitles by Peter Milligan:'

    # Parse the input
    comic_xml.seek(0)
    parser.parseFile( comic_xml )

    # Close the parser
    parser.close()


# DOM tests

print "DOM tests:\n"

import sys
from xml.sax import saxexts
from xml.dom.ext.reader.Sax import FromXml
from xml.dom.ext import PrettyPrint
#from xml.dom import utils

dom_xml = """<?xml version="1.0" encoding="iso-8859-1"?>
<xbel>  
  <?processing instruction?>
  <desc>No description</desc>
  <folder>
    <title>XML bookmarks</title>
    <bookmark href="http://www.python.org/sigs/xml-sig/" >
      <title>SIG for XML Processing in Python</title>
    </bookmark>
  </folder>
</xbel>"""

# Parse the input into a DOM tree
doc = FromXml(dom_xml)

# Print it
PrettyPrint(doc)

# whitespace-removal currently not supported
# utils.strip_whitespace( doc )
# print ' With whitespace removed:'
# print doc.toxml()

# Builder code

print 'DOM creation tests'

from xml.dom.DOMImplementation import implementation
d = implementation.createDocument(None, None, None)

# Create the root element
r = d.createElement("html")
d.appendChild(r)

# Create an empty 'head' element
r.appendChild(d.createElement("head"))

# Start the 'body' element, giving it an attribute
b = d.createElement("body")
b.setAttribute('background','#ffffff')
r.appendChild(b)

# Add a text node
b.appendChild(d.createTextNode("The body text goes here."))

# Print the document
PrettyPrint(d)
