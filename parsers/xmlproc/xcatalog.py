
import catalog,xmlapp,xmlval

# --- An XCatalog parser factory

class XCatParserFactory:

    def make_parser(self,sysid):
        return XCatalogParser()

class FancyParserFactory:

    def make_parser(self,sysid):
        if sysid[-4:]==".soc":
            return catalog.CatalogParser()
        elif sysid[-4:]==".xml":
            return XCatalogParser()
        else:
            return catalog.CatalogParser()
    
# --- An XCatalog 0.1 parser

class XCatalogParser(catalog.AbstrCatalogParser,xmlapp.Application):

    def __init__(self):
        catalog.AbstrCatalogParser.__init__(self)
        xmlapp.Application.__init__(self)

    def parse_resource(self,sysid):
        parser=xmlval.XMLValidator()
        parser.set_application(self)
        parser.set_error_handler(self.err)
        parser.parse_resource(sysid)

    def handle_start_tag(self,name,attrs):
        if name=="Base":
            self.app.handle_base(attrs["HRef"]) 
        elif name=="Map":
            self.app.handle_public(attrs["PublicID"],attrs["HRef"])
        elif name=="Delegate":
            self.app.handle_delegate(attrs["PublicID"],attrs["HRef"])
        elif name=="Extend":
            self.app.handle_catalog(attrs["HRef"])        
