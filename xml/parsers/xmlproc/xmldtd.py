
"""These are the DTD-aware classes of xmlproc. They provide both the
DTD event consumers for the DTD parser as well as the objects that
store DTD information for retrieval by clients (including the
validating parser)."""

import types

from xmlutils import *
from xmlapp import *

# ==============================
# WFC-DTD
# ==============================

class WFCDTD(DTDConsumer):
    "DTD-representing class for the WFC parser."

    def __init__(self,parser):
	DTDConsumer.__init__(self,parser)
        self.dtd_listener=DTDConsumer(parser)        
        self.reset()

    def reset(self):
        "Clears all DTD information."
	self.gen_ents={}
	self.param_ents={}
	self.elems={}
        self.namespaces={}
        self.attrinfo={}

	# Adding predefined entities
	for name in predef_ents.keys():
	    self.new_general_entity(name,predef_ents[name])        
            
    def set_dtd_listener(self,listener):
        "Registers an object that listens for DTD parse events."
        self.dtd_listener=listener
            
    def resolve_pe(self,name):
	"""Returns the entitiy object associated with this parameter entity
        name. Throws KeyError if the entity is not declared."""
        return self.param_ents[name]

    def resolve_ge(self,name):
	"""Returns the entitiy object associated with this general entity
        name. Throws KeyError if the entity is not declared."""
        return self.gen_ents[name]

    def get_elem(self,name):
	"""Returns the declaration of this element. Throws KeyError if the
	element does not exist."""
	return self.elems[name]

    def get_namespace(self,prefix):
        """Returns the namespace declared with this prefix. Throws a KeyError
        if the prefix is not declared."""
        return self.namespaces[prefix]

    def get_elements(self):
        "Returns a list of all declared element names."
        return self.elems.keys()

    # --- Shortcut information for validation

    def prepare_for_parsing(self):
        "Stores shortcut information."
        self.attrinfo={}
        for elem in self.elems.values():
            self.attrinfo[elem.get_name()]=(elem.get_default_attributes(),
                                            elem.get_fixed_attributes())

    def get_element_info(self,name):
        return self.attrinfo[name]
            
    # --- Parse events
    
    def new_attribute(self,elem,attr,a_type,a_decl,a_def):
	"Receives the declaration of a new attribute."
        self.dtd_listener.new_attribute(elem,attr,a_type,a_decl,a_def)
        
        if not self.elems.has_key(elem):
	    self.elems[elem]=ElementTypeAny(elem) # Adding dummy

        self.elems[elem].add_attr(attr,a_type,a_decl,a_def,self.parser)
        
    # --- Echoing DTD parse events
    
    def new_general_entity(self,name,val):
        ent=InternalEntity(name,val)
	self.gen_ents[ent.name]=ent
        self.dtd_listener.new_general_entity(name,val)

    def new_parameter_entity(self,name,val):
        ent=InternalEntity(name,val)
	self.param_ents[ent.name]=ent
        self.dtd_listener.new_parameter_entity(name,val)

    def new_external_entity(self,ent_name,pubid,sysid,ndata):
        ent=ExternalEntity(ent_name,pubid,sysid,ndata)
	self.gen_ents[ent.name]=ent
        self.dtd_listener.new_external_entity(ent_name,pubid,sysid,ndata)

    def new_external_pe(self,name,pubid,sysid):
        ent=ExternalEntity(name,pubid,sysid,"")
	self.param_ents[ent.name]=ent
        self.dtd_listener.new_external_pe(name,pubid,sysid)
	
    def dtd_end(self):
        self.dtd_listener.dtd_end()
    
    def new_comment(self,contents):
        self.dtd_listener.new_comment(contents)

    def new_pi(self,target,rem):
        self.dtd_listener.new_pi(target,rem)
    
    def new_notation(self,name,pubid,sysid):
        self.dtd_listener.new_notation(name,pubid,sysid)

    def new_element_type(self,elem_name,elem_cont):
        self.dtd_listener.new_element_type(elem_name,elem_cont)
    
