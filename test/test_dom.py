
import StringIO
from xml.dom import core, sax_builder
from xml.sax import saxexts

test_text = """<?xml version="1.0"?>
<doc>
<title>This is a test</title>
<h1>Don't panic</h1>
<p>Maybe it will work.</p>
<h2>We can handle it</h2>
<h3>Yes we can</h3>
<h3>Or maybe not</h3>
End of test.
</doc>
"""

p = saxexts.make_parser()
h = sax_builder.SaxBuilder()
p.setDocumentHandler( h )
file = StringIO.StringIO( test_text )
p.parseFile( file )

doc = h.document
print doc.toxml()



