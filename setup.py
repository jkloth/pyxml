
# Setup script for the XML tools
#
# Targets: build test install help

import sys, os

from distutils.core import setup, Extension

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
except ImportError:
    build_pyexpat = 1

if build_pyexpat:
    ext_modules.append(
        Extension(xml('.parsers.pyexpat'),
                  define_macros = [('XML_NS', None)],
                  include_dirs = [ 'extensions/expat/xmltok',
                                   'extensions/expat/xmlparse' ], 
                  sources = [ 'extensions/pyexpat.c',
                              'extensions/expat/xmltok/xmltok.c',
                              'extensions/expat/xmltok/xmlrole.c',
                              'extensions/expat/xmlwf/xmlfile.c',
                              'extensions/expat/xmlwf/xmlwf.c',
                              'extensions/expat/xmlwf/codepage.c',
                              'extensions/expat/xmlparse/xmlparse.c',
                              'extensions/expat/xmlparse/hashtable.c',
                              FILEMAP_SRC,
                              ]
                  ))

# Build sgmlop
ext_modules.append(
  Extension(xml('.parsers.sgmlop'), sources=['extensions/sgmlop.c']))
                                  

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
       
       package_dir = {xml(''):'xml'},
       
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