# ==============================
# DTD consumer for the validating parser
# ==============================
    
class CompleteDTD(WFCDTD):
    "Complete DTD handler for the validating parser."

    def __init__(self,parser):
	WFCDTD.__init__(self,parser)

    def reset(self):
        "Clears all DTD information."
        WFCDTD.reset(self)
	self.notations={}
	self.attlists={}  # Attribute lists of elements not yet declared
        self.root_elem=None
        
    def get_root_elem(self):
	"Returns the name of the declared root element."
	return self.root_elem

    def get_notation(self,name):
	"""Returns the declaration of the notation. Throws KeyError if the
        notation does not exist."""
        return self.notations[name]

    # --- DTD parse events

    def dtd_end(self):
	for elem in self.attlists.keys():
	    self.parser.report_error(1006,elem)

	self.attlists={}  # Not needed any more, can free this memory
        self.dtd_listener.dtd_end()
	
    def new_notation(self,name,pubid,sysid):
	self.notations[name]=(pubid,sysid)
        self.dtd_listener.new_notation(name,pubid,sysid)

    def new_element_type(self,elem_name,elem_cont):       
	if self.elems.has_key(elem_name):
	    self.parser.report_error(2012,elem_name)

	if elem_cont==None:
	    model=make_empty_model()
	elif elem_cont!=1:
            model=make_model(elem_cont,self.parser)

	if elem_cont==1:
	    self.elems[elem_name]=ElementTypeAny(elem_name)
	else:
	    self.elems[elem_name]=ElementType(elem_name,model)

	if self.attlists.has_key(elem_name):
	    for (attr,a_type,a_decl,a_def) in self.attlists[elem_name]:
		self.elems[elem_name].add_attr(attr,a_type,a_decl,a_def,\
					       self.parser)
	    del self.attlists[elem_name]
            
        self.dtd_listener.new_element_type(elem_name,elem_cont)
	        
    def new_attribute(self,elem,attr,a_type,a_decl,a_def):
	"Receives the declaration of a new attribute."
        self.dtd_listener.new_attribute(elem,attr,a_type,a_decl,a_def)
	try:
	    self.elems[elem].add_attr(attr,a_type,a_decl,a_def,self.parser)
	except KeyError,e:
	    try:
		self.attlists[elem].append((attr,a_type,a_decl,a_def))
	    except KeyError,e:
		self.attlists[elem]=[(attr,a_type,a_decl,a_def)]
                
# ==============================
# Represents an XML element type
# ==============================
    
class ElementType:
    "Represents an element type."

    def __init__(self,name,cont):
	self.name=name
	self.attrhash={}
	self.content_model=cont

    def get_name(self):
	"Returns the name of the element type."
	return self.name
	
    def get_attr_list(self):
	"Returns a list of the declared attribute names."
	return self.attrhash.keys()
	
    def get_attr(self,name):
	"Returns the attribute or throws a KeyError if it's not declared."
	return self.attrhash[name]
	
    def add_attr(self,attr,a_type,a_decl,a_def,parser):
	"Adds a new attribute to the element."
	if self.attrhash.has_key(attr):
	    parser.report_error(1007,attr)
	
	if a_type=="ID":
	    for attr_name in self.attrhash.keys():
		if self.attrhash[attr_name].type=="ID":
		    parser.report_error(2013)

	    if a_decl!="#REQUIRED" and a_decl!="#IMPLIED":
		parser.report_error(2014)
	
	self.attrhash[attr]=Attribute(attr,a_type,a_decl,a_def)
	
    def get_start_state(self):
	"Return the start state of this content model."
	return self.content_model["start"]
	
    def final_state(self,state):
	"True if 'state' is a final state."
	return self.content_model["final"] & state
	
    def next_state(self,state,elem_name):
	"""Returns the next state of the content model from the given one
        when elem_name is encountered. Character data is represented as
        '#PCDATA'. If 0 is returned the element is not allowed here."""
	
	for (to,trans_name) in self.content_model[state]:
	    if trans_name==elem_name:
		return to

	return 0

    # --- Methods used to create shortcut validation information

    def get_default_attributes(self):
        defs={}
        for attr in self.attrhash.values():
            if attr.get_default()!=None:
                defs[attr.get_name()]=attr.get_default()

        return defs

    def get_fixed_attributes(self):
        fixed={}
        for attr in self.attrhash.values():
            if attr.get_decl()=="#FIXED":
                fixed[attr.get_name()]=attr.get_default()

        return fixed        

