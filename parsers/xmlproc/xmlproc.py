"""
The main module of the parser. All other modules will be imported into this
one, so this module is the only one one needs to import. For validating
parsing, import xmlval instead.
"""
   
import re,string,sys,urllib,urlparse,types

from xmlutils import *
from xmlapp import *
from xmldtd import *

version="0.52"

# ==============================
# Common code for the parsers
# ==============================

class XMLCommonParser(EntityParser):

    def parse_external_id(self,required=0,sysidreq=1):
        """Parses an external ID declaration and returns a tuple consisting
        of (pubid,sysid). If the required attribute is false neither SYSTEM
        nor PUBLIC identifiers are required. If sysidreq is false a SYSTEM
        identifier is not required after a PUBLIC one."""

        pub_id=None
        sys_id=None
        
        if self.now_at("SYSTEM"):
            self.skip_ws(1)
            sys_id=self.get_wrapped_match([("\"",reg_sysid_quote),\
                                           ("'",reg_sysid_apo)])
        elif self.now_at("PUBLIC"):
            self.skip_ws(1)
            pub_id=self.get_wrapped_match([("\"",reg_pubid_quote),\
                                           ("'",reg_pubid_apo)])
            pub_id=string.join(string.split(pub_id))

            if sysidreq:
                self.skip_ws(1)
                sys_id=self.get_wrapped_match([("\"",reg_sysid_quote),\
                                               ("'",reg_sysid_apo)])
            else:
                self.skip_ws()
                if self.test_str("'") or self.test_str('"'):
                    sys_id=self.get_wrapped_match([("\"",reg_sysid_quote),\
                                                   ("'",reg_sysid_apo)])
        else:
            if required: self.report_error(3006)

        return (pub_id,sys_id)

    # --- Namespace name mangling

    def process_name(self,name):    
        pos=string.find(name,":")
        if pos!=-1:
            prefix=name[:pos]
            if prefix=="xmlns" or prefix=="xml":
                return name
            
            try:
                name=self.namespaces[prefix]+" "+name[pos+1:]
            except KeyError:
                self.report_error(1000,prefix)

        return name

    # --- EONamespaces

    def __get_quoted_string(self):
        "Returns the contents of a quoted string at current position."
        try:
            quo=self.data[self.pos]
        except IndexError:
            raise OutOfDataException()
            
        if not (self.now_at('"') or self.now_at("'")):
            self.report_error(3004,("'\"'","'"))
            self.scan_to(">")
            return ""

        return self.scan_to(quo)
    
    def parse_xml_decl(self):
        "Parses the contents of the XML declaration from after the '<?xml'."

        textdecl=self.is_external() # If this is an external entity, then this
                                    # is a text declaration, not an XML decl
        
        self.update_pos()
        if self.get_column()!=5 or self.get_line()!=1:
            if textdecl:
                self.report_error(3007)
            else:    
                self.report_error(3008)
            
        if self.seen_xmldecl: # Set in parse_pi, to avoid block problems
            if textdecl:
                self.report_error(3009)
            else:
                self.report_error(3010)

        enc=None
        sddecl=None
        ver=None
        self.skip_ws()
        
        if self.now_at("version"):
            self.skip_ws()
            if not self.now_at("="): self.report_error(3005,"=")
            self.skip_ws()
            ver=self.__get_quoted_string()
            if reg_ver.match(ver)==None:
                self.report_error(3901)
            
            if ver!="1.0":
                self.report_error(1001)

            self.skip_ws()
        elif not textdecl:
            self.report_error(3011)

        if self.now_at("encoding"):
            self.skip_ws()
            if not self.now_at("="): self.report_error(3005,"=")
            self.skip_ws()
            enc=self.__get_quoted_string()
            if reg_enc_name.match(enc)==None:
                self.report_error(3902)

            # Setting up correct conversion
            if string.lower(enc)!="iso-8859-1":
                self.report_error(1002,enc)
            
            self.skip_ws()          

        if self.now_at("standalone"):
            if textdecl:
                self.report_error(3012)
                sddecl="yes"
            else:
                self.skip_ws()
                if not self.now_at("="): self.report_error(3005,"=")
                self.skip_ws()
                sddecl=self.__get_quoted_string()
                if reg_std_alone.match(sddecl)==None:
                    self.report_error(3911)
                    
                self.standalone= sddecl=="yes"

                self.skip_ws()

        self.skip_ws()

        if isinstance(self,XMLProcessor):
            self.app.set_entity_info(ver,enc,sddecl)

    def parse_pi(self,handler):
        """Parses a processing instruction from after the '<?' to beyond
        the '?>'."""
        trgt=self.get_match(reg_name)

        if trgt=="xml":
            self.parse_xml_decl()
            if not self.now_at("?>"):
                self.report_error(3005,"?>")
            self.seen_xmldecl=1
        else:
            if reg_res_pi.match(trgt)!=None:
                if trgt=="xml:namespace":
                    self.report_error(1003)
                else:
                    self.report_error(1004)

            self.skip_ws()
            rem=self.scan_to("?>") # OutOfDataException if not found
            handler.handle_pi(trgt,rem)   

    def parse_comment(self,handler):
        "Parses the comment from after '<!--' to beyond '-->'."
        handler.handle_comment(self.get_match(reg_comment_content))
        if not self.now_at("-->"):
            self.report_error(3005,"-->")

    def _read_char_ref(self):
        "Parses a character reference and returns the character."
        if self.now_at("x"):
            digs=unhex(self.get_match(reg_hex_digits))
        else:
            digs=string.atoi(self.get_match(reg_digits))

        if not (digs==9 or digs==10 or digs==13 or \
                (digs>=32 and digs<=255)):
            if digs>255:
                self.report_error(1005,digs)
            else:
                self.report_error(3018,digs)
            return ""
        else:
            return chr(digs)

    def _get_name(self):
        """Parses the name at the current position and returns it. An error
        is reported if no name is present."""
        if self.pos>self.datasize-5 and not self.final:
            raise OutOfDataException()

        if self.data[self.pos] in namestart:
            start=self.pos
            self.pos=self.pos+1

            try:
                while self.data[self.pos] in namechars:
                    self.pos=self.pos+1

                return self.data[start:self.pos]
            except IndexError:
                if self.final:
                    return self.data[start:]
                else:
                    raise OutOfDataException()
        else:
            self.report_error(3900)
            return ""            
        
