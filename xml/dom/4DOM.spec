Summary: Python XML/HTML Library implementing the W3C's Document Object Model
Name: 4DOM
Version: 0.10.1
Release: 1
Requires: python python-xml-nodom
Copyright: freeware
Group: Development/Languages/Python
BuildArchitectures: noarch
Packager: Fourthought, Inc. <support@4suite.com>
Source: ftp://FourThought.com/4Suite/4DOM-0.10.1.tar.gz
Url: http://FourThought.com/4Suite/4DOM

%description
4DOM is a Python library for XML and HTML processing and manipulation
using the W3C's Document Object Model for interface.  4DOM supports
DOM all of Level 1 (core and HTML), as well as core, HTML and Document
Traversal from Level 2.  4DOM also adds some helper components for DOM
Tree creation and printing, python integration, white-space manipulation,
etc.

%prep
%setup -n xml/dom

%install
install -d -m 755 -o 0 -g 0 /usr/lib/python1.5/site-packages/xml/dom/ext/reader
install -d -m 755 -o 0 -g 0 /usr/lib/python1.5/site-packages/xml/dom/html

python -O -c "import compileall; compileall.compile_dir('.')"

install -m 644 -o 0 -g 0 *.py* /usr/lib/python1.5/site-packages/xml/dom
install -m 644 -o 0 -g 0 ext/*.py* /usr/lib/python1.5/site-packages/xml/dom/ext
install -m 644 -o 0 -g 0 ext/reader/*.py* /usr/lib/python1.5/site-packages/xml/dom/ext/reader
install -m 644 -o 0 -g 0 html/*.py* /usr/lib/python1.5/site-packages/xml/dom/html

%clean
cd ../..
rm -rf xml/dom

%files
%defattr(-,root,root)
%doc COPYRIGHT ChangeLog README TODO docs/4DOM.html docs/extensions.html demo
/usr/lib/python1.5/site-packages/xml/dom

%changelog
* Tue Jun 06 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
  [4DOM-0.10.1]
 - Fix nasty character-encoding bugs in Printer
 - Fixed many bugs in demos
 - Fix Sax2 support for passed-in documents
 - Other bug-fixes
* Wed May 24 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
  [4DOM-0.10.0]
 - Moved all static variables to class variables
 - Fixed printing to work with empty elements
 - Removed all tabs from files
 - Change package to xml.dom
 - major change to the internals to use Node as a Python attribute manager
   this improves efficiency: cutting down on __g/setattrs__ and simplifies
   some things
* Thu Mar 17 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
 - Minor fixes for 0.9.3 release
* Sun Mar 12 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
  [4DOM-0.9.3beta2]
 - Better UTF-8 handling in printing
 - Clean up printer whitespace
 - Fix nasty bug in Sax2 attribute namespace defaulting
 - Other bug-fixes
* Tue Jan 25 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
  [4DOM-0.9.2]
 - Major fixes to namespace code
 - Other bug-fixes
* Mon Jan 03 2000 Uche Ogbuji <uche.ogbuji@fourthought.com>
  [4DOM-0.9.1]
 - Fixed HTML reader
 - Misc. Bug-Fixes
* Sun Dec 19 1999 Uche Ogbuji <uche.ogbuji@fourthought.com>
- upgrade to 4DOM 0.9.0
* Thu Oct 21 1999 Uche Ogbuji <uche.ogbuji@fourthought.com>
- upgrade to 4DOM 0.8.2
* Mon Oct 18 1999 Uche Ogbuji <uche.ogbuji@fourthought.com>
- initial RPM release
