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
        print name, attrs
        if name == 'FOLDER':
            self.entered_folder = 1
        elif name == 'NAME':
            self.name = ""
        elif name == 'OWNER':
            self.owner = ""
        elif name == 'BOOKMARK':
            self.name = self.url = ""
            self.added = self.visited = self.modified = ""

    def characters(self, ch, start, length):
        if self.cur_elem in ['NAME', 'URL', 'ADDED',
                               'VISITED', 'MODIFIED', 'OWNER']:
            attr = string.lower(self.cur_elem)
            value = getattr(self, attr)
            setattr(self, attr, value + ch[start:start+length])
            print getattr(self, attr)
        
    def endElement(self, name):
        print 'ending:', name
        self.cur_elem = None
        if name == 'FOLDER':
            print 'leaving folder'
            self.bms.leave_folder()
            self.entered_folder = 0
        elif name == 'OWNER':
            self.bms.owner = self.owner
        elif name == 'NAME' and self.entered_folder:
            print 'Adding folder', self.name
            self.bms.add_folder(self.name, None, None)
            self.entered_folder = 0
        elif name == 'BOOKMARK':
            print 'adding bookmark:', self.name, self.url
            self.entered_folder = 0
            if self.added == "": self.added = None
            if self.visited == "": self.visited = None
            if self.modified == "": self.modified = None
#            raise ImportError
            self.bms.add_bookmark(self.name, self.added, self.visited, self.url)
            
if __name__ == '__main__':
    import sys, getopt

    opts, args = getopt.getopt(sys.argv[1:], '',
                               ['opera', 'netscape', 'lynx', 'msie', 'xbel'] )
    if len(args):
        print 'xbel_parse only reads from standard input'
        sys.exit(1)
    if len(opts)>1 or len(opts)==0:
        print 'You must specify a single output format when running xbel_parse'
        print 'Available formats: --opera, --netscape, --msie, --lynx, --xbel'
        sys.exit(1)
        
    xbel_handler = XBELHandler()
    p=saxexts.XMLParserFactory.make_parser("xml.sax.drivers.drv_xmlproc")
    p.setDocumentHandler( xbel_handler )
    p.parseFile( sys.stdin )
    bms = xbel_handler.bms
    print bms.__dict__
    mode = opts[0][0]
    if mode == '--opera': bms.dump_adr()
    elif mode == '--lynx': bms.dump_lynx()
    elif mode == '--netscape': bms.dump_netscape()
    elif mode == '--msie': bms.dump_msie()
    elif mode == '--xbel': bms.dump_xbel()
    
    
