
# Read a Lynx bookmark file, and output the corresponding XBEL document

import re

def lynx2xbel(input, output):
    """Convert a Lynx 2.8 bookmark file to XBEL, reading from the
    input file object, and write to the output file object.""" 

    # Determine the owner on Unix platforms
    import os, pwd
    uid = os.getuid()
    t = pwd.getpwuid( uid )
    owner = t[4]
    
    # Read the whole file into memory
    data = input.read()

    # Get the title
    m = re.search("<title>(.*?)</title>", data, re.IGNORECASE)
    if m is None: title = "Untitled"
    else: title = m.group(1)

    output.write("""<?xml version="1.0"?>
<!DOCTYPE XBEL SYSTEM "xbel.dtd">
<XBEL>
  <INFO>
    <OWNER>%s</OWNER>
  </INFO>
  
  <FOLDER>
    <NAME>%s</NAME>
""" % (owner, title) )

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
        output.write("""    <BOOKMARK>
      <NAME>%s</NAME>
      <URL>%s</URL>
    </BOOKMARK>\n""" % (name, url) )
    output.write("  </FOLDER>\n</XBEL>\n")
    
if __name__ == '__main__':
    import sys
    input = open('/home/amk/lynx_bookmarks.html')
    lynx2xbel(input, sys.stdout)
    