# --- Element types with ANY content

class ElementTypeAny(ElementType):

    def __init__(self,name):
	ElementType.__init__(self,name,None)

    def get_start_state(self):
	return 1

    def final_state(self,state):
	return 1

    def next_state(self,state,elem_name):
	return 1
    
# ==============================
# Attribute
# ==============================

class Attribute:
    "Represents a declared attribute."

    def __init__(self,name,attrtype,decl,default):
	self.name=name
	self.type=attrtype
	self.decl=decl
	self.default=default

        # Handling code for special attribute xml:space
        
        if name=="xml:space":
            if type(self.type)==types.StringType:
                parser.report_error(2015)
                return

            if len(self.type)!=2:
                error=1
            else:
                if (self.type[0]=="default" and self.type[1]=="preserve") or \
                   (self.type[1]=="default" and self.type[0]=="preserve"):
                    error=0
                else:
                    error=1

            if error: parser.report_error(2016)                            
                
    def validate(self,value,parser):
	"Validates given value for correctness."

	if type(self.type)!=types.StringType:
	    for val in self.type:
		if val==value: return
	    parser.report_error(2017,(value,self.name))
	elif self.type=="CDATA":
	    return
	elif self.type=="ID" or self.type=="IDREF" or self.type=="ENTITIY":
	    if not matches(reg_name,value):
		parser.report_error(2018,self.name)
	elif self.type=="NMTOKEN":
	    if not matches(reg_nmtoken,value):
		parser.report_error(2019,self.name)
	elif self.type=="NMTOKENS":
	    if not matches(reg_nmtokens,value):
		parser.report_error(2020,self.name)
        elif self.type=="IDREFS" or self.type=="ENTITIES":
            for token in string.split(value):
                if not matches(reg_name,token):
                    parser.report_error(2021,(token,self.name))

    def get_name(self):
        "Returns the attribute name."
        return self.name
        
    def get_type(self):
        "Returns the type of the attribute. (ID, CDATA etc)"
        return self.type

    def get_decl(self):
        "Returns the declaration (#IMPLIED, #REQUIRED, #FIXED or #DEFAULT)."
        return self.decl

    def get_default(self):
        """Returns the default value of the attribute, or None if none has
        been declared."""
        return self.default    
                
# ==============================
# Entities
# ==============================

class InternalEntity:

    def __init__(self,name,value):
	self.name=name
	self.value=value

    def is_internal(self):
	return 1

class ExternalEntity:

    def __init__(self,name,pubid,sysid,notation):
	self.name=name
	self.pubid=pubid
	self.sysid=sysid
	self.notation=notation

    def is_parsed(self):
        "True if this is a parsed entity."
	return self.notation==""
	
    def is_internal(self):
	return 0

    def get_pubid(self):
        "Returns the public identifier of the entity."
        return self.pubid

    def get_sysid(self):
        "Returns the system identifier of the entity."
        return self.sysid

# ==============================
# Namespaces
# ==============================

class Namespace:

    def __init__(self,prefix,nsname,srcdef):
        self.__prefix=prefix
        self.__nsname=nsname
        self.__srcdef=srcdef

    def get_prefix(self):
        return self.__prefix

    def get_name(self):
        return self.__nsname

    def get_schema_URL(self):
        return self.__srcdef

# ==============================
# Internal classes
# ==============================

# Non-deterministic state model builder

