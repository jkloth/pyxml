
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

# Don't build pyexpat if the Python installation provides one.
# FIXME: It should be build for binary distributions even if the core has it.
build_pyexpat = 0
try:
    import pyexpat
except ImportError:
    build_pyexpat = 1

if build_pyexpat:
    ext_modules.append(
        Extension('_xmlplus.parsers.pyexpat',
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
                                  

setup (name = "PyXML",
       version = "0.6.0", # Needs to match xml/__init__.version_info
       description = "Python/XML package",
       author = "XML-SIG",
       author_email = "xml-sig@python.org",
       url = "http://www.python.org/sigs/xml-sig/",
       long_description = "Long desc goes here",
       
       package_dir = {'_xmlplus':'xml'},
       
       packages = ['_xmlplus', 
                   '_xmlplus.dom', '_xmlplus.dom.html', '_xmlplus.dom.ext',
                   '_xmlplus.dom.ext.reader',
                   '_xmlplus.marshal',
                   '_xmlplus.parsers', '_xmlplus.parsers.xmlproc', 
                   '_xmlplus.sax', '_xmlplus.sax.drivers',
                   '_xmlplus.sax.drivers2',
                   '_xmlplus.unicode', '_xmlplus.utils'
                   ],

       ext_modules = ext_modules
       )

