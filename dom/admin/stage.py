#!/usr/bin/env python

import sys, os, string

rootDir = string.join(string.split(os.__dict__['__file__'],'/')[:-1],'/') + '/site-packages/xml/dom'

if len(sys.argv) > 1 and sys.argv[1] == 'quick':
     os.system('find . -name "*.py" -exec cp {} %s/{} \;' % rootDir)
     sys.exit(0)                                                                                 

os.system('rm -rf %s' % rootDir);

directories = ['.',
               'ext',
               'ext/test_suite',
               'ext/reader',
               'html',
               'html/test_suite',
               'test_suite',
               'demo',
               'admin',
               'docs'
               ]

fileTypes = ['*.py','*.idl','*.xml','*.dtd','*.html']

print "Copying DOM files..."
for dir in directories:
    os.system('install -d -m 775 %s/%s' % (rootDir, dir))
    for file in fileTypes:
        os.system('find ./%s -maxdepth 1 -name "%s" -exec cp {} %s/{} \;' % (dir, file, rootDir))

print "Generating HTML DOM files..."
os.system('cd %s/html && ./generateHtml.py html_classes.xml' % rootDir)
