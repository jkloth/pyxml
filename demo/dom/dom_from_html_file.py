"""Reads in an HTML file from the command line and pretty-prints it."""

from xml.dom.ext.reader import HtmlLib
from xml.dom import ext

def read_html_from_file(fileName):
    #build a DOM tree from the file
    dom_object = HtmlLib.FromHtmlFile(fileName)

    #strip any ignorable white-space in preparation for pretty-printing
    ext.StripHtml(dom_object)

    #pretty-print the node
    ext.PrettyPrint(dom_object)

    #reclaim the object
    ext.ReleaseNode(dom_object);
   

if __name__ == '__main__':
    import sys
    read_html_from_file(sys.argv[1])
