
# A demo SAX application using the xmllib.py driver, a command-line
# interface and the ESIS outputter.

from xml.sax import saxexts, saxlib, saxutils

import sys,StringIO

in_sysID="quotes.xml"

for klass in [saxutils.Canonizer, saxutils.ESISDocHandler]:
    output = StringIO.StringIO()
    dh = klass(output)
    p=saxexts.make_parser()
    p.setDocumentHandler(dh)
    p.parse(in_sysID)
    print output.getvalue()
    
