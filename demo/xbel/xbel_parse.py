#!/usr/bin/env python

"""

A class to parse an XBEL file and produce a Bookmarks instance.

If executed as a script, this module will read an XBEL file from
standard input, produce the corresponding Bookmarks instance, and dump
it to standard output in a selected format.

"""

import bookmark
import string
from xml.sax import saxexts,saxlib

class XBELHandler(saxlib.HandlerBase):
    def __init__(self):
        self.bms = bookmark.Bookmarks()
        self.entered_folder = self.entered_bookmark = 0

    def startElement(self, name, attrs):
        self.cur_elem = name
#        print name, attrs
        if name == 'folder':
            self.entered_folder = 1
        elif name == 'title':
            self.title = ""
        elif name == 'desc':
            self.desc = ""
        elif name == 'bookmark':
            self.title = self.href = ""
            self.added = self.visited = self.modified = ""

            if attrs.has_key('href'):
                self.href = attrs['href']
            if attrs.has_key('added'):
                self.added = attrs['added']
            if attrs.has_key('visited'):
                self.visited = attrs['visited']
            if attrs.has_key('modified'):
                self.modified = attrs['modified']

    def characters(self, ch, start, length):
        if self.cur_elem in ['title', 'desc']:
            attr = string.lower(self.cur_elem)
            value = getattr(self, attr)
            setattr(self, attr, value + ch[start:start+length])
#            print getattr(self, attr)

    def endElement(self, name):
#        print 'ending:', name
        self.cur_elem = None
        if name == 'folder':
#            print 'leaving folder'
            self.bms.leave_folder()
            self.entered_folder = 0
        elif name == 'desc':
            self.bms.desc = self.desc
        elif name == 'title' and self.entered_folder:
#            print 'Adding folder', self.title
            self.bms.add_folder(self.title)
            self.entered_folder = 0
        elif name == 'bookmark':
#            print 'adding bookmark:', self.title, self.href
            self.entered_folder = 0
            if self.added == "": self.added = None
            if self.visited == "": self.visited = None
            if self.modified == "": self.modified = None
#            raise ImportError
            self.bms.add_bookmark(self.title, self.added, self.visited, self.modified, self.href)

if __name__ == '__main__':
    import sys, getopt

    opts, args = getopt.getopt(sys.argv[1:], '',
                               ['opera', 'netscape', 'lynx=', 'msie', 'xbel'] )
    if len(args):
        print 'xbel_parse only reads from standard input'
        sys.exit(1)
    if len(opts)>1 or len(opts)==0:
        print 'You must specify a single output format when running xbel_parse'
        print 'Available formats: --opera, --netscape, --msie, --lynx, --xbel'
        print '    --lynx <path> : For Lynx, a path to the directory where'
        print '                    the output bookmark files should be written'
        sys.exit(1)

    xbel_handler = XBELHandler()
    p=saxexts.XMLParserFactory.make_parser()
    p.setDocumentHandler( xbel_handler )
    p.parseFile( sys.stdin )
    bms = xbel_handler.bms
    mode, arg = opts[0]
    if mode == '--opera': bms.dump_adr()
    elif mode == '--lynx': bms.dump_lynx(arg)
    elif mode == '--netscape': bms.dump_netscape()
    elif mode == '--msie': bms.dump_msie()
    elif mode == '--xbel': bms.dump_xbel()
