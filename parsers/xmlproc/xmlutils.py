"""
Some common declarations for the xmlproc system gathered in one file.
"""
   
import string,re,urlparse,os

from xmlapp import *
import errors

# Standard exceptions

class OutOfDataException(Exception):
    """An exception that signals that more data is expected, but the current
    buffer has been exhausted."""
    pass

# ==============================
# The general entity parser
# ==============================

class EntityParser:
    """A generalized parser for XML entities, whether DTD, documents or even
    catalog files."""

    def __init__(self):
        # --- Creating support objects
        self.err=ErrorHandler(self)
        self.ent=EntityHandler(self.err)
        self.isf=InputSourceFactory()
        self.pubres=PubIdResolver()
        self.data_charset="iso-8859-1"
        self.errors=errors.get_error_list("en")
        
        self.reset()

    def set_error_language(self,language):
        """Sets the language in which errors are reported. (ISO 3166 codes.)
        Throws a KeyError if the language is not supported."""
        self.errors=errors.get_error_list(string.lower(language))

    def set_error_handler(self,err):
        "Sets the object to send error events to."
        self.err=err

    def set_pubid_resolver(self,pubres):
        self.pubres=pubres
        
    def set_entity_handler(self,ent):
        "Sets the object that resolves entity references."
        self.ent=ent

    def set_inputsource_factory(self,isf):
        "Sets the object factory used to create input sources from sysids."
        self.isf=isf

    def set_data_charset(self,charset):
        """Tells the parser which character encoding to use when reporting data
        to applications."""
        self.data_charset=charset
        
    def parse_resource(self,sysID,bufsize=16384):
        """Begin parsing an XML entity with the specified public and
        system identifiers (the system identifier, a URI, is required).
        Only used for the document entity, not to handle subentities, which
        open_entity takes care of."""

        self.current_sysID=sysID
        try:
            infile=self.isf.create_input_source(sysID)
        except IOError,e:
            self.report_error(3000,sysID)
            return
        
        self.read_from(infile,bufsize)
        infile.close()
        self.flush()
        self.parseEnd()

    def open_entity(self,sysID):
        """Starts parsing a new entity, pushing the old onto the stack. This
        method must not be used to start parsing, use parse_resource for
        that."""

        sysID=join_sysids(self.get_current_sysid(),sysID)
            
        try:
            inf=self.isf.create_input_source(sysID)
        except IOError,e:
            self.report_error(3000,sysID)
            return

        self.ent_stack.append(self.get_current_sysid(),self.data,self.pos,\
                              self.line,self.last_break,self.datasize,\
                              self.last_upd_pos,self.block_offset)
        
        self.current_sysID=sysID
        self.pos=0
        self.line=1
        self.last_break=0
        self.data=""
        
        self.read_from(inf)

        self.flush()
        self.pop_entity()

    def push_entity(self,sysID,contents):
        """Parse some text and consider it a new entity, making it possible
        to return to the original entity later."""
        self.ent_stack.append(self.get_current_sysid(),self.data,self.pos,\
                              self.line,self.last_break,self.datasize,\
                              self.last_upd_pos,self.block_offset)

        self.data=contents
        self.current_sysID=sysID
        self.pos=0
        self.line=1
        self.last_break=0
        self.datasize=len(contents)
        self.last_upd_pos=0

    def pop_entity(self):
        "Skips out of the current entity and back to the previous one."

        if self.ent_stack==[]: self.report_error(4000)

        (self.current_sysID,self.data,self.pos,self.line,self.last_break,\
         self.datasize,self.last_upd_pos,self.block_offset)=self.ent_stack[-1]

        del self.ent_stack[-1]
        self.final=0
        
    def read_from(self,fileobj,bufsize=16384):
        """Reads data from a file-like object until EOF. Does not close it.
        **WARNING**: This method does not call the parseStart/parseEnd methods,
        since it does not know if it may be called several times. Use
        parse_resource if you just want to read a file."""
        while 1:
            buf=fileobj.read(bufsize)
            if buf=="": break

            try:
                self.feed(buf)
            except OutOfDataException,e:
                break

    def reset(self):
        """Resets the parser, losing all unprocessed data."""
        self.ent_stack=[]
        self.open_ents=[]  # Used to test for entity recursion
        self.current_sysID="Unknown"
        self.first_feed=1

        # Block information
        self.data=""
        self.final=0
        self.datasize=0
        self.start_point=-1
        
        # Location tracking
        self.line=1
        self.last_break=0
        self.block_offset=0 # Offset from start of stream to start of cur block
        self.pos=0
        self.last_upd_pos=0
            
    def feed(self,new_data):
        """Accepts more data from the data source. This method must
        set self.datasize and correctly update self.pos and self.data."""
        if self.first_feed:
            self.first_feed=0                    
            self.parseStart()


        self.update_pos() # Update line/col count
        
        if self.start_point==-1:
            self.block_offset=self.block_offset+self.datasize
            self.data=self.data[self.pos:]
            self.last_break=self.last_break-self.pos  # Keep track of column
            self.pos=0
            self.last_upd_pos=0

        # Adding new data and doing line end normalization
        self.data=string.replace(self.data+new_data,
                                 "\015\012","\012")
        self.datasize=len(self.data)

        self.do_parse()
        
    def close(self):
        "Closes the parser, processing all remaining data. Calls parseEnd."
        self.flush()
        self.parseEnd()        
        
    def parseStart(self):
        "Called before the parse starts to notify subclasses."
        pass

    def parseEnd(self):
        "Called when there are no more data to notify subclasses."
        pass

    def flush(self):
        "Parses any remnants of data in the last block."
        if not self.pos+1==self.datasize:
            self.final=1
            try:
                self.do_parse()
            except OutOfDataException,e:
                self.report_error(3001)
                
    # --- GENERAL UTILITY
    
    # --- LOW-LEVEL SCANNING METHODS

    def set_start_point(self):
        """Stores the current position and tells the parser not to forget any
        of the data beyond this point until get_region is called."""
        self.start_point=self.pos

    def store_state(self):
        """Makes the parser remember where we are now, so we can go back
        later with restore_state."""
        self.set_start_point()
        self.old_state=(self.last_upd_pos,self.line,self.last_break)

    def restore_state(self):
        """Goes back to a state previously remembered with store_state."""
        self.pos=self.start_point
        self.start_point=-1
        (self.last_upd_pos,self.line,self.last_break)=self.old_state
        
    def get_region(self):
        """Returns the area from start_point to current position and remove
        start_point."""
        data=self.data[self.start_point:self.pos]
        self.start_point=-1
        return data

    def find_reg(self,regexp,required=1):
        """Moves self.pos to the first character that matches the regexp and
        returns everything from pos and up to (but not including) that
        character."""
        oldpos=self.pos
        mo=regexp.search(self.data,self.pos)
        if mo==None:
            if self.final and not required:                
                self.pos=len(self.data)   # Just moved to the end
                return self.data[oldpos:]            
                
            raise OutOfDataException()
                
        self.pos=mo.start(0)
        return self.data[oldpos:self.pos]
    
    def scan_to(self,target):
        "Moves self.pos to beyond target and returns skipped text."
        new_pos=string.find(self.data,target,self.pos)
        if new_pos==-1:
            raise OutOfDataException()
        res=self.data[self.pos:new_pos]
        self.pos=new_pos+len(target)
        return res

    def get_index(self,target):
        "Finds the position where target starts and returns it."
        new_pos=string.find(self.data,target,self.pos)
        if new_pos==-1:
            raise OutOfDataException()
        return new_pos
    
    def test_str(self,test_str):
        "See if text at current position matches test_str, without moving."
        if self.datasize-self.pos<len(test_str) and not self.final:
            raise OutOfDataException()
        return self.data[self.pos:self.pos+len(test_str)]==test_str
    
    def now_at(self,test_str):
        "Checks if we are at this string now, and if so skips over it."
        if self.datasize-self.pos<len(test_str) and not self.final:
            raise OutOfDataException()
        
        if self.data[self.pos:self.pos+len(test_str)]==test_str:
            self.pos=self.pos+len(test_str)
            return 1
        else:
            return 0
    
    def skip_ws(self,necessary=0):
        "Skips over any whitespace at this point."
        start=self.pos
        
        try:
            while self.data[self.pos] in whitespace:
                self.pos=self.pos+1
        except IndexError:
            if necessary and start==self.pos:
                if self.final:
                    self.report_error(3002)
                else:
                    raise OutOfDataException()

    def test_reg(self,regexp):
        "Checks if we match the regexp."
        if self.pos>self.datasize-5 and not self.final:
            raise OutOfDataException()
        
        return regexp.match(self.data,self.pos)!=None
            
    def get_match(self,regexp):
        "Returns the result of matching the regexp and advances self.pos."
        if self.pos>self.datasize-5 and not self.final:
            raise OutOfDataException()

        ent=regexp.match(self.data,self.pos)
        if ent==None:
            self.report_error(reg2code[regexp.pattern])
            return ""

        end=ent.end(0) # Speeds us up slightly
        if end==self.datasize:
            raise OutOfDataException()

        self.pos=end
        return ent.group(0)

    def update_pos(self):
        "Updates (line,col)-pos by checking processed blocks."
        breaks=string.count(self.data,"\n",self.last_upd_pos,self.pos)
        self.last_upd_pos=self.pos

        if breaks>0:
            self.line=self.line+breaks
            self.last_break=string.rfind(self.data,"\n",0,self.pos)

    def get_wrapped_match(self,wraps):
        "Returns a contained match. Useful for regexps inside quotes."
        found=0
        for (wrap,regexp) in wraps:
            if self.test_str(wrap):
                found=1
                self.pos=self.pos+len(wrap)
                break

        if not found:
            msg=""
            for (wrap,regexp) in wraps[:-1]:
                msg="%s'%s', " % (msg,wrap)
            self.report_error(3004,(msg[:-2],wraps[-1][0]))

        data=self.get_match(regexp)
        if not self.now_at(wrap):
            self.report_error(3005,wrap)

        return data

    #--- ERROR HANDLING

    def report_error(self,number,args=None):
        try:
            msg=self.errors[number]
            if args!=None:
                msg=msg % args
        except KeyError:
            msg=self.errors[4002] # Unknown err msg :-)
        
        if number<2000:
            self.err.warning(msg)
        elif number<3000:
            self.err.error(msg)
        else:
            # Make parser stop reporting data events!
            self.err.fatal(msg)
    
    #--- USEFUL METHODS

    def get_current_sysid(self):
        "Returns the sysid of the file we are reading now."
        return self.current_sysID

    def set_sysid(self,sysID):
        "Sets the current system identifier. Does not store the old one."
        self.current_sysID=sysID

    def get_offset(self):
        "Returns the current offset from the start of the stream."
        return self.block_offset+self.pos
        
    def get_line(self):
        "Returns the current line number."
        self.update_pos()
        return self.line

    def get_column(self):
        "Returns the current column position."
        self.update_pos()
        return self.pos-self.last_break  

    def is_root_entity(self):
        "Returns true if the current entity is the root entity."
        return self.ent_stack==[]

    def is_external(self):
        """Returns true if the current entity is an external entity. The root
        (or document) entity is not considered external."""
        return self.ent_stack!=[] and \
               self.ent_stack[0][0]!=self.get_current_sysid()
    
