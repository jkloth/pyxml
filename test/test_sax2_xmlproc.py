import unittest
from cStringIO import StringIO
import xml.sax
from xml.sax import handler
from xml.sax import xmlreader # constants & helpers

_drv_xmlproc = "xml.sax.drivers2.drv_xmlproc"
_xmls_nons = "<test>data</test>"
_xmls_blankns = "<test xmlns=''>data</test>"

class _MyHandler(handler.ContentHandler):
    def __init__(self,testCase):
        self.__testCase = testCase
    def startElementNS(self,name,qname,atts):
        # XXX: is this right ? At least pyexpat and xmlproc do it this way.
        self.__testCase.failIf(name[0] != None)
        # XXX: or should it be this one ?
        #self.__testCase.failIf(name[0] != '')

def _makeParser(driver,ns):
    reader = xml.sax.make_parser([driver])
    reader.setFeature(handler.feature_namespaces,ns)
    return reader

def _saxParse(testCase,driver,ns,h,xmls):
    reader = _makeParser(driver,ns)
    reader.setContentHandler(h)
    inps = xmlreader.InputSource()
    inps.setByteStream(StringIO(xmls))
    reader.parse(inps)

# test cases

class MyTest(unittest.TestCase):
    def test_sax_xmlproc_nson__nons(self):
        _saxParse(self,_drv_xmlproc,1,_MyHandler(self),_xmls_nons)
    def test_sax_xmlproc_nson__blankns(self):
        _saxParse(self,_drv_xmlproc,1,_MyHandler(self),_xmls_blankns)

if __name__ == "__main__":
    unittest.main()
