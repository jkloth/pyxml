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

# Rename xml to _xmlplus for Python 2.0

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
for arg in args:
    if string.find(arg, '--with-libexpat=') == 0:
        LIBEXPAT = string.split(arg, '=')[1]
        sys.argv.remove(arg)
    elif string.find(arg, '--ldflags=') == 0:
        LDFLAGS = string.split(string.split(arg, '=')[1])
        sys.argv.remove(arg)

def should_build_pyexpat():
    try:
        import pyexpat
        # The following features of are required by PyXML from pyexpat,
        # which are not available in older versions:
        # ExternalEntityParserCreate, available only from 2.25 on.
        # ParseFile throws exception, not available up to 2.28.
        # Memory leak fixes, merged into 2.33
        # Wrong array boundaries fixed in 2.35
        if pyexpat.__version__ <= '2.39':
            if 'pyexpat' in sys.builtin_module_names:
                print "Error: builtin expat library will conflict with ours"
                print "Re-build python without builtin expat module"
                raise SystemExit
            return 1
    except ImportError:
        return 1
    else:
        return 0

def get_expat_prefix():
    if LIBEXPAT:
        return LIBEXPAT

    for p in ("/usr", "/usr/local"):
        incs = os.path.join(p, "include")
        libs = os.path.join(p, "lib")
        if os.path.isfile(os.path.join(incs, "expat.h")) \
           and (os.path.isfile(os.path.join(libs, "libexpat.so"))
                or os.path.isfile(os.path.join(libs, "libexpat.a"))):
            return p


# Don't build pyexpat if the Python installation provides one.
# FIXME: It should be built for binary distributions even if the core has it.
build_pyexpat = should_build_pyexpat()
if build_pyexpat:
    expat_prefix = get_expat_prefix()

    if build_pyexpat:
        sources = ['extensions/pyexpat.c']
        if expat_prefix:
            define_macros = [('HAVE_EXPAT_H', None)]
            include_dirs = [os.path.join(expat_prefix, "include")]
            libraries = ['expat']
            library_dirs = [os.path.join(expat_prefix, "lib")]
        else:
            define_macros = [('XML_NS', None),
                             ('XML_DTD', None),
                             ('EXPAT_VERSION','0x010200')]
            include_dirs = ['extensions/expat/xmltok',
                            'extensions/expat/xmlparse']
            sources.extend(['extensions/expat/xmltok/xmltok.c',
                            'extensions/expat/xmltok/xmlrole.c',
                            'extensions/expat/xmlparse/xmlparse.c'])
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
    Extension(xml('.parsers.sgmlop'), sources=['extensions/sgmlop.c']))

# Build boolean
ext_modules.append(
    Extension(xml('.utils.boolean'), sources=['extensions/boolean.c']))


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
       version = "0.7", # Needs to match xml/__init__.version_info
       description = "Python/XML package",
       author = "XML-SIG",
       author_email = "xml-sig@python.org",
       url = "http://www.python.org/sigs/xml-sig/",
       long_description =
"""XML Parsers and API for Python
This version of PyXML was tested with Python 2.0 and 1.5.2.
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
                   xml('.xpath'), xml('.xslt')
                   ],

       ext_modules = ext_modules,

       scripts = ['scripts/xmlproc_parse', 'scripts/xmlproc_val']
       )