# --- A collection of useful functions

# Utility functions

def unhex(hex_value):
    "Converts a string hex-value to an integer."

    sum=0
    for char in hex_value:
        sum=sum*16
        char=ord(char)
        
        if char<58 and char>=48:
            sum=sum+(char-48)
        elif char>=97 and char<=102:
            sum=sum+(char-87)
        elif char>=65 and char<=70:
            sum=sum+(char-55)
        # else ERROR, but it can't occur here

    return sum

def matches(regexp,str):
    mo=regexp.match(str)
    return mo!=None and len(mo.group(0))==len(str)

def join_sysids(base,url):
    if urlparse.urlparse(base)[0]=="":
        return os.path.join(os.path.split(base)[0],url)
    else:
        return urlparse.urljoin(base,url)

# --- Some useful regexps

namestart="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_:"
namechars=namestart+"0123456789.-"
whitespace="\n\t \r"

reg_ws=re.compile("[\n\t \r]+")
reg_ver=re.compile("[-a-zA-Z0-9_.:]+")
reg_enc_name=re.compile("[A-Za-z][-A-Za-z0-9._]*")
reg_std_alone=re.compile("yes|no")
reg_comment_content=re.compile("([^-]|-[^-])*")
reg_name=re.compile("[A-Za-z_:][\-A-Za-z_:.0-9]*")
reg_names=re.compile("[A-Za-z_:][\-A-Za-z_:.0-9]*"
                     "([\n\t \r]+[A-Za-z_:][\-A-Za-z_:.0-9]*)*")
