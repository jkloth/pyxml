"""
Classes to store bookmarks and dump them to XBEL.
"""

import sys,string

# --- Class for bookmark container

class Bookmarks:

    def __init__(self):
        self.folders=[]
        self.folder_stack=[]
        self.owner = "Anonymous Bookmark File"
        
    def add_folder(self,name,created,visited):
        nf=Folder(name,created,visited)
        if self.folder_stack==[]:
            self.folders.append(nf)
        else:
            self.folder_stack[-1].add_child(nf)
            
        self.folder_stack.append(nf)

    def add_bookmark(self,name,created,visited,url):
        nb=Bookmark(name,created,visited,url)

        if self.folder_stack!=[]:
            self.folder_stack[-1].add_child(nb)
        else:
            self.folders.append(nb)
        
    def leave_folder(self):
        if self.folder_stack!=[]:
            del self.folder_stack[-1]

    def dump_xbel(self,out=sys.stdout):
        out.write('<?xml version="1.0"?>\n'
                  '<!DOCTYPE xbel SYSTEM "xbel.dtd">\n'
                  '<xbel>\n')
        out.write("  <desc>%s's Bookmarks</desc>\n" % (self.owner,) )

        for folder in self.folders:
            folder.dump_xbel(out)
        out.write("</xbel>\n")

    def dump_adr(self,out=sys.stdout):
        out.write("Opera Hotlist version 2.0\n\n")
        for folder in self.folders:
            folder.dump_adr(out)

    def dump_netscape(self,out=sys.stdout):
        out.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        out.write("<!-- This is an automatically generated file.\n")
        out.write("It will be read and overwritten.\n")
        out.write("Do Not Edit! -->\n")
        out.write("<TITLE>" + self.owner + "</TITLE>\n")
        out.write("<H1>" + self.owner + "</H1>\n\n")

        out.write("<DL><p>\n")
        for folder in self.folders:
            folder.dump_netscape(out)
        out.write("</DL><p>\n")

    # Lynx uses multiple bookmark files; each folder will be written to a
    # different file.
    def dump_lynx(self, path):
        for folder in self.folders:
            # First, figure out a reasonable filename for this folder
            file = string.replace(folder.name, ' ', '_') + '.html'
            output = open( os.path.join(path, filename), 'w')
            output.write('<head>\n<title>Bookmark file: %s</title>\n<head>\n'
                         % (folder.name,) )
            output.write('<p>\n<ol>\n')
            folder.dump_lynx(path, output)
            
# --- Superclass for folder and bookmarks
        
class Node:

    def __init__(self,name,created,visited):
        self.name=name
        self.created=created
        self.visited=visited

# --- Class for folders
    
class Folder(Node):

    def __init__(self,name,created,visited):
        Node.__init__(self,name,created,visited)
        self.children=[]

    def add_child(self,child):
        self.children.append(child)

    def dump_xbel(self,out):
        out.write("  <folder>\n")
        out.write("    <title>%s</title>\n" % self.name)
        for child in self.children:
            child.dump_xbel(out)
        out.write("  </folder>\n")

    def dump_adr(self,out):
        out.write("#FOLDER\n")
        out.write("\tNAME=%s\n" % self.name)
        out.write("\tCREATED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

        for child in self.children:
            child.dump_adr(out)

        out.write("\n")
        out.write("-\n")

    def dump_netscape(self,out):
        out.write("  <DT><H3 FOLDED>%s</H3>\n" % self.name)
        out.write("  <DL><p>\n")

        for child in self.children:
            child.dump_netscape(out)

        out.write("  </DL><p>\n")

# --- Class for bookmarks
        
class Bookmark(Node):

    def __init__(self,name,created,visited,url):
        Node.__init__(self,name,created,visited)
        self.url=url

    def dump_xbel(self,out):
        if self.visited!=None:
            visited = 'visited="%s" ' % self.visited
        else:
            visited = ""

        if self.created!=None:
            created = 'added="%s" ' % self.created
        else:
            created = ""
            
        out.write('    <bookmark href="%s" %s%s>\n' % (self.url, created, visited) )
        out.write("      <title>%s</title>\n" % self.name)
        out.write("    </bookmark>\n")

    def dump_adr(self,out):
        out.write("#URL\n")
        out.write("\tNAME=%s\n" % self.name)
        out.write("\tURL=%s\n" % self.url)
        out.write("\tCREATED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

    def dump_netscape(self,out):
        out.write("    <DT><A HREF=\"%s\">%s</A>\n" % (self.url,self.name))

