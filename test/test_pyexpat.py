# Very simple test - Parse a file and print what happens
import sys
import os

try:
	from xml.parsers import pyexpat
except ImportError:
	# Possibly the pyexpat module hasn't been installed; we may be
	# running an initial "make test" just after compiling the
	# package.  Try importing pyexpat directly.
	import pyexpat
	 
	
class Outputter:
	def __init__(self, verbose=0):
		self.startcount = 0
		self.endcount = 0
		self.cdatacount = 0
		self.instcount = 0
		self.verbose = verbose

	def startelt(self, name, attrs):
		self.startcount = self.startcount + 1
		if self.verbose:
			print 'start', name
			for i in range(0, len(attrs), 2):
				print 'attr', attrs[i], attrs[i+1]

	def endelt(self, name):
		self.endcount = self.endcount + 1
		if self.verbose:
			print 'end', name

	def cdata(self, data):
		self.cdatacount = self.cdatacount + 1
		if self.verbose:
			print 'cdata', data

	def inst(self, target, data):
		self.instcount = self.instcount + 1
		if self.verbose:
			print 'inst', target, data

sys.argv[1:] = ["quotes.xml"]

out = Outputter(verbose = 1)
if len(sys.argv) != 2:
	if os.name == 'mac':
		import macfs
		fss, ok = macfs.StandardGetFile()
		if not ok: sys.exit(0)
		sys.argv.append(fss.as_pathname())
	else:
		print 'Usage: pyexpattest [-v] inputfile'
		sys.exit(1)
	
parser = pyexpat.ParserCreate()
parser.StartElementHandler = out.startelt
parser.EndElementHandler = out.endelt
parser.CharacterDataHandler = out.cdata
parser.ProcessingInstructionHandler = out.inst

data = open(sys.argv[1]).read()

try:
	parser.Parse(data, 1)
except pyexpat.error:
	print '** Error', parser.ErrorCode
	print '** Line', parser.ErrorLineNumber
	print '** Column', parser.ErrorColumnNumber
	print '** Byte', parser.ErrorByteIndex
print 'Summary of XML parser upcalls:'
print 'start elements:', out.startcount
print 'end elements:', out.endcount
print 'character data:', out.cdatacount
print 'processing instructions:', out.instcount