class FNDABuilder:
    "Builds a finite non-deterministic automaton."

    def __init__(self):
        self.__current=0
        self.__transitions=[[]]
        self.__mem=[]

    def remember_state(self):
        "Makes the builder remember the current state."
        self.__mem.append(self.__current)

    def set_current_to_remembered(self):
        """Makes the current state the last remembered one. The last remembered
        one is not forgotten."""
        self.__current=self.__mem[-1]
        
    def forget_state(self):
        "Makes the builder forget the current remembered state."
        del self.__mem[-1]

    def new_state(self):
        "Creates a new last state and makes it the current one."
        self.__transitions.append([])
        self.__current=len(self.__transitions)-1

    def get_automaton(self):
        "Returns the automaton produced by the builder."
        return self.__transitions

    def get_current_state(self):
        "Returns the current state."
        return self.__current

    def new_transition(self,label,frm,to):
        "Creates a new transition from frm to to, over label."
        self.__transitions[frm].append((to,label))

    def new_transition_to_new(self,label):
        """Creates a new transition from the current state to a new state,
        which becomes the new current state."""
        self.remember_state()
        self.new_state()
        self.__transitions[self.__mem[-1]].append((self.__current,label))
        self.forget_state()

    def new_transition_cur2rem(self,label):
        """Adds a new transition from the current state to the last remembered
        state."""
        self.__transitions[self.__current].append((self.__mem[-1],label))

    def new_transition_rem2cur(self,label):
        """Creates a new transition from the current state to the last
        remembered one."""
        self.__transitions[self.__mem[-1]].append((self.__current,label))

    def new_transition_2cur(self,frm,label):
        "Creates a new transition from frm to current state, with label."
        self.__transitions[frm].append((self.__current,label))
        
# Content model class

class ContentModel:
    "Represents a singleton content model. (Internal.)"

    def __init__(self,contents,modifier):
	self.contents=contents
	self.modifier=modifier
        
    def add_states(self,builder):
        "Builds the part of the automaton corresponding to this model part."
        if self.modifier=="?":
            builder.remember_state()
            self.add_contents(builder)
            builder.new_transition_rem2cur("")
            builder.forget_state()
        elif self.modifier=="+":
            self.add_contents(builder)
            builder.remember_state()
            self.add_contents(builder,1)
            builder.set_current_to_remembered()
            builder.forget_state()
        elif self.modifier=="*":
            builder.remember_state()
            builder.new_transition_to_new("")
            self.add_contents(builder,1)
            builder.new_transition_rem2cur("")
            builder.forget_state()
        else:
            self.add_contents(builder)

    def add_contents(self,builder,loop=0):
        """Adds the states and transitions belonging to the self.contents
        parts. If loop is true the states will loop back to the first state."""
        if type(self.contents[0])==types.InstanceType:
            if loop:
                builder.remember_state()
                self.contents[0].add_states(builder)
                builder.new_transition_cur2rem("")
                builder.set_current_to_remembered()
                builder.forget_state()
            else:
                self.contents[0].add_states(builder)
        else:
            if loop:
                builder.new_transition(self.contents[0],
                                       builder.get_current_state(),
                                       builder.get_current_state())
            else:
                builder.new_transition_to_new(self.contents[0])
            
# Sequential content model
    
class SeqContentModel(ContentModel):
    "Represents a sequential content model. (Internal.)"

    def add_contents(self,builder,loop=0):
        if loop:
            builder.remember_state()
        
        for cp in self.contents:
            cp.add_states(builder)

        if loop:
            builder.new_transition_cur2rem("")
            builder.forget_state()
    
# Choice content model

class ChoiceContentModel(ContentModel):
    "Represents a choice content model. (Internal.)"

    def add_contents(self,builder,loop=0):
        builder.remember_state()
        end_states=[] # The states at the end of each alternative
        
        for cp in self.contents:
            builder.new_state()
            builder.new_transition_rem2cur("")
            cp.add_states(builder)
            end_states.append(builder.get_current_state())

        builder.new_state()
        for state in end_states:
            builder.new_transition_2cur(state,"")

        if loop:
            builder.new_transition_cur2rem("")

        builder.forget_state()
    
