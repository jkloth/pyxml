
# Parser test suite:
# This checks if the test/xmltest directory

import os
from xml.sax import saxexts, saxlib

def test_parser(p):
    # Put a parser through its paces
    pass

def test_all_parsers():
    for parser in saxexts.XMLParserFactory.get_parser_list():
        try:
            p = saxexts.XMLParserFactory.make_parser( parser )
        except saxlib.SAXException:
            # The parser must not be available, so just silently move
            # on to the next parser
            pass
        else:
            test_parser( p )
            
if os.path.exists('xmltest/'):
    test_all_parsers()