reg_nmtoken=re.compile("[\-A-Za-z_:.0-9]+")
reg_nmtokens=re.compile("[\-A-Za-z_:.0-9]+([\n\t \r]+[\-A-Za-z_:.0-9]+)*")
reg_sysid_quote=re.compile("[^\"]*")
reg_sysid_apo=re.compile("[^']*")
reg_pubid_quote=re.compile("[- \n\t\ra-zA-Z0-9'()+,./:=?;!*#@$_%]*")
reg_pubid_apo=re.compile("[- \n\t\ra-zA-Z0-9()+,./:=?;!*#@$_%]*")
reg_start_tag=re.compile("<[A-Za-z_:]")
reg_quoted_attr=re.compile("[^<\"]*")
reg_apo_attr=re.compile("[^<']*")
reg_c_data=re.compile("[<&]")
reg_pe_ref=re.compile("%[A-Za-z_:][\-A-Za-z_:.0-9]*;")

reg_ent_val_quote=re.compile("[^\"]+")
reg_ent_val_apo=re.compile("[^\']+")

reg_attr_type=re.compile(r"CDATA|IDREFS|IDREF|ID|ENTITY|ENTITIES|NMTOKENS|"
                         "NMTOKEN")
reg_attr_def=re.compile(r"#REQUIRED|#IMPLIED")

