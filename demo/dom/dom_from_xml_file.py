from xml.dom import ext
from xml.dom.ext.reader import Sax2

def read_xml_from_file(fileName):
    #build a DOM tree from the file
    try:
        xml_dom_object = Sax2.FromXmlFile(fileName, validate=0)
    except Sax.saxlib.SAXException, msg:
        print "SAXException caught:", msg
    except Sax.saxlib.SAXParseException, msg:
        print "SAXParseException caught:", msg

    ext.Print(xml_dom_object)

    #reclaim the object
    ext.ReleaseNode(xml_dom_object)

if __name__ == '__main__':
    import sys
    read_xml_from_file(sys.argv[1])
