'''Test module to thest the xmllib module.
   Sjoerd Mullender
'''

# Copied from the Python 1.5.1 test suite.

from test_support import verbose

testdoc = """\
<?xml version="1.0" encoding="UTF-8" standalone='yes' ?>
<!-- comments aren't allowed before the <?xml?> tag,
     but they are allowed before the <!DOCTYPE> tag -->
<!DOCTYPE greeting [
  <!ELEMENT greeting (#PCDATA|empty)*>
  <!ELEMENT empty EMPTY>
]>

<greeting>
  <empty></empty>
  Hello, world!
  <empty/>
</greeting>
"""

from xml.parsers import xmllib
parser = xmllib.TestXMLParser()

for c in testdoc:
	parser.feed(c)
parser.close()
