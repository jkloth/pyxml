
"""This is the parts of xmlproc that are specific to validation. They
are an application class that receive data from the parser and a
subclass of the parser object that sets this up."""

# Todo:
#
# - make parser report correct position inside internal entities
# - test position reporting and make it work consistently
#   - new attribute: self.last_pos, position at start of construct
# - handle XML decl in external entities
# - clean up entity reference handling in attribute values (parse_string)
# - make position reporting work in XML DTD with parameter entities as well
# - THINK THIS THROUGH AND MAKE A CONSISTENT POLICY FOR INTERNAL
#   AND EXTERNAL ENTITIES OF DIFFERENT TYPES...
#
# - run through the entire test case collection
#
# - implement notation attributes
#
# - BUGFIX:  normalize whitespace in FPIs
#
# - validate the document type itself:
#   - only allow elem types once in mixed-content models
#   - attr default val: must be legal
#   - standalone doc decl VC
#   - external entity notation: must match declared notation
# - report interoperability violations
# - when fatal error has occurred, don't send more data to app
#
# - WFCs:
#   - Well-Formedness Constraint: Entity Declared
#
# - move more stuff up into AbstractXML (DTDParser must use app attribute)
# - move entityparser down into xmlutils
#
# - parameter entities in DTD
#
# customization:
# - buffer size
# - catalog file
# - warnings (language, type)

import urlparse

from xmlproc import *
from xmldtd import *
from xmlapp import *

# ==============================
# The validator class
# ==============================

class XMLValidator:
    """XML parser that validates a document and does some of what is required
    of a validating parser, like adding fixed and default attribute values
    etc."""
    
    def __init__(self):
	self.parser=XMLProcessor()
        self.app=Application()
        self.reset()

    def parse_resource(self,sysid):
        self.parser.parse_resource(sysid)

    def reset(self):
        self.dtd=CompleteDTD(ErrorHandler(self.parser))
	self.val=ValidatingApp(self.dtd)
	self.val.set_real_app(self.app)

        self.parser.reset()
	self.parser.set_application(self.val)
        self.parser.dtd=self.dtd
	self.parser.ent=self.dtd
        
    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()
        
    def set_application(self,app):
        self.app=app
	self.val.set_real_app(self.app)
	app.set_locator(self.parser)
	
    def set_error_handler(self,err):
	self.parser.set_error_handler(err)
	self.dtd.set_error_handler(err)
	self.val.set_error_handler(err)

    def set_dtd_listener(self,dtd_listener):
	self.parser.set_dtd_listener(dtd_listener)

    def set_inputsource_factory(self,isf):
        self.parser.set_inputsource_factory(isf)

    def set_pubid_resolver(self,pubres):
        self.val.set_pubid_resolver(pubres)
        self.parser.set_pubid_resolver(pubres)
	
    def get_dtd(self):
        return self.dtd

    def get_current_sysid(self):
	return self.parser.get_current_sysid()

    def get_offset(self):
	return self.parser.get_offset()
	
    def get_line(self):
	return self.parser.get_line()

    def get_column(self):
	return self.parser.get_column()

    def parseStart(self):
        self.parser.parseStart()

    def parseEnd(self):
        self.parser.parseEnd()

    def read_from(self,file):
        self.parser.read_from(file)

    def flush(self):
        self.parser.flush()
	    
# ==============================
# Application object that checks the document
# ==============================

