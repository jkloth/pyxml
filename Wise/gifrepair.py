# repair .gif files for Windows CVS
# The repository should be configured to handle this
# Properly, using cvswrappers settings.

# CT 990918

import os, sys, string

# this script assumes to be sitting inside the XML tree
# and repairs all .gif files.

args = sys.argv[1:]
path = ""
types = []
if args:
    path = args[0]
    types = args[1:]

if not path: path = ".."
if not types: types = [".gif"]

types = map(string.lower, types)

def repairer(types, d, files):
    for namex in files:
        namex = string.lower(namex)
        name, ext = os.path.splitext(namex)
        if string.lower(ext) in types:
            fname = os.path.join(d, namex)
            print "repairing", fname,
            bad = open(fname, "rb").read()
            good = string.replace(bad, "\r\n", "\n")
            open(fname, "wb").write(good)
            print " - done."

os.path.walk(path, repairer, types)
