#! /usr/bin/env python
"""
A simple XBEL to HTML converter written with SAX.
"""

# Limitations: will screw up if a folder lacks a 'title' element.
#              no checking of the command-line args

import sys

from xml.sax import saxlib,saxutils,saxexts

# --- HTML templates

top=\
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>%s</TITLE>
  <META NAME="Generator" CONTENT="sax_xbel">
</HEAD>

<BODY>
<H1>%s</H1>
"""

bottom=\
"""
<HR>
<ADDRESS>
Converted from XBEL by sax_xbel, using %s.
</ADDRESS>
</BODY>
</HTML>
"""

# --- DocumentHandler

class XBELHandler(saxlib.HandlerBase):

    def __init__(self,parser,writer=sys.stdout):
        self.stack=[]
        self.writer=writer
        self.last_url=None
        self.parser=parser
        self.inside_ul=0
        self.level=0

    def startElement(self,name,attrs):
        self.stack.append(name)

        if name=="bookmark":
            self.last_url=attrs["href"]

    def characters(self,data,start,length):
        if self.stack==[]: return

        if self.stack[-1]=="title" and self.stack[-2]=="xbel":
            data=data[start:start+length]
            self.writer.write(top % (data,data))
            self.state=None

        if self.stack[-1]=="desc" and self.stack[-2]=="xbel":
            self.writer.write("<P>%s</P>\n" % data[start:start+length])

        if self.stack[-1]=="title" and self.stack[-2]=="bookmark":
            if not self.inside_ul:
                self.inside_ul=1
                self.writer.write("<UL>\n")
                
            self.writer.write('<LI><A HREF="%s">%s</A>. \n' %
                              (self.last_url,data[start:start+length]))

        if self.stack[-1]=="desc" and self.stack[-2]=="bookmark":
            self.writer.write(data[start:start+length]+"\n\n")

        if self.stack[-1]=="title" and self.stack[-2]=="folder":
            self.writer.write("<LI><B>%s</B>\n" % data[start:start+length])
            self.writer.write("<UL>\n")        
            self.inside_ul=1
            
    def endElement(self,name):
        del self.stack[-1]

        if name=="folder":
            self.writer.write("</UL>\n")

    def endDocument(self):
        self.writer.write("</UL>\n")
        self.writer.write(bottom % self.parser)
        
# --- Main program

if __name__ == '__main__':
    p=saxexts.make_parser()
    p.setDocumentHandler(XBELHandler(p.get_parser_name()))
    p.setErrorHandler(saxutils.ErrorPrinter())
    p.parse(sys.argv[1])


