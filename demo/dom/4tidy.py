import sys, cStringIO
from xml.dom.ext.reader import HtmlLib
from xml.dom.ext import XHtmlPrint

def Tidy(doc):
    #stream = cStringIO.StringIO()
    #XHtmlPrint(doc, stream=stream)
    #text = stream.getvalue()

    XHtmlPrint(doc)
    return


if __name__ == "__main__":
    html_reader = HtmlLib.Reader()
    if len(sys.argv) != 2:
        print "%s requires a single argument: a URL or file name to be tidied"%sys.argv[0]
        sys.exit(-1)
    html_doc = html_reader.fromUri(sys.argv[1])
    Tidy(html_doc)
    
