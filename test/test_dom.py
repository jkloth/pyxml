from xml.dom.transformer import *
from xml.dom.writer import HtmlWriter

test_text = """<?xml>
<doc>
<title>This is a test</title>

<h1>Don't panic</h1>

<p>Maybe it will work.</p>

<h2>We can handle it</>

<h3>Yes we can</h3>
<h3>Or maybe not</h3>

End of test.
</doc>
"""


class TestTransformer(Transformer):
	def do_doc(self, node):
		return [HTML(
			HEAD(
				TITLE(cdata(having(node._children, 'this.GI == "title"')))
			),
			BODY(
				{'bgcolor': '#FFFFFF', 'text': '#000000'},
				having(node._children, 'this.GI in ["h1", "h2", "h3"]')
			)
		)]

transformer = TestTransformer()
parser = DcBuilder()
parser.feed(test_text)
document = transformer.transform(parser.document)

writer = HtmlWriter()
writer.write(document)
