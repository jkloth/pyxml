from xml.parsers.xmlproc.utils import validate_doc, load_dtd, ErrorPrinter
import sys

dtd = load_dtd("xmlval_illformed.dtd")

f=open("doc.xml","w")
f.write("""<?xml version="1.0"?>
<!DOCTYPE configuration SYSTEM "xmlval_illformed.dtd">
<configuration><notallowed/></configuration>""")
f.close()

# validate_doc(dtd, "doc.xml")
# validate_doc is not suitable since it prints to stderr
from xml.parsers.xmlproc import xmlval

parser=xmlval.XMLValidator()
parser.dtd=dtd # FIXME: what to do if there is a !DOCTYPE?
parser.set_error_handler(ErrorPrinter(parser, out=sys.stdout))
parser.parse_resource("doc.xml")