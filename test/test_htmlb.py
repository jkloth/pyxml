
# dom.html_builder tests

from xml.dom import html_builder

good_html = """
<html>
<P>I prefer (all things being equal) regularity/orthogonality and logical
syntax/semantics in a language because there is less to have to remember.
(Of course I <em>know</em> all things are NEVER really equal!)
<P CLASS=source>Guido van Rossum, 6 Dec 91
<P>The details of that silly code are irrelevant.
<P CLASS=source>Tim Peters, 4 Mar 92
&amp; &lt; &gt; &eacute; &ouml; &nbsp;
</html>
"""

bad_html = """
<html>
Interdigitated <b>bold and <i>italic</B> tags.</i>&amp; &lt; &gt; &eacute; &ouml; &nbsp;
</html>
"""

# Try the good output with both settings of ignore_mismatched_end_tags

print "Good document (no ignore)"
b = html_builder.HtmlBuilder() 
b.expand_entities = b.expand_entities + ('eacute',)
b.feed( good_html ) ; b.close()
print b.document.toxml()

print "Good document (ignoring mismatched end tags)"
b = html_builder.HtmlBuilder(ignore_mismatched_end_tags = 1)
b.expand_entities = b.expand_entities + ('eacute',)
b.feed( good_html ) ; b.close()
print b.document.toxml()

print "Bad document (no ignore)"
b = html_builder.HtmlBuilder()
try:
    b.feed( bad_html ) ; b.close()
except html_builder.BadHTMLError:
    print "Exception raised for bad HTML"
else:
    print "*** ERROR: no exception raised for bad HTML"

print "Bad document (ignoring mismatched end tags)"
b = html_builder.HtmlBuilder(ignore_mismatched_end_tags = 1)
b.feed( bad_html ) ; b.close()
print b.document.toxml()





