"""
SAX driver for the Pyexpat C module.  This driver works with
pyexpat.__version__ == '1.5'.

$Id: drv_pyexpat.py,v 1.4 2000/09/26 14:43:11 loewis Exp $
"""

# Todo on driver:
#  - make it support external entities (wait for pyexpat.c)
#  - enable configuration between reset() and feed() calls
#  - support lexical events?
#  - proper inputsource handling
#  - properties and features

# Todo on pyexpat.c:
#  - support XML_ExternalEntityParserCreate
#  - exceptions in callouts from pyexpat to python code lose position info

version = "0.20"

from xml.sax import saxlib, saxutils
from string import split
AttributesImpl = saxutils.AttributesImpl

try:
    import pyexpat
except ImportError:
    from xml.parsers import pyexpat

# --- ExpatDriver

class ExpatDriver(saxutils.BaseIncrementalParser, saxlib.Locator):
    "SAX driver for the Pyexpat C module."

    def __init__(self):
        saxutils.BaseIncrementalParser.__init__(self)
        self._source = None
        self._parser = None
        self._namespaces = 1
        self._parsing = 0

    # XMLReader methods

    def parse(self, source):
	"Parse an XML document from a system identifier or an InputSource."

        self.reset()
        self._cont_handler.setDocumentLocator(self)
        try:
            saxutils.BaseIncrementalParser.parse(self, source)
        except pyexpat.error:
            error_code = self._parser.ErrorCode
            raise saxlib.SAXParseException(pyexpat.ErrorString(error_code),
                                           None, self)
            
            self._cont_handler.endDocument()

    def prepareParser(self, source):
        self._source = source
        
        if self._source.getSystemId() != None:
            self._parser.SetBase(self._source.getSystemId())
        
    def getFeature(self, name):
        "Looks up and returns the state of a SAX2 feature."
        if name == feature_namespaces:
            return self._namespaces
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def setFeature(self, name, state):
        "Sets the state of a SAX2 feature."
        if self._parsing:
            raise SAXNotSupportedException("Cannot set features while parsing")
        if name == feature_namespaces:
            self._namespaces = state
        else:
            raise SAXNotRecognizedException("Feature '%s' not recognized" %
                                            name)

    def getProperty(self, name):
        "Looks up and returns the value of a SAX2 property."
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def setProperty(self, name, value):
        "Sets the value of a SAX2 property."
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    # IncrementalParser methods

    def feed(self, data):
        if not self._parsing:
            self._parsing=1
            self.reset()
            self._cont_handler.startDocument()
        self._parser.Parse(data, 0)

    def close(self):
        if self._parsing:
            self._cont_handler.endDocument()
            self._parsing=0
        self._parser.Parse("", 1)
        
    def reset(self):
        if self._namespaces:
            self._parser = pyexpat.ParserCreate(None, " ")
            self._parser.StartElementHandler = self.start_element_ns
            self._parser.EndElementHandler = self.end_element_ns
        else:
            self._parser = pyexpat.ParserCreate()
            self._parser.StartElementHandler = self.start_element
            self._parser.EndElementHandler = self.end_element

        self._parser.ProcessingInstructionHandler = self.processing_instruction
        self._parser.CharacterDataHandler = self.character_data
        self._parser.UnparsedEntityDeclHandler = self.unparsed_entity_decl
        self._parser.NotationDeclHandler = self.notation_decl
        self._parser.StartNamespaceDeclHandler = self.start_namespace_decl
        self._parser.EndNamespaceDeclHandler = self.end_namespace_decl
#         self._parser.CommentHandler = 
#         self._parser.StartCdataSectionHandler = 
#         self._parser.EndCdataSectionHandler = 
#         self._parser.DefaultHandler = 
#         self._parser.DefaultHandlerExpand = 
#         self._parser.NotStandaloneHandler = 
        self._parser.ExternalEntityRefHandler = self.external_entity_ref
    
    # Locator methods

    def getColumnNumber(self):
        return self._parser.ErrorColumnNumber

    def getLineNumber(self):
        return self._parser.ErrorLineNumber

    def getPublicId(self):
        return self._source.getPublicId()

    def getSystemId(self):
        return self._parser.GetBase()
    
    # internal methods

    # event handlers

    def start_element(self, name, attrs):
        self._cont_handler.startElement(name,
                                        AttributesImpl(attrs, attrs))

    def end_element(self, name):
        self._cont_handler.endElement(name)

    def start_element_ns(self, name, attrs):
        pair = split(name)
        if len(pair) == 1:
            pair = (None, name)
        else:
            pair = tuple(pair)

        self._cont_handler.startElementNS(pair, None,
                                          AttributesImpl(attrs, None))        

    def end_element_ns(self, name):
        pair = split(name)
        if len(pair) == 1:
            pair = (None, name)
        else:
            pair = tuple(pair)
            
        self._cont_handler.endElementNS(pair, None)

    def processing_instruction(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def character_data(self, data):
        self._cont_handler.characters(data)

    def start_namespace_decl(self, prefix, uri):
        self._cont_handler.startPrefixMapping(prefix, uri)

    def end_namespace_decl(self, prefix):
        self._cont_handler.endPrefixMapping(prefix)
        
    def unparsed_entity_decl(self, name, base, sysid, pubid, notation_name):
        self._dtd_handler.unparsedEntityDecl(name, pubid, sysid, notation_name)

    def notation_decl(self, name, base, sysid, pubid):
        self._dtd_handler.notationDecl(name, pubid, sysid)

    def external_entity_ref(self, context, base, sysid, pubid):
        source = self._ent_handler.resolveEntity(pubid, sysid)
        source = saxutils.prepare_input_source(source)
        # FIXME: create new parser, stack self._source and self._parser
        # FIXME: reuse code from self.parse(...)
        return 1
        
# ---
        
def create_parser():
    return ExpatDriver()
        
# ---

if __name__ == "__main__":
    p = create_parser()
    p.setContentHandler(saxutils.ContentGenerator())
    p.setErrorHandler(saxutils.ErrorPrinter())
    p.parse("test.xml")
