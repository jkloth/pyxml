
# Setup script for the XML tools
#
# Targets: build test install help

import sys, os

try:
    from distutils.core import setup, Extension
except ImportError:
    pass
else:

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

    # Check if we need to compile the wide string modules, or if this version
    # of Python has Unicode support.
    import __builtin__
    if hasattr(__builtin__, 'unicode'):
        wstr_modules = []
    else:
        wstr_modules = [('sgmlop', { 'sources' : ['extensions/sgmlop.c'] }),
                        ('xml.unicode.wstrop', { 'sources' : ['extensions/wstrop.c']
                                                 })
                        ]
                         
    setup (name = "PyXML",
           version = "0.5.6",
           description = "Python/XML package",
           author = "XML-SIG",
           author_email = "xml-sig@python.org",
           url = "http://www.python.org/sigs/xml-sig/",

           packages = ['xml', 
	               'xml.dom', 'xml.dom.html', 'xml.dom.ext',
		       'xml.dom.ext.reader',
		       'xml.marshal',
                       'xml.parsers', 'xml.parsers.xmlproc', 
                       'xml.sax', 'xml.sax.drivers',
                       'xml.unicode', 'xml.utils'
                       ],

           ext_modules = #wstr_modules +
	                 [Extension('xml.parsers.pyexpat',
			 define_macros = [('XML_NS', None)],
			 include_dirs = [ 'extensions/expat/xmltok',
			                  'extensions/expat/xmlparse' ], 
                         sources = [
                                      'extensions/pyexpat.c',
                                      'extensions/expat/xmltok/xmltok.c',
                                      'extensions/expat/xmltok/xmlrole.c',
                                      'extensions/expat/xmlwf/xmlfile.c',
                                      'extensions/expat/xmlwf/xmlwf.c',
                                      'extensions/expat/xmlwf/codepage.c',
                                      'extensions/expat/xmlparse/xmlparse.c',
                                      'extensions/expat/xmlparse/hashtable.c',
                                      FILEMAP_SRC,
                                      ] )
                          ]
           )
    
    sys.exit(0)
    
import shutil, compileall

if (len(sys.argv) == 1 or sys.argv[1] == 'help' or
    sys.argv[1] not in ['build', 'test', 'install']):
    print "Usage: python setup.py [command]"
    print "command can be one of 'build', 'test', 'install', 'help'"
    sys.exit(0)

action = sys.argv[1]
if action == 'build': actions = ['build']
elif action == 'test': actions = ['build', 'test']
elif action == 'install': actions = ['build', 'install']

# copytree() function copied from shutil, and modified to allow
# copying to an already existing directory.

EXCLUDE_FILES = ['CVS']

def copytree(src, dst, symlinks=0):
    """Recursively copy a directory tree using copy2().

    Errors are reported to standard output.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.
    """
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        if name in EXCLUDE_FILES: continue
        
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            print "Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why))

def create_build_dir():
    # Create build subdirectory
    if not os.path.exists('build'):
        os.mkdir('build')

    # Ensure build/xml/ directory doesn't exist
    if os.path.exists('build/xml'):
        shutil.rmtree('build/xml')
    copytree('xml', 'build/xml')

def build_win32():
    create_build_dir()
    
def build_mac():
    create_build_dir()
    
def build_unix():
    os.chdir('extensions')
    if not os.path.exists('Makefile'):
        cmd = 'make -f Makefile.pre.in boot'
        print '\nRunning command:', cmd
        os.system(cmd)
        
    cmd = 'make'
    print '\nRunning command:', cmd
    os.system(cmd)

    os.chdir('..')
    create_build_dir()

    # Copy the C extensions into the build directory
    for filename in ['pyexpat.so', 'sgmlop.so']:
        shutil.copy('extensions/' + filename, 'build/xml/parsers/')

    shutil.copy('extensions/wstrop.so', 'build/xml/unicode/')

def test_unix():
    old_path = sys.path
    sys.path = ['../build/'] + sys.path
    os.chdir('test')
    import testxml
    testxml.main()
    os.chdir('..')
    sys.path = old_path
test_win32 = test_mac = test_unix

# XXX is this correct?
dest_dir = (sys.prefix + '/lib/python' + sys.version[:3] +
            '/site-packages/xml/' )

def install_unix():
    copytree('build/xml', dest_dir)
    compileall.compile_dir( dest_dir)
    
install_win32 = install_mac = install_unix

platform = sys.platform
if platform not in ['win32', 'mac']: platform = 'unix'

for action in actions:
    print "\nExecuting '%s' action..." % (action)
    func = eval(action + '_' + platform)
    func()
    

