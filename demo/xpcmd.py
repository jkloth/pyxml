
"""
A command-line interface to the xmlproc parser. It continues parsing
after even fatal errors, in order to be find more errors, since this
does not mean feeding data to the application after a fatal error
(which would be in violation of the spec).

Usage:

  [xpcmd.py] urltodoc

urltodoc: URL to the document to parse. (You can use plain file names
          as well.)
"""

# --- INITIALIZATION

import sys
from xml.parsers.xmlproc import xmlproc

# --- ERROR HANDLING

class MyErrorHandler(xmlproc.ErrorHandler):

    def __init__(self,loc):
	self.locator=loc
	self.errors=0
	self.warnings=0

    def get_location(self):
	return "%s:%d:%d" % (self.locator.get_current_sysid(),\
			     self.locator.get_line(),
			     self.locator.get_column())
	
    def warning(self,msg):
	print "WARNING ON %s:" % self.get_location()
	print "  "+msg
	self.warnings=self.warnings+1
    
    def fatal(self,msg):
	print "ERROR ON %s: " % self.get_location()
	print "  "+msg
	self.errors=self.errors+1
	sys.exit(1)

# --- MAIN PROGRAM
	
p=xmlproc.XMLProcessor()
err=MyErrorHandler(p)

p.set_error_handler(err)

print "Parsing document"

p.parse_resource(sys.argv[1])
print "Parse complete, %d error(s) and %d warning(s)" % \
      (err.errors,err.warnings)

# try:
# except:
#     print "Error, parse aborted."