# ==============================
# A full well-formedness parser
# ==============================

class XMLProcessor(XMLCommonParser):
    "A parser that performs a complete well-formedness check."

    def __init__(self):        
        EntityParser.__init__(self)

        # Various handlers
        self.app=Application()
        self.dtd=WFCDTD(self.err)
        self.ent=self.dtd
        self.dtd_listener=None  # Only used to give to DTDParser

    def close(self):
        import types
        for name, value in self.__dict__.items():
            if type(value) == types.InstanceType:
                setattr(self, name, None)
        
    def set_application(self,app):
        "Sets the object to send data events to."
        self.app=app
        app.set_locator(self)
        
    def set_dtd_listener(self,listener):
        "Registers an object that listens for DTD parse events."
        self.dtd_listener=listener                

    def reset(self):
        EntityParser.reset(self)
        if hasattr(self,"dtd"):
            self.dtd.reset()

        # State vars
        self.stack=[]
        self.seen_root=0
        self.seen_doctype=0
        self.seen_xmldecl=0

    def do_parse(self):
        "Does the actual parsing."
        try:
            while self.pos+1<self.datasize:
                prepos=self.pos

                if self.data[self.pos]=="<":
                    if self.now_at("</"):
                        self.parse_end_tag()
                    elif not (self.test_str("<!") or self.test_str("<?")):
                        self.parse_start_tag()
                    elif self.now_at("<!--"):
                        self.parse_comment(self.app)
                    elif self.now_at("<?"):
                        self.parse_pi(self.app)
                    elif self.now_at("<![CDATA["):
                        self.parse_cdata()
                    elif self.now_at("<!DOCTYPE"):
                        self.parse_doctype()
                    else:
                        self.report_error(3013)
                        self.scan_to(">") # Avoid endless loops
                elif self.data[self.pos]=="&":
                    if self.now_at("&#"):
                        self.parse_charref()
                    else:
                        self.pos=self.pos+1  # Skipping the '&'
                        self.parse_ent_ref()
                else:
                    self.parse_data()

        except IndexError:
            # Means self.pos was outside the buffer when we did a raw compare.
            # This is both a little ugly and risky, but this loop is rather
            # time-critical, so we do it anyway.
            
            if self.final:
                raise IndexError()
            else:
                self.pos=prepos  # Didn't complete the construct            
        except OutOfDataException:
            if self.final:
                raise OutOfDataException()
            else:
                self.pos=prepos  # Didn't complete the construct

    def parseStart(self):
        "Must be called before parsing starts. (Notifies application.)"
        self.app.doc_start()

    def parseEnd(self):
        """Must be called when parsing is finished. (Does some checks and "
        "notifies the application.)"""      
        if self.stack!=[] and self.ent_stack==[]:
            self.report_error(3014,self.stack[-1])
        elif not self.seen_root:
            self.report_error(3015)

        self.app.doc_end()
            
    def parse_start_tag(self):
        "Parses the start tag."
        self.pos=self.pos+1 # Skips the '<'
        #name=self.get_match(reg_name)
        name=self._get_name()
        self.skip_ws()

        try:
            (attrs,fixeds)=self.dtd.attrinfo[name]
            attrs=attrs.copy()
        except KeyError:
            attrs={}
            fixeds={}
        
        if not (self.pos<self.datasize and (self.data[self.pos]==">" or \
                                       self.data[self.pos]=="/")):
            seen={}
            while not self.test_str(">") and not self.test_str("/>"):
                a_name=self._get_name()
                self.skip_ws()
                if not self.now_at("="):
                    self.report_error(3005,"=")
                    self.scan_to(">") ## Panic! Get out of the tag!
                    a_val=""
                    break
                self.skip_ws()

                a_val=self.parse_att_val()

                if seen.has_key(a_name):
                    self.report_error(3016,a_name)
                else:
                    seen[a_name]=1

                attrs[a_name]=a_val
                if fixeds.has_key(a_name) and fixeds[a_name]!=a_val:
                    self.report_error(2000,a_name)
                self.skip_ws()

        # --- Take care of the tag
            
        if self.stack==[] and self.seen_root:
            self.report_error(3017)
            
        self.seen_root=1
            
        if self.now_at(">"):
            self.app.handle_start_tag(name,attrs)
            self.stack.append(name)
        elif self.now_at("/>"):
            self.app.handle_start_tag(name,attrs)
            self.app.handle_end_tag(name)
        else:
            self.report_error(3004,("'>'","/>"))

    def parse_att_val(self):
        "Parses an attribute value and resolves all entity references in it."

        val=""
        if self.now_at('"'):
            delim='"'
            reg_attval_stop=reg_attval_stop_quote
        elif self.now_at("'"):
            delim="'"
            reg_attval_stop=reg_attval_stop_sing
        else:
            self.report_error(3004,("'","\""))
            self.scan_to(">")
            return        
                
        while 1:
            piece=self.find_reg(reg_attval_stop)
            val=val+string.translate(piece,ws_trans)

            if self.now_at(delim):
                break

            if self.now_at("&#"):
                val=val+self._read_char_ref()
            elif self.now_at("&"):
                #name=self.get_match(reg_name)
                name=self._get_name()

                if name in self.open_ents:
                    self.report_error(3019)
                    return
                else:
                    self.open_ents.append(name)
                
                try:
                    ent=self.ent.resolve_ge(name)
                    if ent.is_internal():
                        # Doing all this here sucks a bit, but...
                        self.push_entity(self.get_current_sysid(),\
                                         ent.value)

                        self.final=1 # Only one block

                        val=val+self.parse_literal_entval()
                        if not self.pos==self.datasize:
                            self.report_error(3001) # Thing started, not compl

                        self.pop_entity()
                    else:
                        self.report_error(3020)
                except KeyError,e:
                    self.report_error(3021,name) ## FIXME: Check standalone dcl

                del self.open_ents[-1]

            elif self.now_at("<"):
                self.report_error(3022)
            else:
                self.report_error(4001)
                
            if not self.now_at(";"):
                self.report_error(3005,";")
                self.scan_to(">")
                            
        return val

    def parse_literal_entval(self):
        "Parses a literal entity value for insertion in an attribute value."

        val=""
        reg_stop=re.compile("&")
                
        while 1:
            try:
                piece=self.find_reg(reg_stop)
            except OutOfDataException,e:
                # Only character data left
                val=val+string.translate(self.data[self.pos:],ws_trans)
                self.pos=self.datasize
                break
            
            val=val+string.translate(piece,ws_trans)

            if self.now_at("&#"):
                val=val+self._read_char_ref()           
            elif self.now_at("&"):
                #name=self.get_match(reg_name)
                name=self._get_name()

                if name in self.open_ents:
                    self.report_error(3019)
                    return ""
                else:
                    self.open_ents.append(name)
                
                try:
                    ent=self.ent.resolve_ge(name)
                    if ent.is_internal():
                        # Doing all this here sucks a bit, but...
                        self.push_entity(self.get_current_sysid(),\
                                         ent.value)

                        self.final=1 # Only one block

                        val=val+self.parse_literal_entval()
                        if not self.pos==self.datasize:
                            self.report_error(3001)

                        self.pop_entity()
                    else:
                        self.report_error(3020)
                except KeyError,e:
                    self.report_error(3021,name)               

                del self.open_ents[-1]
                    
            else:
                self.report_error(4001)
                
            if not self.now_at(";"):
                self.report_error(3005,";")
                self.scan_to(">")
                            
        return val
    
    def parse_end_tag(self):
        "Parses the end tag from after the '</' and beyond '>'."
        #name=self.get_match(reg_name)
        name=self._get_name()
        
        if not self.now_at(">"):
            self.skip_ws() # Probably rare to find whitespace here
            if not self.now_at(">"): self.report_error(3005,">")

        try:
            if not name==self.stack[-1]:
                self.report_error(3023,(name,self.stack[-1]))

                # Let's do some guessing in case we continue
                if len(self.stack)>1 and self.stack[-2]==name:
                    del self.stack[-1]
                    del self.stack[-1]
            else:
                del self.stack[-1]
        except IndexError,e:
            self.report_error(3024,name)

        self.app.handle_end_tag(name)

    def parse_data(self):
        "Parses character data."

        start=self.pos
        end=string.find(self.data,"<",self.pos)
        if end==-1:
            end=string.find(self.data,"&",self.pos)
            
            if end==-1:
                if not self.final:
                    raise OutOfDataException()

                end=self.datasize
        else:
            ampend=string.find(self.data,"&",self.pos,end)
            if ampend!=-1:
                end=ampend

        self.pos=end
        
        if string.find(self.data,"]]>",start,end)!=-1:
            self.pos=string.find(self.data,"]]>",start,end)
            self.report_error(3025)
            self.pos=self.pos+3 # Skipping over it

        if self.stack==[]:
            res=reg_ws.match(self.data,start)                
            if res==None or res.end(0)!=end:
                self.report_error(3026)
            self.app.handle_ignorable_data(self.data,start,end)
        else:
            self.app.handle_data(self.data,start,end)

    def parse_charref(self):
        "Parses a character reference."
        if self.now_at("x"):
            digs=unhex(self.get_match(reg_hex_digits))
        else:
            try:
                digs=string.atoi(self.get_match(reg_digits))
            except ValueError,e:
                self.report_error(3027)
                digs=None

        if not self.now_at(";"): self.report_error(3005,";")
        if digs==None: return
            
        if not (digs==9 or digs==10 or digs==13 or \
                (digs>=32 and digs<=255)):
            if digs>255:
                self.report_error(1005,digs)
            else:
                self.report_error(3018,digs)
        else:
            if self.stack==[]:
                self.report_error(3028)
            self.app.handle_data(chr(digs),0,1)

    def parse_cdata(self):
        "Parses a CDATA marked section from after the '<![CDATA['."
        new_pos=self.get_index("]]>")
        if self.stack==[]:
            self.report_error(3029)
        self.app.handle_data(self.data,self.pos,new_pos)
        self.pos=new_pos+3

    def parse_ent_ref(self):
        "Parses a general entity reference from after the '&'."
        #name=self.get_match(reg_name)
        name=self._get_name()
        if not self.now_at(";"): self.report_error(3005,";")

        try:
            ent=self.ent.resolve_ge(name)
        except KeyError,e:
            self.report_error(3021,name)
            return

        if ent.name in self.open_ents:
            self.report_error(3019)
            return
        else:
            self.open_ents.append(ent.name)

        if self.stack==[]:
            self.report_error(3030)
            
        if ent.is_internal():
            self.push_entity(self.get_current_sysid(),ent.value)
            self.do_parse()
            self.flush()
            self.pop_entity()
        else:
            if ent.notation!="":
                self.report_error(3031)

            tmp=self.seen_xmldecl
            self.seen_xmldecl=0 # Avoid complaints
            self.seen_root=0    # Haven't seen root in the new entity yet
            self.open_entity(self.pubres.resolve_entity_pubid(ent.get_pubid(),
                                                              ent.get_sysid()))
            self.seen_root=1 # Entity references only allowed inside elements
            self.seen_xmldecl=tmp
            
        del self.open_ents[-1]
        
    def parse_doctype(self):
        "Parses the document type declaration."

        if self.seen_doctype:
            self.report_error(3032)
        if self.seen_root:
            self.report_error(3033)
        
        self.skip_ws(1)
        #rootname=self.get_match(reg_name)
        rootname=self._get_name()
        self.skip_ws(1)

        (pub_id,sys_id)=self.parse_external_id()

        self.skip_ws()
        if pub_id!=None or sys_id!=None:
            self.app.handle_doctype(rootname,pub_id,sys_id)
        
        if self.now_at("["):
            self.parse_internal_dtd()    
        elif not self.now_at(">"):
            self.report_error(3005,">")

        self.dtd.prepare_for_parsing()
        self.seen_doctype=1 # Has to be at the end to avoid block trouble
    
    def parse_internal_dtd(self):
        "Parse the internal DTD beyond the '['."

        self.set_start_point() # Record start of int_subset, preserve data
        self.update_pos()
        line=self.line
        lb=self.last_break
        
        while 1:
            self.find_reg(reg_int_dtd)

            if self.now_at("\""): self.scan_to("\"")
            elif self.now_at("'"): self.scan_to("'")
            elif self.now_at("<?"): self.scan_to("?>")
            elif self.now_at("<!--"): self.scan_to("-->")
            elif self.now_at("<!["): self.scan_to("]]>")
            elif self.now_at("]>"): break

        # [:-2] cuts off the "]>" at the end
        self.handle_internal_dtd(line,lb,self.get_region()[:-2])
        
    def handle_internal_dtd(self,doctype_line,doctype_lb,int_dtd):
        "Handles the internal DTD."
        p=DTDParser()
        p.set_error_handler(self.err)
        p.set_dtd_consumer(self.dtd)
        if self.dtd_listener!=None:
            self.dtd.set_dtd_listener(self.dtd_listener)
        p.set_internal(1)
        self.err.set_locator(p)

        try:
            try:                
                p.line=doctype_line
                p.last_break=doctype_lb
                
                p.set_sysid(self.get_current_sysid())
                p.final=1
                p.feed(int_dtd)
            except OutOfDataException,e:
                self.report_error(3034)
        finally:
            self.err.set_locator(self)
            self.dtd.dtd_end()
                
