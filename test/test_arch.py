#!/usr/bin/env python
# Test script for xml.arch subpackage
# Derived from the complex.py example in the xmlarch distribution

# Import needed modules
from xml.sax import saxexts, saxlib, saxutils
from xml.arch import xmlarch

import sys, StringIO
input = StringIO.StringIO("""<?xml version="1.0"?>
<?test where="before"?>
<?IS10744:arch name ="biblio" renamer-att="bren" suppressor-att="bsup" ignore-data-att="bign" bridge-form="bibbrid"?>
<?IS10744:arch name ="html" suppressor-att="hsup" auto="ArcAuto" form-att="ht"?>
<?test where="after"?>

<!DOCTYPE doc [
<!ATTLIST content ht     CDATA  #FIXED   "body"     >
<!ATTLIST info    ht     CDATA  #FIXED   "title"    >
<!ATTLIST last    ht     CDATA  #FIXED   "#IMPLIED" >
<!ATTLIST test    ht     CDATA  #FIXED   "#IMPLIED" >
<!ATTLIST creator ht     CDATA  #FIXED   "#IMPLIED" >
<!ELEMENT init ANY >
<!ATTLIST init    id     ID     #REQUIRED           >
<!ATTLIST comment 
                  biblio CDATA  #FIXED   "note"
                  ht     CDATA  #FIXED   "address"  >
]>
<doc bsup="sArcForm">
  <front ht="#IMPLIED">
    <head biblio="title">
      <info date="19980721">A more complex sample</info>
    </head>
    <creator biblio="author" hsup="sArcAll" bsup="sArcNone" bign="cArcIgnD">
      <init id="abc123">Mr.</init>
      <first biblio="firstname" nationality="norwegian">Geir Ove</first> 
      <last biblio="lastname" updated="yes" bren="updated modified">Gronmo</last>
      <comment>You can reach me at <phone>12345678 or at </phone>grove@infotek.no</comment>
      <test ignore="maybe"/>
    </creator>
  </front>
  <content>
    <h1>The title</h1>
    <para ht="p" biblio="content" bsup="sArcNone">This is the <em ht="b">complex </em>document.</para>
  </content>
</doc>
""")

htmlout = StringIO.StringIO()
bib1out = StringIO.StringIO()
bib2out = StringIO.StringIO()
stdout = StringIO.StringIO()

# create architecture processor handler
arch_handler = xmlarch.ArchDocHandler()

# Create parser and register architecture processor with it
parser = saxexts.XMLParserFactory.make_parser()
parser.setDocumentHandler(arch_handler)

# Add an document handlers to process the html and biblio architectures
arch_handler.add_document_handler("html",
                                  xmlarch.Prettifier( htmlout ))
arch_handler.add_document_handler("biblio",
                                  saxutils.ESISDocHandler( bib1out ))
arch_handler.add_document_handler("biblio",
                                  saxutils.Canonizer( bib2out ))

# Register a default document handler that just passes through any incoming events
arch_handler.set_default_document_handler(xmlarch.Prettifier(stdout))

# Parse (and process) the document
parser.parseFile(input)

print 'HTML output:', htmlout.getvalue()
print 'Bib1 output:', bib1out.getvalue()
print 'Bib2 output:', bib2out.getvalue()
