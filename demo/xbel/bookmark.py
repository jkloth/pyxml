"""
Classes to store bookmarks and dump them to XBEL.
"""

import sys,string

# --- Class for bookmark container

class Bookmarks:

    def __init__(self):
        self.folders=[]
        self.folder_stack=[]

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
        out.write("<XBEL>\n")
        if hasattr(self, 'owner'):
            out.write('  <INFO>\n')
            out.write('    <OWNER>%s</OWNER>\n' % (self.owner,) )
            out.write('  </INFO>\n')

        for folder in self.folders:
            folder.dump_xbel(out)
        out.write("<XBEL>")

    def dump_adr(self,out=sys.stdout):
        out.write("Opera Hotlist version 2.0\n\n")
        for folder in self.folders:
            folder.dump_adr(out)

    def dump_netscape(self,out=sys.stdout):
        out.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        out.write("<!-- This is an automatically generated file.\n")
        out.write("It will be read and overwritten.\n")
        out.write("Do Not Edit! -->\n")
        if hasattr(self, 'owner'): owner=self.owner
        else: owner="Anonymous Bookmark File"
        out.write("<TITLE>" + owner + "</TITLE>\n")
        out.write("<H1>" + owner + "</H1>\n\n")

        out.write("<DL><p>\n")
        for folder in self.folders:
            folder.dump_netscape(out)
        out.write("</DL><p>\n")

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
        out.write("  <NODE>\n")
        out.write("    <NAME>%s</NAME>\n" % self.name)
        for child in self.children:
            child.dump_xbel(out)
        out.write("  </NODE>\n")

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
        out.write("  <BOOKMARK>\n")
        out.write("    <NAME>%s</NAME>\n" % self.name)
        out.write("    <URL>%s</URL>\n" % self.url)

        if self.created!=None:
            out.write("    <ADDED>%s</ADDED>\n" % self.created)

        if self.visited!=None:
            out.write("    <VISITED>%s</VISITED>\n" % self.visited)
            
        out.write("  </BOOKMARK>\n")

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
