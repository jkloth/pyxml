"""
Small utility that parses Netscape bookmarks.
"""

from xml.sax import saxexts,saxlib
import bookmark

# --- SAX handler for Netscape bookmarks

class NetscapeHandler(saxlib.HandlerBase):

    def __init__(self):
        self.bms=bookmark.Bookmarks()
        self.cur_elem=None
        self.added=None
        self.url=None
        self.visited=None
        self.last_modified=None

    def startElement(self,name,attrs):
        if name=="h3":
            self.cur_elem="h3"
            self.added=attrs["add_date"]
        elif name=="a":
            self.cur_elem="a"
            self.added=attrs["add_date"]
            self.url=attrs["href"]
            self.visited=attrs["last_visit"]
            self.last_modified=attrs["last_modified"]            
        elif name=='title':  # Could equally use h1 element
            self.cur_elem = 'title'
            self.bms.owner = ""
            
    def characters(self,data,start,length):
        if self.cur_elem=="h3":
            self.bms.add_folder(data[start:start+length],None,None)
        elif self.cur_elem=="a":
            self.bms.add_bookmark(data[start:start+length],None,None,self.url)
        elif self.cur_elem=="title":
            self.bms.owner = self.bms.owner + data[start:start+length]
            
    def endElement(self,name):
        if name=="h3":
            self.cur_elem=None
        elif name=="dl":
            self.bms.leave_folder()
        elif name=="a" or name == 'title':
            self.cur_elem=None

# --- Main program

if __name__ == '__main__':
    ns_handler=NetscapeHandler()

    p=saxexts.SGMLParserFactory.make_parser()
    p.setDocumentHandler(ns_handler)
    p.parseFile(open(r"/home/amk/.netscape/bookmarks.html"))
    ns_handler.bms.dump_xbel()

