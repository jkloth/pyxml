# cleanup certain files recursively
# CT 990722

import os, sys, string

args = sys.argv[1:]
path = ""
types = []

if args:
    path = args[0]
    types = args[1:]

if not path: path = "."
if not types: types = [".pyc", ".pyo"]

types = map(string.lower, types)

def eraser(types, d, files):
    for namex in files:
        namex = string.lower(namex)
        name, ext = os.path.splitext(namex)
        if string.lower(ext) in types:
            try:
                fname = os.path.join(d, namex)
                print "removing", fname,
                os.unlink(fname)
                print " - done."
            except os.error:
                print " - cannot remove!"

os.path.walk(path, eraser, types)
