
# Test suite containing code from the XML HOWTO

# SAX testing code
from xml.sax import saxlib, saxexts
import StringIO

comic_xml = StringIO.StringIO("""<collection>
  <comic title="Sandman" number='62'>
    <writer>Neil Gaiman</writer>
    <penciller pages='1-9,18-24'>Glyn Dillon</penciller>
    <penciller pages="10-17">Charles Vess</penciller>
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


