#!/usr/bin/env python

"""
Small utility that parses Netscape bookmarks.
"""

from xml.sax import saxexts,saxlib
import bookmark
import string

# --- SAX handler for Netscape bookmarks

class NetscapeHandler(saxlib.HandlerBase):

    def __init__(self):
        self.bms=bookmark.Bookmarks()
        self.cur_elem = None
        self.added    = None
        self.href     = None
        self.visited  = None
        self.modified = None

    def startElement(self,name,attrs):
        name = string.lower( name )
        d = {}
        for key, value in attrs.items():
            d[ string.lower(key) ] = value
##        print 'start', name, d
        if name=="h3":
            self.cur_elem="h3"
            if d.has_key('add_date'): self.added=d["add_date"]
            else: self.added = ""

        elif name=="a":
            self.cur_elem="a"
            if d.has_key('add_date'): self.added=d["add_date"]
            else: self.added = None
            if d.has_key('last_visit'): self.visited=d["last_visit"]
            else: self.visited = None
            if d.has_key('last_modified'): self.modified=d["last_modified"]
            else: self.modified = None

            self.url=d["href"]
        elif name=='title':  # Could equally use h1 element
            self.cur_elem = 'title'
            self.bms.owner = ""

    def characters(self,data,start,length):
##        print 'char', self.cur_elem, data[start:start+length]
        if self.cur_elem=="h3":
            self.bms.add_folder(data[start:start+length],None)
        elif self.cur_elem=="a":
            self.bms.add_bookmark( data[start:start+length],
                                   added = self.added,
                                   visited = self.visited,
                                   modified = self.modified,
                                   href = self.url)
        elif self.cur_elem=="title":
            self.bms.owner = self.bms.owner + data[start:start+length]

    def endElement(self,name):
        name = string.lower( name )
##        print 'end', name
        if name=="h3":
            self.cur_elem=None
        elif name=="dl":
            self.bms.leave_folder()
        elif name=="a" or name == 'title':
            self.cur_elem=None

# --- Test-program

if __name__ == '__main__':
    import sys

    if len(sys.argv)<2 or len(sys.argv)>3:
        print
        print "A simple utility to convert Netscape bookmarks to XBEL."
        print
        print "Usage: "
        print "  ns_parse.py <ns-file> [<xbel-file>]"
        sys.exit(1)

    ns_handler=NetscapeHandler()
    p=saxexts.SGMLParserFactory.make_parser()
    p.setDocumentHandler(ns_handler)
    file = open(sys.argv[1], 'r')
    p.parseFile( file )
    bms = ns_handler.bms

    if len(sys.argv)==3:
        out=open(sys.argv[2],"w")
        bms.dump_xbel(out)
        out.close()
    else:
        bms.dump_xbel()

    # Done

##     ns_handler=NetscapeHandler()

##     p=saxexts.SGMLParserFactory.make_parser()
##     p.setDocumentHandler(ns_handler)
##     p.parseFile(open(r"/home/amk/.netscape/bookmarks.html"))
##     ns_handler.bms.dump_xbel()
