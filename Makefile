# Convenience make rules to help run the build/tests for several
# Python versions.  Edit to suit your choice of Python versions.

PLAT=$(shell python -c 'from distutils import util; print util.get_platform()')

# For now, always build pyexpat, since PyXML contains a more advanced
# version of the extension.
#
BUILDARGS=--with-pyexpat

.PHONY:	build

all:	build
test:	check

build:
	python2.0 setup.py $(BUILDARGS) -q build
	python2.1 setup.py $(BUILDARGS) -q build
	python2.2 setup.py $(BUILDARGS) -q build
	python2.3 setup.py $(BUILDARGS) -q build

check:	build
	cd test && PYTHONPATH=../build/lib.$(PLAT)-2.0 python2.0 testxml.py
	cd test && PYTHONPATH=../build/lib.$(PLAT)-2.1 python2.1 testxml.py
	cd test && PYTHONPATH=../build/lib.$(PLAT)-2.2 python2.2 testxml.py
	cd test && PYTHONPATH=../build/lib.$(PLAT)-2.3 python2.3 testxml.py

clean:
	rm -rf build