# ==============================
# A DTD parser
# ==============================
            
class DTDParser(XMLCommonParser):
    "A parser for XML DTDs, both internal and external."

    def __init__(self):
        EntityParser.__init__(self)
        self.internal=0
        self.seen_xmldecl=0
        self.dtd=DTDConsumer(self)

        self.ignore=0 # Currently in a conditional section marked ignore?
        self.section_stack=[] # Conditional section nesting tracker

    def parseStart(self):
        self.dtd.dtd_start()

    def parseEnd(self):
        self.dtd.dtd_end()
        
    def set_dtd_consumer(self,dtd):
        "Tells the parser where to send DTD information."
        self.dtd=dtd
        
    def set_internal(self,yesno):
        "Tells the parser whether the DTD is internal or external."
        self.internal=yesno
        
    def do_parse(self):
        "Does the actual parsing."

        try:
            self.skip_ws()
            while self.pos<self.datasize:
                prepos=self.pos
                
                if self.now_at("<!ELEMENT"):
                    self.parse_elem_type()
                elif self.now_at("<!ENTITY"):
                    self.parse_entity()
                elif self.now_at("<!ATTLIST"):
                    self.parse_attlist()
                elif self.now_at("<!NOTATION"):
                    self.parse_notation()
                elif self.test_reg(reg_pe_ref):
                    self.parse_pe_ref()
                elif self.now_at("<?"):
                    self.parse_pi(self.dtd)
                elif self.now_at("<!--"):
                    self.parse_comment(self.dtd)
                elif self.now_at("<!["):
                    self.parse_conditional()
                elif self.now_at("]]>") and self.section_stack!=[]:
                    self.ignore=self.section_stack[-1]
                    del self.section_stack[-1]
                else:
                    self.report_error(3013)
                    self.pos=self.pos+1

                self.skip_ws()

        except OutOfDataException,e:
            if self.final:
                raise e
            else:
                self.pos=prepos

    def parse_entity(self):
        "Parses an entity declaration."

        self.skip_ws(1)
        if self.now_at("%"):
            pedecl=1
            self.skip_ws(1)
        else:
            pedecl=0
        
        #ent_name=self.get_match(reg_name)
        ent_name=self._get_name()
        self.skip_ws(1)

        (pub_id,sys_id)=self.parse_external_id(0)

        if sys_id==None:
            internal=1
            ent_val=self.parse_ent_repltext()
        else:
            internal=0

        if self.now_at("NDATA"):
            self.report_error(3002)
        else:
            self.skip_ws()
        
        if not internal and self.now_at("NDATA"):
            # Parsing the optional NDataDecl
            if pedecl:
                self.report_error(3035)
            self.skip_ws()

            #ndata=self.get_match(reg_name)
            ndata=self._get_name()
        else:
            ndata=""

        if not self.now_at(">"):
            self.report_error(3005,">")

        if pedecl:
            if internal:
                self.dtd.new_parameter_entity(ent_name,ent_val)
            else:
                self.dtd.new_external_pe(ent_name,pub_id,sys_id)
        else:
            if internal:
                self.dtd.new_general_entity(ent_name,ent_val)
            else:
                self.dtd.new_external_entity(ent_name,pub_id,sys_id,ndata)

    def parse_ent_repltext(self):
        """Parses an entity replacement text and resolves all character
        entity references in it."""

        val=""
        if self.now_at('"'):
            delim='"'
        elif self.now_at("'"):
            delim="'"
        else:
            self.report_error(3004,("'","\""))
            self.scan_to(">")
            return

        reg_stop=re.compile("%|&#|"+delim)              
        while 1:
            piece=self.find_reg(reg_stop)
            val=val+piece

            if self.now_at(delim):
                break

            if self.now_at("&#"):
                val=val+self._read_char_ref()
            elif self.now_at("%"):
                #name=self.get_match(reg_name)
                name=self._get_name()

                if self.internal:
                    self.report_error(3036)
                    val=val+"%"+name+";"
                else:
                    try:
                        ent=self.dtd.resolve_pe(name)
                        if ent.is_internal():
                            val=val+ent.value
                        else:
                            self.report_error(3037)
                    except KeyError,e:
                        self.report_error(3038,name)
            else:
                self.report_error(4001)
                
            if not self.now_at(";"):
                self.report_error(3005,";")
                self.scan_to(">")
                            
        return val
        
    def parse_notation(self):
        "Parses a notation declaration."
        self.skip_ws(1)
        #name=self.get_match(reg_name)
        name=self._get_name()
        self.skip_ws(1)

        (pubid,sysid)=self.parse_external_id(1,0)
        self.skip_ws()
        if not self.now_at(">"):
            self.report_error(3005,">")

        self.dtd.new_notation(name,pubid,sysid)

    def parse_pe_ref(self):
        "Parses a reference to a parameter entity."
        pe_name=self.get_match(reg_pe_ref)[1:-1]

        try:
            ent=self.dtd.resolve_pe(pe_name)
        except KeyError,e:
            self.report_error(3038,name)
            return 

        if ent.is_internal():
            self.push_entity(self.get_current_sysid(),ent.value)
            self.do_parse()
            self.pop_entity()
        else:
            sysid=self.pubres.resolve_pe_pubid(ent.get_pubid(),
                                               ent.get_sysid())
            self.open_entity(sysid) # Does parsing and popping
            
    def parse_attlist(self):
        "Parses an attribute list declaration."

        self.skip_ws(1)
        #elem=self.get_match(reg_name)
        elem=self._get_name()
        self.skip_ws(1)

        while not self.test_str(">"):
            #attr=self.get_match(reg_name)
            attr=self._get_name()
            self.skip_ws(1)

            if self.test_reg(reg_attr_type):
                a_type=self.get_match(reg_attr_type)
            elif self.now_at("NOTATION"):
                self.skip_ws(1)
                a_type=("NOTATION",self.__parse_list(reg_name,"|"))
            elif self.now_at("("):
                self.pos=self.pos-1 # Does not expect '(' to be skipped
                a_type=self.__parse_list(reg_nmtoken,"|")
            else:
                self.report_error(3039)
                self.scan_to(">")
                return
            
            self.skip_ws(1)

            if self.test_reg(reg_attr_def):
                a_decl=self.get_match(reg_attr_def)
                a_def=None
            elif self.now_at("#FIXED"):
                self.skip_ws(1)
                a_decl="#FIXED"
                a_def=self.parse_ent_repltext()
            else:
                a_decl="#DEFAULT"
                a_def=self.parse_ent_repltext()
            
            self.skip_ws()

            self.dtd.new_attribute(elem,attr,a_type,a_decl,a_def)

        self.pos=self.pos+1 # Skipping the '>'

    def parse_elem_type(self):
        "Parses an element type declaration."

        self.skip_ws(1)
        #elem_name=self.get_match(reg_name)
        elem_name=self._get_name()
        self.skip_ws(1)

        # content-spec
        if self.now_at("EMPTY"):
            elem_cont=None
        elif self.now_at("ANY"):
            elem_cont=1 
        elif self.now_at("("):
            elem_cont=self.parse_content_model()
        else:
            self.report_error(3004,("EMPTY, ANY","("))
            elem_cont=None

        self.skip_ws()
        if not self.now_at(">"):
            self.report_error(3005,">")

        self.dtd.new_element_type(elem_name,elem_cont)

    def parse_content_model(self,level=0):
        """Parses the content model of an element type declaration. Level
        tells the function if we are on the top level (=0) or not (=1)."""

        self.skip_ws()

        # Creates a content list with separator first
        cont_list=[]
        sep="" 
        
        if self.now_at("#PCDATA") and level==0:
            return self.parse_mixed_content_model()

        while 1:
            self.skip_ws()
            if self.now_at("("):
                cp=self.parse_content_model(1)
            else:
                #cp=self.get_match(reg_name)
                cp=self._get_name()

            if self.test_str("?") or self.test_str("*") or self.test_str("+"):
                mod=self.data[self.pos]
                self.pos=self.pos+1
            else:
                mod=""
            cont_list.append(ContentModel([cp],mod))

            self.skip_ws()
            if self.now_at(")"):
                break

            if sep=="":
                if self.test_str("|") or self.test_str(","):
                    sep=self.data[self.pos]
                else:
                    self.report_error(3004,("'|'",","))
                self.pos=self.pos+1
            else:
                if not self.now_at(sep):
                    self.report_error(3040)
                    self.scan_to(")")
                    
        if self.test_str("+") or self.test_str("?") or self.test_str("*"):
            mod=self.data[self.pos]
            self.pos=self.pos+1
        else:
            mod=""

        if sep==",":
            return SeqContentModel(cont_list,mod)
        elif sep=="|":
            return ChoiceContentModel(cont_list,mod)
        elif sep=="":
            if mod!="":
                return ContentModel(cont_list,mod)
            else:
                return cont_list[0] # Only a single object anyway

    def parse_conditional(self):
        "Parses a conditional section." 
        if self.internal:
            self.report_error(3041)
            ignore=1
            self.scan_to("[")
        else:
            self.skip_ws()

            if self.now_at("IGNORE"):
                ignore=1
            elif self.now_at("INCLUDE"):
                ignore=0
            else:
                self.report_error(3004,("'IGNORE'","INCLUDE"))
                self.scan_to("[")
                ignore=1

            self.skip_ws()
            if not self.now_at("["):
                self.report_error(3005,"[")

        self.section_stack.append(self.ignore)
        self.ignore=ignore or self.ignore                   
        
    def parse_mixed_content_model(self):
        "Parses mixed content models. Ie: ones containing #PCDATA."

        cont_list=[ContentModel(["#PCDATA"],"")]
        sep="?"

        while 1:
            self.skip_ws()
            if self.now_at("|"):
                sep="|"
            elif self.now_at(")"):
                break
            else:
                self.report_error(3005,"|")
                self.scan_to(">")

            self.skip_ws()
            cont_list.append(ContentModel([self.get_match(reg_name)],""))

        if sep=="|" and not self.now_at("*"):
            self.report_error(3005,"*")

        return ChoiceContentModel(cont_list,"*") 
        
    def __parse_list(self, elem_regexp, separator):
        "Parses a '(' S? elem_regexp S? separator ... ')' list. (Internal.)"

        list=[]
        self.skip_ws()
        if not self.now_at("("):
            self.report_error(3005,"(")

        while 1:
            self.skip_ws()
            list.append(self.get_match(elem_regexp))
            self.skip_ws()
            if self.now_at(")"):
                break
            elif not self.now_at(separator):
                self.report_error(3004,("')'",separator))
                break

        return list
                
    def is_external(self):
        return not self.internal
