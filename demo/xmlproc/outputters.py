
# This is just a common library of xmlproc applications that can output
# parsed XML in various formats, included so that you can actually see
# the parsed data outputted by xmlproc.

# This file is not useful in itself, it's imported by xvcmd.py and
# xpcmd.py

import sys

from xml.parsers.xmlproc import xmlapp

# ESIS document handler

class ESISDocHandler(xmlapp.Application):

    def __init__(self,writer=sys.stdout):
	self.writer=writer
    
    def handle_pi(self,target,data):
	self.writer.write("?"+target+" "+remainder+"\n")

    def handle_start_tag(self,name,amap):
	self.writer.write("("+name+"\n")
	for a_name in amap.keys():
	    self.writer.write("A"+a_name+" "+amap[a_name]+"\n")

    def handle_end_tag(self,name):
	self.writer.write(")"+name+"\n")

    def handle_data(self,data,start_ix,length):
	self.writer.write("-"+data[start_ix:start_ix+length]+"\n")
        
# XML canonizer

class Canonizer(xmlapp.Application):

    def __init__(self,writer=sys.stdout):
	self.elem_level=0
	self.writer=writer
    
    def handle_pi(self,target, remainder):
	if not target=="xml":
	    self.writer.write("<?"+target+" "+remainder+"?>")

    def handle_start_tag(self,name,amap):
	self.writer.write("<"+name)
	
	a_names=amap.keys()
	a_names.sort()

	for a_name in a_names:
	    self.writer.write(" "+a_name+"=\"")
	    self.write_data(amap[a_name])
	    self.writer.write("\"")
	self.writer.write(">")
	self.elem_level=self.elem_level+1

    def handle_end_tag(self,name):
	self.writer.write("</"+name+">")
	self.elem_level=self.elem_level-1

    def handle_ignorable_data(self,data,start_ix,length):
	self.characters(data,start_ix,length)
	
    def handle_data(self,data,start_ix,length):
	if self.elem_level>0:
            self.write_data(data[start_ix:start_ix+length])
	    
    def write_data(self,data):
	data=string.replace(data,"&","&amp;")
	data=string.replace(data,"<","&lt;")
	data=string.replace(data,"\"","&quot;")
	data=string.replace(data,">","&gt;")
        data=string.replace(data,chr(9),"&#9;")
        data=string.replace(data,chr(10),"&#10;")
        data=string.replace(data,chr(13),"&#13;")
	self.writer.write(data)