class ValidatingApp(Application):
    "The object that uses the DTD to actually validate XML documents."

    def __init__(self,dtd):
	self.dtd=dtd
	self.cur_elem=None
	self.cur_state=0
	self.stack=[]
        self.pubres=PubIdResolver()
	self.err=ErrorHandler(None)
	self.ids={}
	self.idrefs=[]
	self.realapp=Application()
	
    def set_real_app(self,app):
	self.realapp=app

    def set_pubid_resolver(self,pubres):
        self.pubres=pubres
                
    def set_locator(self,locator):
	Application.set_locator(self,locator)
	self.realapp.set_locator(locator)

    def set_error_handler(self,err):
	self.err=err

    def handle_start_tag(self,name,attrs):
	decl_root=self.dtd.get_root_elem()
	
	if self.cur_elem!=None:
            if self.cur_state!=-1:
                next=self.cur_elem.next_state(self.cur_state,name)
                if next==0:
                    self.err.error("Element '%s' not allowed here" % name)
                else:
                    self.cur_state=next

	    self.stack.append(self.cur_elem,self.cur_state)
	elif decl_root!=None and name!=decl_root:
	    self.err.error("Document root element '%s' does not match "
			   "declared root element" % name)

	try:
	    self.cur_elem=self.dtd.get_elem(name)
	    try:
		self.cur_state=self.cur_elem.get_start_state()
	    except KeyError,e:
		self.err.error("Bad content model: '%s'. (Internal error.)" %\
			       e)
		self.cur_state=1

	    self.validate_attributes(self.dtd.get_elem(name),attrs)
		
	except KeyError,e:
	    self.err.error("Element '%s' not declared" % name)
	    self.cur_state=-1

	self.realapp.handle_start_tag(name,attrs)
	
    def handle_end_tag(self,name):
	"Notifies the application of end tags (and empty element tags)."
	if self.cur_elem!=None and \
	   not self.cur_elem.final_state(self.cur_state):
	    self.err.error("Element '%s' ended, but not finished" % name)
	
	if self.stack!=[]:
	    (self.cur_elem,self.cur_state)=self.stack[-1]
	    del self.stack[-1]

	self.realapp.handle_end_tag(name)
    
    def handle_data(self,data,start,end):
	"Notifies the application of character data."
	if self.cur_elem!=None and self.cur_state!=-1:
	    next=self.cur_elem.next_state(self.cur_state,"#PCDATA")

	    if next==0:
		mo=reg_ws.match(data[start:end])
		if mo!=None and len(mo.group(0))==len(data[start:end]):
		    self.realapp.handle_ignorable_data(data,start,end)
		    return
		else:
		    self.err.error("Character data not allowed here")
	    else:
		self.cur_state=next

	self.realapp.handle_data(data,start,end)

    def validate_attributes(self,element,attrs):
	"""Validates the attributes against the element declaration and adds
	fixed and default attributes."""

	# Check the values of the present attributes
	for attr in attrs.keys():
	    try:
		decl=element.get_attr(attr)
	    except KeyError,e:
		self.err.error("Unknown attribute '%s'" % attr)
                return
        
            if decl.type!="CDATA":
                res=""
                for elem in string.split(attrs[attr]," "):
                    if elem!="":
                        res=res+elem+" "
                        
                attrs[attr]=res[:-1]
            
            decl.validate(attrs[attr],self.err)
                
	    if decl.type=="ID":
		if self.ids.has_key(attrs[attr]):
		    self.err.error("ID '%s' appears more than once in "
				   "document" % attrs[attr])
		self.ids[attrs[attr]]=""
	    elif decl.type=="IDREF":
		self.idrefs.append((self.locator.get_line(),
				    self.locator.get_column(),
				    attrs[attr]))
	    elif decl.type=="IDREFS":
		for idref in string.split(attrs[attr]):
		    self.idrefs.append((self.locator.get_line(),
					self.locator.get_column(),
					idref))
	    elif decl.type=="ENTITY":
                try:
                    ent=self.dtd.resolve_ge(attrs[attr])
		    if ent.notation=="":
			self.err.error("Only unparsed entities allowed here")
		    else:
                        try:
                            self.dtd.get_notation(ent.notation)
                        except KeyError,e:
                            self.err.error("Notation '%s' not declared" %\
                                           ent.notation)
                except KeyError,e:
                    self.err.fatal("Unknown entity '%s'" % name)

	    elif decl.type=="ENTITIES":
		for ent_ref in string.split(attrs[attr]):
                    try:
                        ent=self.dtd.resolve_ge(attrs[ent_ref])

			if ent.notation=="":
			    self.err.error("Only unparsed entities allowed "
					   "here")
			else:
                            try:
                                self.dtd.get_notation(ent.notation)
                            except KeyError,e:
                                self.err.error("Notation '%s' not declared" %\
                                               ent.notation)
                    except KeyError,e:
                        self.err.fatal("Unknown entity '%s'" % name)

        # Check for missing required attributes
	for attr in element.get_attr_list():
	    decl=element.get_attr(attr)
	    if decl.decl=="#REQUIRED" and not attrs.has_key(attr):
		self.err.error("Required attribute %s not present" % attr)

    def doc_end(self):
	for (line,col,id) in self.idrefs:
	    if not self.ids.has_key(id):
		self.err.error("IDREF referred to non-existent ID '%s'" % id)

	self.realapp.doc_end()

    def handle_doctype(self,rootname,pub_id,sys_id):
	self.dtd.root_elem=rootname

	prev_loc=self.err.get_locator()
	p=DTDParser()
	p.set_error_handler(self.err)
	p.set_dtd_consumer(self.dtd)

        # === UGLY: SHOULD REALLY ACCESS THE PARSER IN SOME OTHER WAY HERE!
        if self.locator.dtd_listener!=None:
            self.dtd.set_dtd_listener(self.locator.dtd_listener)
	self.err.set_locator(p)

        if pub_id!=None:
            sys_id=self.pubres.resolve_doctype_pubid(pub_id,sys_id)

        try:
            sys_id=urlparse.urljoin(p.get_current_sysid(),sys_id)
            p.parse_resource(sys_id)
        finally:
            self.err.set_locator(prev_loc)

	self.realapp.handle_doctype(rootname,pub_id,sys_id)
	    
    # --- These methods added only to make this hanger-on application
    #     invisible to external users.
		
    def doc_start(self):
	self.realapp.doc_start()
	
    def handle_comment(self,data):
	self.realapp.handle_comment(data)

    def handle_ignorable_data(self,data,start,end):
	self.realapp.handle_ignorable_data(data,start,end)

    def handle_pi(self,target,data):
	self.realapp.handle_pi(target,data)

    def set_entity_info(self,xmlver,enc,sddecl):
	self.realapp.set_entity_info(xmlver,enc,sddecl)
