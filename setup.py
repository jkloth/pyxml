#! /usr/bin/env python

# Setup script for the XML tools
#
# Targets: build install help

import sys, os, string

from distutils.core import setup, Extension
from setupext import Data_Files, install_Data_Files, wininst_request_delete

# I want to override the default build directory so the extension
# modules are compiled and placed in the build/xml directory
# tree.  This is a bit clumsy, but I don't see a better way to do
# this at the moment.

ext_modules = []

# Rename xml to _xmlplus for Python 2.x

if sys.hexversion < 0x2000000:
    def xml(s):
        return "xml"+s
else:
    def xml(s):
        return "_xmlplus"+s

# special command-line arguments
LIBEXPAT = None
LDFLAGS = []

args = sys.argv[:]
extra_packages = []
with_xpath = 1
with_xslt = 1

for arg in args:
    if string.find(arg, '--with-libexpat=') == 0:
        LIBEXPAT = string.split(arg, '=')[1]
        sys.argv.remove(arg)
    elif string.find(arg, '--ldflags=') == 0:
        LDFLAGS = string.split(string.split(arg, '=')[1])
        sys.argv.remove(arg)
    elif arg == '--with-xpath':
        with_xpath = 1
        sys.argv.remove(arg)
    elif arg == '--with-xslt':
        with_xslt = 1
	sys.argv.remove(arg)
    elif arg == '--without-xpath':
        with_xpath = 0
        sys.argv.remove(arg)
    elif arg == '--without-xslt':
        with_xslt = 0
	sys.argv.remove(arg)

if sys.platform[:6] == "darwin": # Mac OS X
    LDFLAGS.append('-flat_namespace')

if with_xpath:
    extra_packages.append(xml('.xpath'))

if with_xslt:
    extra_packages.append(xml('.xslt'))

def get_expat_prefix():
    if LIBEXPAT:
        return LIBEXPAT

    # XXX temporarily disable usage of installed expat
    # until we figure out a way to determine its version
    return

    for p in ("/usr", "/usr/local"):
        incs = os.path.join(p, "include")
        libs = os.path.join(p, "lib")
        if os.path.isfile(os.path.join(incs, "expat.h")) \
           and (os.path.isfile(os.path.join(libs, "libexpat.so"))
                or os.path.isfile(os.path.join(libs, "libexpat.a"))):
            return p


expat_prefix = get_expat_prefix()

sources = ['extensions/pyexpat.c']
if expat_prefix:
    define_macros = [('HAVE_EXPAT_H', None)]
    include_dirs = [os.path.join(expat_prefix, "include")]
    libraries = ['expat']
    library_dirs = [os.path.join(expat_prefix, "lib")]
else:
    # To build expat 1.95.2, we need to find out the byteorder
    # Python 1.x doesn't provide sys.byteorder
    try:
        byteorder = sys.byteorder
    except AttributeError:
        try:
            import struct
        except ImportError:
            print "Need struct module to determine byteorder"
            raise SystemExit
        if struct.pack("i",1) == '\x01\x00\x00\x00':
            byteorder = "little"
        else:
            byteorder = "big"
    if byteorder == "little":
        xmlbo = "12"
    else:
        xmlbo = "21"
    define_macros = [
        ('HAVE_EXPAT_H',None),
        ('VERSION', '"1.95.2"'),
        ('XML_NS', '1'),
        ('XML_DTD', '1'),
        ('XML_BYTE_ORDER', xmlbo),
        ('XML_CONTEXT_BYTES','1024'),
        ]
    include_dirs = ['extensions/expat/lib']
    sources.extend([
        'extensions/expat/lib/xmlparse.c',
        'extensions/expat/lib/xmlrole.c',
        'extensions/expat/lib/xmltok.c',
        ])
    libraries = []
    library_dirs = []
    
ext_modules.append(
    Extension(xml('.parsers.pyexpat'),
              define_macros=define_macros,
              include_dirs=include_dirs,
              library_dirs=library_dirs,
              libraries=libraries,
              extra_link_args=LDFLAGS,
              sources=sources
              ))

# Build sgmlop
ext_modules.append(
    Extension(xml('.parsers.sgmlop'),
              extra_link_args=LDFLAGS,
              sources=['extensions/sgmlop.c'],
              ))

# Build boolean
ext_modules.append(
    Extension(xml('.utils.boolean'),
              extra_link_args=LDFLAGS,
              sources=['extensions/boolean.c'],
              ))


# On Windows, install the documentation into a directory xmldoc, along
# with xml/_xmlplus. For RPMs, docs are installed into the RPM doc
# directory via setup.cfg (usuall /usr/doc). On all other systems, the
# documentation is not installed.

doc2xmldoc = 0
if sys.platform == 'win32':
    doc2xmldoc = 1

# This is a fragment from MANIFEST.in which should contain all
# files which are considered documentation (doc, demo, test, plus some
# toplevel files)

# distutils 1.0 has a bug where
# recursive-include test/output test_*
# is translated into a pattern ^test\\output\.*test\_[^/]*$
# on windows, which results in files not being included. Work around
# this bug by using graft where possible.
docfiles="""
recursive-include doc *.html *.tex *.txt *.gif *.css *.api *.web

recursive-include demo README *.py *.xml *.dtd *.html *.htm
include demo/genxml/data.txt
include demo/dom/html2html
include demo/xbel/doc/xbel.bib
include demo/xbel/doc/xbel.tex
include demo/xmlproc/catalog.soc

recursive-include test *.py *.xml *.html *.dtd
include test/test.xml.out
graft test/output

include ANNOUNCE CREDITS LICENCE README* TODO

global-exclude */CVS/*
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
       version = "0.8", # Needs to match xml/__init__.version_info
       description = "Python/XML package",
       author = "XML-SIG",
       author_email = "xml-sig@python.org",
       url = "http://www.python.org/sigs/xml-sig/",
       long_description =
"""XML Parsers and API for Python
This version of PyXML was tested with Python 2.x
""",

       # Override certain command classes with our own ones
       cmdclass = {'install_data':install_Data_Files,
                   'bdist_wininst':wininst_request_delete
                   },

       package_dir = {xml(''):'xml'},

       data_files = [Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/de/LC_MESSAGES'),
                                files=['xml/dom/de/LC_MESSAGES/4Suite.mo']),
                     Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/en_US/LC_MESSAGES'),
                                files=['xml/dom/en_US/LC_MESSAGES/4Suite.mo']),
                     Data_Files(base_dir='install_lib',
                                copy_to=xml('/dom/fr_FR/LC_MESSAGES'),
                                files=['xml/dom/fr_FR/LC_MESSAGES/4Suite.mo']),
                     ] + xmldocfiles,
       
       packages = [xml(''), 
                   xml('.dom'), xml('.dom.html'), xml('.dom.ext'),
                   xml('.dom.ext.reader'),
                   xml('.marshal'), xml('.unicode'),
                   xml('.parsers'), xml('.parsers.xmlproc'),
                   xml('.sax'), xml('.sax.drivers'),
                   xml('.sax.drivers2'), xml('.utils'), xml('.schema'),
                   #xml('.xpath'), xml('.xslt')
                   ] + extra_packages,

       ext_modules = ext_modules,

       scripts = ['scripts/xmlproc_parse', 'scripts/xmlproc_val']
       )
