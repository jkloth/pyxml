"""
A command-line interface to the validating xmlproc parser. Prints error
messages and can output the parsed data in various formats.
"""

usage=\
"""
Usage:

  xvcmd.py [-c catalog] [-l language] [-o format] [-n] [urltodoc]

  ---Options:  
  catalog:  path to catalog file to use to resolve public identifiers
  language: ISO 3166 language code for language to use in error messages
  format:   Format to output parsed XML. 'e': ESIS, 'x': canonical XML
            No data will be outputted if this option is not specified
  urltodoc: URL to the document to parse. (You can use plain file names
            as well.) Can be omitted if a catalog is specified and contains
            a DOCUMENT entry.
  -n:       Report qualified names as 'URI name'. (Namespace processing.)
            
  Catalog files with URLs that end in '.xml' are assumed to be XCatalogs,
  all others are assumed to be SGML Open Catalogs.

  If the -c option is not specified the environment variables XMLXCATALOG
  and XMLSOCATALOG will be used (in that order).
"""

from xml.parsers.xmlproc import xmlval,catalog,xcatalog,xmlproc
import sys,getopt,os,outputters

# --- Initialization

print "xmlproc version %s" % xmlval.version

p=xmlval.XMLValidator()
err=outputters.MyErrorHandler(p)

p.set_error_handler(err)

# --- Interpreting options

try:
    (options,sysids)=getopt.getopt(sys.argv[1:],"c:l:o:n")
except getopt.error,e:
    print "Usage error: "+e
    print usage
    sys.exit(1)
    
cat=None
pf=None
namespaces=0
app=xmlproc.Application()

for option in options:
    if option[0]=="-c":
        cat=option[1]
        pf=xcatalog.FancyParserFactory()
    elif option[0]=="-l":
        try:
            p.set_error_language(option[1])
        except KeyError:
            print "Error language '%s' not available" % option[1]
    elif option[0]=="-o":
        if option[1]=="e" or option[1]=="E":
            app=outputters.ESISDocHandler()            
        elif option[1]=="x" or option[1]=="X":
            app=outputters.Canonizer()
        else:
            print "Error: Unknown output format "+option[1]
            print usage
    elif option[0]=="-n":
        namespaces=1

# Acting on option settings
        
if namespaces:
    from xml.parsers.xmlproc import namespace

    nsf=namespace.NamespaceFilter(p)
    nsf.set_application(app)
    p.set_application(nsf)
else:
    p.set_application(app)
        
if cat==None and os.environ.has_key("XMLXCATALOG"):
    cat=os.environ["XMLXCATALOG"]
    pf=xcatalog.XCatParserFactory()
elif cat==None and os.environ.has_key("XMLSOCATALOG"):
    cat=os.environ["XMLSOCATALOG"]
    pf=catalog.CatParserFactory()

if cat!=None:
    print "Parsing catalog file '%s'" % cat
    cat=catalog.xmlproc_catalog(cat,pf)
    p.set_pubid_resolver(cat)

if len(sysids)==0:
    if cat==None:
        print "You must specify a system identifier if no catalog is used"
        print usage
        sys.exit(1)
    elif cat.get_document_sysid()==None:
        print "You must specify a system identifier if the catalog has no "+\
              "DOCUMENT entry"
        print usage
        sys.exit(1)

    sysids=[cat.get_document_sysid()]
    print "Parsing DOCUMENT '%s' from catalog" % sysids[0]

# --- Parsing

for sysid in sysids:
    print
    print "Parsing '%s'" % sysid
    p.parse_resource(sysid)
    print "Parse complete, %d error(s) and %d warning(s)" % \
          (err.errors,err.warnings)
    err.reset()
    p.reset()
