#! /usr/bin/env python

# The seven examples from the Canonical XML spec.
# http://www.w3.org/TR/2001/REC-xml-c14n-20010315

eg1 = """<?xml version="1.0"?>

<?xml-stylesheet   href="doc.xsl"
   type="text/xsl"   ?>

<!DOCTYPE doc SYSTEM "doc.dtd">

<doc>Hello, world!<!-- Comment 1
--></doc>

<?pi-without-data     ?>

<!-- Comment 2 -->

<!-- Comment 3 -->
"""


eg2 = """<doc>
   <clean>   </clean>
   <dirty>   A   B   </dirty>
   <mixed>
      A
      <clean>   </clean>
      B
      <dirty>   A   B   </dirty>
      C
   </mixed>
</doc>
"""

eg3 = """<!DOCTYPE doc [<!ATTLIST e9 attr CDATA "default">]>
<doc>
   <e1   />
   <e2   ></e2>
   <e3    name = "elem3"   id="elem3"    />
   <e4    name="elem4"   id="elem4"    ></e4>
   <e5 a:attr="out" b:attr="sorted" attr2="all" attr="I'm"
       xmlns:b="http://www.ietf.org" 
       xmlns:a="http://www.w3.org"
       xmlns="http://example.org"/>
   <e6 xmlns="" xmlns:a="http://www.w3.org">
       <e7 xmlns="http://www.ietf.org">
           <e8 xmlns="" xmlns:a="http://www.w3.org">
               <e9 xmlns="" xmlns:a="http://www.ietf.org"/>
           </e8>
       </e7>
   </e6>
</doc>
"""

eg3 = """<!DOCTYPE doc [<!ATTLIST e9 attr CDATA "default">]>
<doc xmlns:foo="http://www.bar.org">
   <e1   />
   <e2   ></e2>
   <e3    name = "elem3"   id="elem3"    />
   <e4    name="elem4"   id="elem4"    ></e4>
   <e5 a:attr="out" b:attr="sorted" attr2="all" attr="I'm"
       xmlns:b="http://www.ietf.org" 
       xmlns:a="http://www.w3.org"
       xmlns="http://example.org"/>
   <e6 xmlns="" xmlns:a="http://www.w3.org">
       <e7 xmlns="http://www.ietf.org">
           <e8 xmlns="" xmlns:a="http://www.w3.org" a:foo="bar">
               <e9 xmlns="" xmlns:a="http://www.ietf.org"/>
           </e8>
       </e7>
   </e6>
</doc>
"""

eg4 = """<!DOCTYPE doc [ <!ATTLIST normId id ID #IMPLIED> <!ATTLIST normNames attr NMTOKENS #IMPLIED> ]> <doc>
   <text>First line&#x0d;&#10;Second line</text>
   <value>&#x32;</value>
   <compute><![CDATA[value>"0" && value<"10" ?"valid":"error"]]></compute>
   <compute expr='value>"0" &amp;&amp; value&lt;"10" ?"valid":"error"'>valid</compute>
   <norm attr=' &apos;   &#x20;&#13;&#xa;&#9;   &apos; '/>
   <normNames attr='   A   &#x20;&#13;&#xa;&#9;   B   '/>
   <normId id=' &apos;   &#x20;&#13;&#xa;&#9;   &apos; '/>
</doc>"""

eg5 = """<!DOCTYPE doc [
<!ATTLIST doc attrExtEnt ENTITY #IMPLIED>
<!ENTITY ent1 "Hello">
<!ENTITY ent2 SYSTEM "world.txt">
<!ENTITY entExt SYSTEM "earth.gif" NDATA gif>
<!NOTATION gif SYSTEM "viewgif.exe">
]>
<doc attrExtEnt="entExt">
   &ent1;, &ent2;!
</doc>

<!-- Let world.txt contain "world" (excluding the quotes) -->
"""

_eg6 = u"""<?xml version="1.0" encoding="ISO-8859-1"?>
<doc>&#169;</doc>"""
eg6 = _eg6.encode('latin')

eg7 = """<!DOCTYPE doc [
<!ATTLIST e2 xml:space (default|preserve) 'preserve'>
<!ATTLIST e3 id ID #IMPLIED>
]>
<doc xmlns="http://www.ietf.org" xmlns:w3c="http://www.w3.org">
   <e1>
      <e2 xmlns="">
         <e3 id="E3"/>
      </e2>
   </e1>
</doc>"""

