
# Setup script for the XML tools
#
# Targets: build test install help

import sys, os, string

from distutils.core import setup, Extension
from setupext import Data_Files, install_Data_Files

# I want to override the default build directory so the extension
# modules are compiled and placed in the build/xml directory
# tree.  This is a bit clumsy, but I don't see a better way to do
# this at the moment. 

# Use either unixfilemap or readfilemap depending on the platform
if sys.platform == 'win32':
    FILEMAP_SRC = 'extensions/expat/xmlwf/win32filemap.c'
elif sys.platform[:3] == 'mac':
    FILEMAP_SRC = 'extensions/expat/xmlwf/readfilemap.c'
else:
    # Assume all other platforms are Unix-compatible; this is almost
    # certainly wrong. :)
    FILEMAP_SRC = 'extensions/expat/xmlwf/unixfilemap.c'

ext_modules = []

# Rename xml to _xmlplus for Python 2.0

if sys.hexversion < 0x2000000:
  def xml(s):
    return "xml"+s
else:
  def xml(s):
    return "_xmlplus"+s

# Don't build pyexpat if the Python installation provides one.
# FIXME: It should be build for binary distributions even if the core has it.
build_pyexpat = 0
try:
    import pyexpat
    # The following features of are required by PyXML from pyexpat,
    # which are not available in older versions:
    # ExternalEntityParserCreate, available only from 2.25 on.
    # ParseFile throws exception, not available up to 2.28.
    if pyexpat.__version__ <= '2.28':
        build_pyexpat = 1
    if 'pyexpat' in sys.builtin_module_names:
        print "Error: builtin expat library will conflict with ours"
        print "Re-build python without builtin expat module"
        raise SystemExit
except ImportError:
    build_pyexpat = 1

if build_pyexpat:
    ext_modules.append(
        Extension(xml('.parsers.pyexpat'),
                  define_macros = [('XML_NS', None),
                                   ('XML_DTD',None),
                                   ('EXPAT_VERSION','0x010200')],
                  include_dirs = [ 'extensions/expat/xmltok',
                                   'extensions/expat/xmlparse' ], 
                  sources = [ 'extensions/pyexpat.c',
                              'extensions/expat/xmltok/xmltok.c',
                              'extensions/expat/xmltok/xmlrole.c',
                              'extensions/expat/xmlwf/xmlfile.c',
                              'extensions/expat/xmlwf/xmlwf.c',
                              'extensions/expat/xmlwf/codepage.c',
                              'extensions/expat/xmlparse/xmlparse.c',
                              # Gone in 1.2
                              #'extensions/expat/xmlparse/hashtable.c',
                              FILEMAP_SRC,
                              ]
                  ))

# Build sgmlop
ext_modules.append(
  Extension(xml('.parsers.sgmlop'), sources=['extensions/sgmlop.c']))


# On Windows, install the documentation into a directory xmldoc, along
# with xml/_xmlplus. For RPMs, docs are installed into the RPM doc
# directory via setup.cfg (usuall /usr/doc). On all other systems, the
# documentation is not installed.

doc2xmldoc = 1
if sys.platform == 'win32':
    doc2xmldoc = 1

# This is a fragment from MANIFEST.in which should contain all
# files which are considered documentation (doc, demo, test, plus some
# toplevel files)
docfiles="""
recursive-include doc *.html 
recursive-include doc *.tex 
recursive-include doc *.txt 
recursive-include doc *.gif 
recursive-include doc *.css
recursive-include doc *.api
recursive-include doc *.web

recursive-include demo README 
recursive-include demo *.py 
recursive-include demo *.xml
recursive-include demo *.dtd
recursive-include demo *.html
recursive-include demo *.htm
include demo/genxml/data.txt
include demo/dom/html2html
include demo/xbel/doc/xbel.bib
include demo/xbel/doc/xbel.tex
include demo/xmlproc/catalog.soc

recursive-include test *.py 
recursive-include test *.xml
include test/test.xml.out
recursive-include test/output test_*

include ANNOUNCE 
include CREDITS 
include LICENCE 
include README* 
include TODO 
"""

if doc2xmldoc:
    xmldocfiles = [
        Data_Files(copy_to = 'xmldoc',
                   template = string.split(docfiles,"\n"),
                   preserve_path = 1)
        ]
else:
    xmldocfiles = []

setup (name = "PyXML",
       version = "0.6.2", # Needs to match xml/__init__.version_info
       description = "Python/XML package",
       author = "XML-SIG",
       author_email = "xml-sig@python.org",
       url = "http://www.python.org/sigs/xml-sig/",
       long_description =
"""XML Parsers and API for Python
This version of PyXML was tested with Python 2.0 and 1.5.2.
""",

       # Override certain command classes with our own ones
       cmdclass = {'install_data':install_Data_Files}, 
       
       package_dir = {xml(''):'xml'},

       data_files = xmldocfiles,
       
       packages = [xml(''), 
                   xml('.dom'), xml('.dom.html'), xml('.dom.ext'),
                   xml('.dom.ext.reader'),
                   xml('.marshal'),
                   xml('.parsers'), xml('.parsers.xmlproc'), 
                   xml('.sax'), xml('.sax.drivers'),
                   xml('.sax.drivers2'), xml('.utils')
                   ],

       ext_modules = ext_modules
       )