# ==============================
# Conversion of FDAs
# ==============================

def hash(included):
    "Creates a hash number from the included array."
    no=0
    exp=1L
    for state in included:
	if state:
	    no=no+exp
	exp=exp*2L

    return no

def fnda2fda(transitions,final_state,parser):
    """Converts a finite-state non-deterministic automaton into a deterministic
    one."""

    # transitions: old FNDA as [[(to,over),(to,over),...],
    #                           [(to,over),(to,over),...]] structure
    # err: error-handler

    #print_trans(transitions)
    transitions.append([])
    new_states={}

    # Compute the e-closure of the start state
    closure_hash={}
    start_state=[0]*len(transitions)
    compute_closure(0,start_state,transitions)
    state_key=hash(start_state)
    closure_hash[0]=state_key

    # Add transitions and the other states
    add_transitions(0,transitions,new_states,start_state,state_key,parser,
                    closure_hash)
    
    states=new_states.keys()
    states.sort()

    #print_states(new_states,2)
    
    for state in states:
	if state % 2==1:
	    new_states["start"]=state
	    break

    new_states["final"]=pow(2L,final_state)
    return new_states
    
def add_transitions(ix,transitions,new_states,cur_state_list,state_key,parser,
                    closure_hash):
    "Set up transitions and create new states."

    new_states[state_key]=[] # OK, a new one, create it
    new_trans={} # Hash from label to a list of the possible destination states

    # Find all transitions from this set of states and group them by their
    # labels in the new_trans hash
    
    no=0
    for old_state in cur_state_list:
	if old_state:
	    for (to,what) in transitions[no]:
		if what!="":
                    if new_trans.has_key(what):
                        new_trans[what].append(to)
                    else:
                        new_trans[what]=[to]

	no=no+1

    # Go through the list of transitions, creating new transitions and
    # destination states in the model
        
    for (over,destlist) in new_trans.items():
        # creating new state                    

        # Reports ambiguity, but rather crudely. Will improve this later.
#         if len(destlist)>1:
#             parser.report_error(1008)

        if len(destlist)==1 and closure_hash.has_key(destlist[0]):
            # The closure of this state has been computed before, don't repeat
            new_state=closure_hash[destlist[0]]
        else:
            new_inc=[0]*len(transitions)
            for to in destlist:
                compute_closure(to,new_inc,transitions)

            new_state=hash(new_inc)
            if len(destlist)==1:
                closure_hash[destlist[0]]=new_state

        # add transition and destination state
        new_states[state_key].append(new_state,over)
        if not new_states.has_key(new_state):
            add_transitions(to,transitions,new_states,new_inc,\
                            new_state,parser,closure_hash)
        
def compute_closure(ix,included,transitions):
    "Computes the e-closure of this state."
    included[ix]=1
    for (to,what) in transitions[ix]:
	if what=="" and not included[to]:
            compute_closure(to,included,transitions)
        
def print_trans(model):
    ix=0
    for transitions in model:        
        print "STATE: %d" % ix
        for step in transitions:
            print "  TO %d OVER %s" % step
        ix=ix+1
        raw_input()
        
def print_states(states,stop=0):
    assert not (states.has_key("start") or states.has_key("final"))
    
    for trans_key in states.keys():
	trans=states[trans_key]
	print "State: "+`trans_key`
	for (to,what) in trans:
	    try:
		print "  To: "+`to`+" over: "+what
	    except TypeError,e:
		print "ERROR: "+`what`

        if stop>1:
            raw_input()

    if stop:
        raw_input()

def make_empty_model():
    "Constructs a state model for empty content models."
    return { 1:[], "final":1, "start":1 }

def make_model(content_model,err):
    "Creates an FDA from the content model."
    builder=FNDABuilder()
    content_model.add_states(builder)
    return fnda2fda(builder.get_automaton(),builder.get_current_state(),err)