# Make one-origined.
examples = [ eg1, eg2, eg3, eg4, eg5, eg6, eg7 ]

# Load XPath and Parser
import codecs, sys, types, traceback
from xml import xpath
from xml.xpath.Context import Context
from xml.dom.ext.reader import PyExpat
from xml.dom.ext import Canonicalize

# My special reader.
PYE = PyExpat.Reader
class ReaderforC14NExamples(PYE):
    '''A special reader to handle resolution of the C14N examples.
    '''
    def initParser(self):
	PYE.initParser(self)
        self.parser.ExternalEntityRefHandler = self.entity_ref

    def entity_ref(self, *args):
	if args != (u'ent2', None, u'world.txt', None): return 0
	self.parser.CharacterDataHandler('world')
	return 1

    # Override some methods from PyExpat.Reader
    def unparsedEntityDecl(self, *args): pass
    def notationDecl(self, *args): pass


utf8_writer = codecs.lookup('utf-8')[3]

def builtin():
    '''Run the builtin tests from the C14N spec.'''
    for num,eg in [(i+1, examples[i]) for i in range(len(examples))]:

	filename = 'out%d.xml' % num
	try:
	    os.unlink(filename)
	except:
	    pass

	print 'Doing %d, %s...' % (num, eg[0:30].replace('\n', '\\n')),

	r = ReaderforC14NExamples()
	try:
	    dom = r.fromString(eg)
	except Exception, e:
	    print '\nException', repr(e)
	    traceback.print_exc()
	    continue

	# Get the nodeset; the tests have some special cases.
	if eg == eg7:
	    con = Context(dom, processorNss={'ietf': 'http://www.ietf.org'})
	else:
	    con = Context(dom)
	if eg == eg5:
	    pattern = '(//. | //@* | //namespace::*)[not (self::comment())]'
	else:
	    pattern = '(//. | //@* | //namespace::*)'
	nodelist = xpath.Evaluate(pattern, context=con)

	outf = utf8_writer(open(filename, 'w'))

	# Canonicalize a DOM with a document subset list according to XML-C14N
	Canonicalize(dom, outf, subset=nodelist)

	outf.close()
	print 'Created ' + filename

def usage():
    print '''Options accepted:
    -b, --builtin            Run the C14N builtin tests
    -i file, --in=file       Read specified file* (default is stdin)
    -o file, --out=file      Write to specified file* (default is stdout)
    -h, --help               Print this text
    -x query, --xpath=query  Specify an XPATH nodelist
If file (for input/output) is like xxx,name then xxx is used as an
encoding (e.g., "utf-8,foo.txt").
'''

if len(sys.argv) == 1: sys.argv.append('-b')

import getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "hbi:o:x:",
	[ "help", "builtin", "in=", "out=", "xpath=", ])
except getopt.GetoptError, e:
    print sys.argv[0] + ':', e, '\nTry --help for help.\n'
    sys.exit(1)

IN, OUT = sys.stdin, sys.stdout
query = '(//. | //@* | //namespace::*)'
for opt,arg in opts:
    if opt in ('-h', '--help'):
	usage()
	sys.exit(0)
    if opt in ('-b', '--builtin'):
	builtin()
	sys.exit(0)
    elif opt in ('-i', '--in'):
	if arg.find(',') == -1:
	    IN = open(arg, 'r')
	else:
	    encoding, filename = arg.split(',')
	    reader = codecs.lookup(encoding)[2]
	    IN = reader(open(filename, 'r'))
    elif opt in ('-o', '--out'):
	if arg.find(',') == -1:
	    OUT = open(arg, 'w')
	else:
	    encoding, filename = arg.split(',')
	    writer = codecs.lookup(encoding)[3]
	    OUT = writer(open(filename, 'w'))
    elif opt in ('-x', '--xpath'):
	query = arg

r = PYE()
dom = r.fromStream(IN)
context = Context(dom)
nodelist = xpath.Evaluate(query, context=context)
c14n.Canonicalize(dom, OUT, subset=nodelist)
OUT.close()
