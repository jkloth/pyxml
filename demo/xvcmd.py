"""
A command-line interface to the xmlproc parser. It continues parsing
after even fatal errors, in order to be find more errors, since this
does not mean feeding data to the application after a fatal error
(which would be in violation of the spec).

Usage:

  xvcmd.py [-c catalog] [urltodoc]

  catalog:  path to catalog file to use to resolve public identifiers
  urltodoc: URL to the document to parse. (You can use plain file names
            as well.) Can be omitted if a catalog is specified and contains
            a DOCUMENT entry.

  Catalog files with URLs that end in '.xml' are assumed to be XCatalogs,
  all others are assumed to be SGML Open Catalogs.

  If the -c option is not specified the environment variables XMLXCATALOG
  and XMLSOCATALOG will be used (in that order).
"""

# --- INITIALIZATION

import sys,getopt,os
from xml.parsers.xmlproc import xmlval,catalog,xcatalog

# --- ERROR HANDLING

class MyErrorHandler(xmlval.ErrorHandler):

    def __init__(self,locator):
	xmlval.ErrorHandler.__init__(self,locator)
	self.errors=0
	self.warnings=0

    def get_location(self):
	return "%s:%d:%d" % (self.locator.get_current_sysid(),\
			     self.locator.get_line(),
			     self.locator.get_column())
	
    def warning(self,msg):
	print "WARNING ON %s: %s" % (self.get_location(),msg)
	self.warnings=self.warnings+1

    def error(self,msg):
	self.fatal(msg)
	
    def fatal(self,msg):
	print "%s: %s" % (self.get_location(),msg)
	self.errors=self.errors+1

# --- MAIN PROGRAM

# --- Initialization

print "xmlproc version %s" % xmlval.version

p=xmlval.XMLValidator()
err=MyErrorHandler(p)

p.set_error_handler(err)

# --- Interpreting options

(options,sysids)=getopt.getopt(sys.argv[1:],"c:")

if (len(options)>0 and options[0][0]=="-c") or \
   os.environ.has_key("XMLSOCATALOG") or \
   os.environ.has_key("XMLXCATALOG"):

    if len(options)>0:
        sysid=options[0][1]
        pf=xcatalog.FancyParserFactory()
    elif os.environ.has_key("XMLXCATALOG"):
        sysid=os.environ["XMLXCATALOG"]
        pf=xcatalog.XCatParserFactory()
    else:
        sysid=os.environ["XMLSOCATALOG"]
        pf=catalog.CatParserFactory()
    
    print "Parsing catalog file '%s'" % sysid
    cat=catalog.xmlproc_catalog(sysid,pf)
    p.set_pubid_resolver(cat)
else:
    cat=None

if len(sysids)==1:
    sysid=sysids[0]
elif len(sysids)==0:
    if cat==None:
        print "You must specify a system identifier if no catalog is used"
        sys.exit(1)
    elif cat.get_document_sysid()==None:
        print "You must specify a system identifier if the catalog has no "+\
              "DOCUMENT entry"
        sys.exit(1)

    sysid=cat.get_document_sysid()
    print "Parsing DOCUMENT '%s' from catalog" % sysid

# --- Parsing

print
p.parse_resource(sysid)
print "\nParse complete, %d error(s) and %d warning(s)" % \
      (err.errors,err.warnings)

# try:
# except:
#     print "Error, parse aborted."
