"""Performance comparison for the xml.dom.expatbuilder DOM loader."""

import os
import sys
import time

from xml.dom import minidom, expatbuilder

FRAGMENT = '''\
<element attr1="foo" attr2="bar">
  <subelement/>
</element>
'''

CHUNKS = 12000
LOGFILE = "hotshot.log"

first = 1
chunks = CHUNKS

if sys.argv[1:]:
    try:
        chunks = int(sys.argv[-1])
    except ValueError:
        pass
    else:
        del sys.argv[-1]


def timeit(parsefunc, *args, **kw):
    global first
    src = "<doc>%s</doc>" % (FRAGMENT * chunks)
    if first:
        print "Document source contains", len(src), "bytes."
        first = 0
    modname = parsefunc.func_globals["__name__"]
    t1 = time.time()
    doc = parsefunc(src, *args, **kw)
    t2 = time.time()
    doc.unlink()
    print ("using %s.parseString():" % modname), t2 - t1
    return t2 - t1


timeit(minidom.parseString)
timeit(expatbuilder.parseString)

if sys.argv[1:] == ["-p"]:
    if os.path.exists(LOGFILE):
        os.unlink(LOGFILE)
    import hotshot
    import hotshot.stats

    def profile(*args, **kw):
        profiler = hotshot.Profile(LOGFILE)
        src = "<doc>%s</doc>" % (FRAGMENT * chunks)
        profiler.runcall(expatbuilder.parseString, src, *args, **kw)
        profiler.close()
        stats = hotshot.stats.load(LOGFILE)
        stats.strip_dirs()
        stats.sort_stats('calls')
        stats.print_stats(20)

    profile()