reg_digits=re.compile("[0-9]+")
reg_hex_digits=re.compile("[0-9a-fA-F]+")

reg_res_pi=re.compile("xml",re.I)

reg_int_dtd=re.compile("\"|'|<\\?|<!--|\\]>|<!\\[")

reg_attval_stop_quote=re.compile("<|&|\"")
reg_attval_stop_sing=re.compile("<|&|'")

reg_decl_with_pe=re.compile("<(![^-\[]|\?)")
reg_subst_pe_search=re.compile(">|%")

# RFC 1766 language codes

reg_lang_code=re.compile("([a-zA-Z][a-zA-Z]|[iIxX]-([a-zA-Z])+)(-[a-zA-Z])*")

# Mapping regexps to error codes
# NB: 3900 is reported directly from _get_name

reg2code={
    reg_name.pattern : 3900, reg_ver.pattern : 3901,
    reg_enc_name.pattern : 3902, reg_std_alone.pattern : 3903,
    reg_comment_content.pattern : 3904, reg_hex_digits.pattern : 3905,
    reg_digits.pattern : 3906, reg_pe_ref.pattern : 3907,
    reg_attr_type.pattern : 3908, reg_attr_def.pattern : 3909,
    reg_nmtoken.pattern : 3910}
    
# Some useful variables

predef_ents={"lt":"&#60;","gt":"&#62;","amp":"&#38;","apos":"&#39;",
             "quot":'&#34;'}

# Translation tables

ws_trans=string.maketrans("\r\t\n","   ")  # Whitespace normalization
id_trans=string.maketrans("","")           # Identity transform 
