"""
Classes to store bookmarks and dump them to XBEL.
"""

import sys,string
from xml.sax.saxutils import escape

# --- Class for bookmark container

class Bookmarks:

    def __init__(self):
        self.folders=[]
        self.folder_stack=[]
        self.desc = "No description"

    def add_folder(self, name, added=None):
        nf=Folder(name, added)
        if self.folder_stack==[]:
            self.folders.append(nf)
        else:
            self.folder_stack[-1].add_child(nf)

        self.folder_stack.append(nf)

    def add_bookmark(self,name=None,
                     added=None, visited=None, modified=None,
                     href=None):
        nb=Bookmark(name,added,visited,modified,href)

        if self.folder_stack!=[]:
            self.folder_stack[-1].add_child(nb)
        else:
            self.folders.append(nb)

    def leave_folder(self):
        if self.folder_stack!=[]:
            del self.folder_stack[-1]

    def dump_xbel(self,out=sys.stdout):
        out.write('<?xml version="1.0"?>\n'
                  '<!DOCTYPE xbel PUBLIC "+//IDN python.org//DTD XML Bookmark Exchange Language 1.0//EN//XML" "xbel.dtd">\n'
                  '<xbel>'
        )
        out.write("  <desc>%s</desc>\n" % (escape(self.desc),) )

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
        out.write("<TITLE>" + self.desc + "</TITLE>\n")
        out.write("<H1>" + self.desc + "</H1>\n\n")

        out.write("<DL><p>\n")
        for folder in self.folders:
            folder.dump_netscape(out)
        out.write("</DL><p>\n")

    # Lynx uses multiple bookmark files; each folder will be written to a
    # different file.
    def dump_lynx(self, path):
        import os
        for folder in self.folders:
            # First, figure out a reasonable filename for this folder
            filename = string.replace(folder.title, ' ', '_') + '.html'

            # Open a file for the top-level folders
            output = open( os.path.join(path, filename), 'w')
            print 'folder title:', folder.title, filename
            output.write('<head>\n<title>%s</title>\n<head>\n'
                         % (folder.title,) )
            output.write('<p>\n<ol>\n')

            folder.dump_lynx(output)

            output.close()

# --- Superclass for folder and bookmarks

class Node:
    def __init__(self,name,added=None, visited=None, modified=None):
        self.title=name
        self.added=added
        self.visited=visited
        self.modified=modified

# --- Class for folders

class Folder(Node):

    def __init__(self,name,added=None):
        Node.__init__(self, name, added=added)
        self.children=[]

    def add_child(self,child):
        self.children.append(child)

    def dump_xbel(self,out):
        out.write("  <folder>\n")
        out.write("    <title>%s</title>\n" % escape(self.title) )
        for child in self.children:
            child.dump_xbel(out)
        out.write("  </folder>\n")

    def dump_adr(self,out):
        out.write("#FOLDER\n")
        out.write("\tNAME=%s\n" % self.title)
        out.write("\tADDED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

        for child in self.children:
            child.dump_adr(out)

        out.write("\n")
        out.write("-\n")

    def dump_netscape(self,out):
        out.write("  <DT><H3 FOLDED>%s</H3>\n" % self.title)
        out.write("  <DL><p>\n")

        for child in self.children:
            child.dump_netscape(out)

        out.write("  </DL><p>\n")

    def dump_lynx(self, out):
        out.write("  <H3>%s</H3>\n" % self.title)
        out.write("  <OL>\n")

        for child in self.children:
            child.dump_lynx(out)

        # Mustn't write the closing </OL>, because Lynx will add it
        # when it reads the bookmark file.
        ##out.write("  </OL>\n")

# --- Class for bookmarks

class Bookmark(Node):

    def __init__(self,name, added=None, visited=None,
                 modified=None, href=None):
        Node.__init__(self,name,added,visited,modified)
        self.href=href

    def dump_xbel(self,out):
        if self.visited!=None:
            visited = 'visited="%s" ' % escape(self.visited)
        else:
            visited = ""

        if self.added!=None:
            added = 'added="%s" ' % escape(self.added)
        else:
            added = ""

        if self.modified!=None:
            modified = 'modified="%s" ' % escape(self.modified)
        else:
            modified = ""

        out.write('    <bookmark href="%s" %s%s%s>\n' %
                  ( escape(self.href), added, visited, modified) )
        out.write("      <title>%s</title>\n" % escape(self.title) )
        out.write("    </bookmark>\n")

    def dump_adr(self,out):
        out.write("#URL\n")
        out.write("\tNAME=%s\n" % self.title)
        out.write("\tURL=%s\n" % self.href)
        out.write("\tCREATED=%s\n" % "0 (?)")
        out.write("\tVISITED=%s\n" % "0 (?)")
        out.write("\tORDER=-1\n")
        out.write("\n")

    def dump_netscape(self,out):
        out.write("    <DT><A HREF=\"%s\">%s</A>\n" % (self.href,self.title))

    def dump_lynx(self, out):
        out.write("<LI><A HREF=\"%s\">%s</A>\n" % (self.href, self.title) )
