#!/usr/bin/env python
#
# lynx_parse.py :
# Read a list of Lynx bookmark files, specified on the command line,
# and outputs the corresponding XBEL document.
#
# Sample usage: ./lynx_parse.py 
#

import bookmark
import re

def parse_lynx_file(bms, input):
    """Convert a Lynx 2.8 bookmark file to XBEL, reading from the
    input file object, and write to the output file object.""" 

    # Read the whole file into memory
    data = input.read()

    # Get the title
    m = re.search("<title>(.*?)</title>", data, re.IGNORECASE)
    if m is None: title = "Untitled"
    else: title = m.group(1)

    bms.add_folder( title, None, None)
    
    hrefpat = re.compile( r"""^ \s* <li> \s*
<a \s+ href \s* = \s* "(?P<url> [^"]* )" \s*>
(?P<name> .*? ) </a>""",
    re.IGNORECASE| re.DOTALL | re.VERBOSE | re.MULTILINE)
    pos = 0
    while 1:
        m = hrefpat.search(data, pos)
        if m is None: break
        pos = m.end()
        url, name = m.group(1,2)
        bms.add_bookmark( name, None, None, url)

    bms.leave_folder()

if __name__ == '__main__':
    import sys
    bms = bookmark.Bookmarks()

    # Determine the owner on Unix platforms
    import os, pwd
    uid = os.getuid()
    t = pwd.getpwuid( uid )
    bms.owner = t[4]

    for file in sys.argv[1:]:
        input = open(file)
        parse_lynx_file(bms, input)

    bms.dump_xbel()
