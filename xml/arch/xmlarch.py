# ============================================================================
# xmlarch.py - an XML architectures processor.
#
# Copyright (C) 1998 by Geir O. Grønmo, grove@infotek.no
# Free for commercial and non-commercial use.
#
# Version 0.11 (September 15th 1998)
# ============================================================================

from xml.sax import saxlib, saxutils

import string, sys

# ============================================================================
# DocumentHandler for processing XML architectures
# ============================================================================

class ArchDocHandler(saxlib.DocumentHandler):

    "DocumentHandler for processing XML architectures."

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, default_handler = None):

	self.architectures = {}
	self.default_handler = default_handler
	
	self.debug = 0
	self.debug_file = sys.stderr
	
    # ----------------------------------------------------------------------------
    # Set Debug flag

    def set_debug(self, debug, debug_file = sys.stderr):
	self.debug = debug
	self.debug_file = debug_file
	
    # ----------------------------------------------------------------------------
    # Set a default document handler that receives the same events as this class

    def setDefaultDocumentHandler(self, handler):
	self.default_handler = handler

    # ----------------------------------------------------------------------------
    # Administer the architecture document handlers
	
    def addArchDocumentHandler(self, arch_name, handler):
	
	# Create new broadcaster if none has already been created
	if not self.architectures.has_key(arch_name):
	    arch = Architecture()
	    arch.set_name(arch_name)
	    self.architectures[arch_name] = arch

	# Reqister document handler with broadcaster
	self.architectures[arch_name].broadcaster.list.append(handler)
	
    def removeArchDocumentHandler(self, arch_name, handler):
	# Not implemented yet
	pass

    def clearArchDocumentHandlers(self):
	# Not implemented yet
	pass

    # ----------------------------------------------------------------------------
    # Events
	    
    def startDocument(self):
	"Handle an event for the beginning of a document."

	# Send event to default handler
	if self.default_handler: self.default_handler.startDocument
	
	# Loop over architectures
	for arch in self.architectures.values():
	    arch.broadcaster.startDocument()

    def endDocument(self):
	"Handle an event for the end of a document."

	# Send event to default handler
	if self.default_handler: self.default_handler.endDocument()

	# Loop over architectures
	for arch in self.architectures.values():
	    arch.broadcaster.startDocument()

    def startElement(self, name, attrs):

	if self.debug: self.debug_file.write("<" + str(name) + " " + str(attrs.keys()) + " >\n")
	
	# Send event to default handler
	if self.default_handler: self.default_handler.startElement(name, attrs)

	# Loop over architectures
	for arch in self.architectures.values():

	    new_attrs = {}

	    # Set new parsestate
	    arch.parse_state = ArchParseState(arch.parse_state)

	    # Is this the document element?
	    if arch.parse_state.get_parent() == None:

		# Is this architecture declared?
		if not arch.is_declared():
		    raise ArchException("Architecture " + str(arch.get_name()) + " not declared.")

		# Scan attributes
		new_attrs = self.scan_arch_attrs(arch, attrs)

		# If not document element form is declared set it to the architecture name
		if not arch.parse_state.get_elem_form():
		    arch.parse_state.set_elem_form(arch.get_doc_elem_form())

		# Check whether document element form is equal to the one this was declared
		if arch.parse_state.get_elem_form() != arch.get_doc_elem_form():
		    raise ArchException("Document element form should be %s -- not %s." % (arch.get_doc_elem_form(), arch.parse_state.get_elem_form()))

	    # Should the element be suppressed?
	    else:

		# Element should be suppressed
		if arch.parse_state.get_suppression() == arch.parse_state.sArcAll:
		    arch.parse_state.set_elem_form(None)
		else:
	    	    
		    # Scan attributes
		    new_attrs = self.scan_arch_attrs(arch, attrs)
		    
		    # Element should be suppressed
		    if arch.parse_state.get_suppression() == arch.parse_state.sArcForm:
			arch.parse_state.set_elem_form(None)
			
		    elif not arch.parse_state.get_elem_form():
		
			# Automatic element form mapping
			if arch.get_auto():
			    arch.parse_state.set_elem_form(name)
		    
			# Brigde element form
			# Help! What should happen when a bridging element isn't specified?
			elif arch.parse_state.get_seen_id() and arch.get_bridge_form():
			    arch.parse_state.set_elem_form(arch.get_bridge_form())

		# Need this to switch off automatic mapping. This is not conforming
		# to ISO 10744:1997
		if arch.parse_state.get_elem_form() == "#IMPLIED":
		    arch.parse_state.set_elem_form(None)


	    att_items = new_attrs.items()

	    # Trigger startElement event if element form exist
	    if arch.parse_state.get_elem_form():
		if self.debug:
		    # Print debug information
		    self.debug_file.write(" + " + str(arch.get_name()) + " -> " + str(arch.parse_state.get_elem_form()))
		    if self.debug >= 2: self.debug_file.write(att_items)
		    self.debug_file.write("\n")
		arch.broadcaster.startElement(arch.parse_state.get_elem_form(), new_attrs)

	    else:
		if self.debug:
		    # Print debug information
		    self.debug_file.write(" - " + str(arch.get_name()))
		    if self.debug >= 2: self.debug_file.write(att_items)
		    self.debug_file.write("\n")
		
    def endElement(self, name):

	# Send event to default handler
	if self.default_handler: self.default_handler.endElement(name)

	# Loop over architectures
	for arch in self.architectures.values():

	    # Trigger endElement event if element form exist
	    if arch.parse_state.get_elem_form():
		arch.broadcaster.endElement(arch.parse_state.get_elem_form())

	    # Set current parse state to the one of the parent element
	    arch.parse_state = arch.parse_state.get_parent()

    def characters(self, ch, start, length):
	"Handle a character data event."

	# Send event to default handler
	if self.default_handler: self.default_handler.characters(ch, start, length)

	# Loop over architectures
	for arch in self.architectures.values():

	    # Outside the document element
	    if arch.parse_state == None:
		# Help! Should this data be suppressed?
		if self.debug >= 2: self.debug_file.write("[or:" + ch[start:start+length] + "]")
		continue
	
	    # If suppression is sArcAll - all data is ignored
	    if arch.parse_state.get_suppression() == arch.parse_state.sArcAll:
		if self.debug >= 2: self.debug_file.write("[sa:" + ch[start:start+length] + "]")
		continue
	    
	    # If ignore data is ArcIgnD - data is always ignored
	    if arch.parse_state.get_ignore_data() == arch.parse_state.ArcIgnD:
		if self.debug >= 2: self.debug_file.write("[ia:" + ch[start:start+length] + "]")
		continue

	    # If ignore data is cArcIgnD - data is only ignored when element form doesn't exist
	    elif arch.parse_state.get_ignore_data() == arch.parse_state.cArcIgnD:
		if arch.parse_state.get_elem_form():
		    arch.broadcaster.characters(ch, start, length)
		else:
		    if self.debug >= 2: self.debug_file.write("[ic:" + ch[start:start+length] + "]")
		    continue

	    # If ignore data is nArcIgnD - data is not ignored
	    elif arch.parse_state.get_ignore_data() == arch.parse_state.nArcIgnD:
		arch.broadcaster.characters(ch, start, length)

    def ignorableWhitespace(self, ch, start, length):
	"Handle an event for ignorable whitespace in element content."

	# Send event to default handler
	if self.default_handler: self.default_handler.ignorableWhitespace(ch, start, length)

	# Ignorable data can be processed as normal characters
	self.characters(ch, start, length)

    def processingInstruction(self, target, data):

	# Send event to default handler
	if self.default_handler:
	    self.default_handler.processingInstruction(target, data)

	# If target is IS10744, remove "arch" part from pi data
	if target == "IS10744" and data[:4] == "arch" and data[4:5] in (' ', "\t", "\n"):
		data = data[4:]

	# Recognize architecture use declaration (could be several)
	if target == "IS10744:arch" or target == "IS10744":

	    # Read attributes
	    attrs = AttributeParser(data).parse()

	    # Load architecture
	    new_arch = Architecture(attrs)
	    if self.debug: self.debug_file.write("Found use declaration for " + str(new_arch.get_name()) + " " + str(attrs) + "\n")
	    
	    # Register architecture
	    if not self.architectures.has_key(new_arch.get_name()):
		self.architectures[new_arch.get_name()] = Architecture(attrs)
	    else:
		self.architectures[new_arch.get_name()].load(attrs)

	    # Loop over architectures
	    for arch in self.architectures.values():

		# Don't output architecture use declaraction pi for this architecture
		if arch.get_name() == new_arch.get_name():
		    continue

		arch.broadcaster.processingInstruction(target, data)

	else:
	    # Loop over architectures
	    for arch in self.architectures.values():

		# Help! Should some, none or all of the IS10744:arch PIs be passed on?
		# One problem with these PIs is that the procesingInstruction events
		# can't be broadcasted to architectures that hasn't yet been recognized.
		arch.broadcaster.processingInstruction(target, data)

    # ----------------------------------------------------------------------------
    # Document Locator

    def setDocumentLocator(self, locator):
	"Receive an object for locating the origin of SAX document events."

	# Help what should I do with this one?
	pass
	
    # ----------------------------------------------------------------------------
    # Utility methods

    def scan_arch_attrs(self, arch, org_attrs):

	# Make a copy of the attributes
	new_attrs = {}
	for h in org_attrs.map.keys():
	    new_attrs[h] = org_attrs[h]

	# Get the architectures form attribute
	if arch.get_form_att():
	    arch_form_att = arch.get_form_att()
	else:
	    arch_form_att = arch.get_name()
	    
	renamer = arch.get_renamer_att()
	suppressor = arch.get_suppressor_att()
	ignore_data = arch.get_ignore_data_att()
	
	# Rename attributes if neccessary
	if renamer and org_attrs.has_key(renamer):
	    values = string.split(org_attrs[renamer])

	    # Validate the renamer attribute value
	    if not len(values) % 2 == 0:
		raise ArchException("Renamer attribute " + renamer + " doesn't contain an even number of tokens")

	    # Loop over all token pairs
	    for num in range(0, len(values), 2):

	        # Rename attributes
		if org_attrs.has_key(values[num]):
		    
		    # Does not support these yet
		    if values[num+1] in ("#DEFAULT", "#MAPTOKEN", "#CONTENT"):
			# Help! Should this attribute be deleted?
			del new_attrs[values[num]]
			continue

		    # Rename attribute
		    new_attrs[values[num+1]] = new_attrs[values[num]]
		    del new_attrs[values[num]]
		    
	    
	# Check for architectual form attribute
	if org_attrs.has_key(arch_form_att):
	    arch.parse_state.set_elem_form(org_attrs[arch_form_att])
	    del new_attrs[arch_form_att]
	
	# Check for renamer attribute
	if org_attrs.has_key(renamer):
	    arch.parse_state.set_renamer(org_attrs[renamer])
	    del new_attrs[renamer]

	# Check for suppressor attribute
	if org_attrs.has_key(suppressor):
	    if org_attrs[suppressor] == "sArcAll":
		arch.parse_state.set_suppression(arch.parse_state.sArcAll)
	    elif org_attrs[suppressor] == "sArcForm":
		arch.parse_state.set_suppression(arch.parse_state.sArcForm)
	    elif org_attrs[suppressor] == "sArcNone":
		arch.parse_state.set_suppression(arch.parse_state.sArcNone)
	    else:
		raise ArchException("Bad value for suppressor attribute: " + org_attrs[suppressor])
	    del new_attrs[suppressor]

        # If no suppression attribute is specified - inherit suppression
        else:
	    if arch.parse_state.get_parent():
		arch.parse_state.set_suppression(arch.parse_state.get_parent().get_suppression())
				    
	# Check for ignore data attribute
	if org_attrs.has_key(ignore_data):
	    if org_attrs[ignore_data] == "ArcIgnD":
		arch.parse_state.set_ignore_data(arch.parse_state.ArcIgnD)
	    elif org_attrs[ignore_data] == "cArcIgnD":
		arch.parse_state.set_ignore_data(arch.parse_state.cArcIgnD)
	    elif org_attrs[ignore_data] == "nArcIgnD":
		arch.parse_state.set_ignore_data(arch.parse_state.nArcIgnD)
	    else:
		raise ArchException("Bad value for ignore data attribute: " + org_attrs[ignore_data])
	    
	    del new_attrs[ignore_data]

        # If no ignore data attribute is specified - inherit ignoration
        else:
	    if arch.parse_state.get_parent():
		arch.parse_state.set_ignore_data(arch.parse_state.get_parent().get_ignore_data())
		
	# Check if there is an attribute of type ID
	for att in org_attrs.keys():
	    
	    if org_attrs.getType(att) == "ID":
		arch.parse_state.set_seen_id(1)

	if self.debug >= 3: self.debug_file.write("{" + str(arch.parse_state.get_suppression()) + "," + str(arch.parse_state.get_ignore_data()) + "}")

	return saxutils.AttributeMap(new_attrs)

# ============================================================================
# XML architecture class
# ============================================================================

class Architecture:

    "Class representing an XML architecture."

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, attrs = None):
	
	self.reset()

	if attrs: self.load(attrs)
	
	self.parse_state = None
	self.broadcaster = saxutils.EventBroadcaster([])
	
    def setBroadcaster(self, broadcaster):
	self.broadcaster = broadcaster

    def getBroadcaster(self):
	return self.broadcaster
    
    def reset (self):

	self.declared = 0
    	self.name = None
	
	self.public_id = None
	self.dtd_public_id = None
	self.dtd_system_id = None
	self.form_att = None
	self.renamer_att = None
	self.suppressor_att = None
	self.ignore_data_att = None
	self.doc_elem_form = None
	self.bridge_form = None
	self.data_form = None
	self.auto = None

	self.declared = 0
	
    def load (self, attrs):
	
	# Load information
	if attrs.has_key("name"):
	    self.set_name(attrs["name"])
	    self.set_doc_elem_form(attrs["name"])
	    self.declared = 1
	else:
	    raise ArchException("Name of architecture isn't specified")
	
	if attrs.has_key("public-id"): self.set_public_id(attrs["public-id"])
	if attrs.has_key("dtd-public-id"): self.set_dtd_public_id(attrs["dtd-public-id"])
	if attrs.has_key("dtd-system-id"): self.set_dtd_system_id(attrs["dtd-system-id"])
	if attrs.has_key("form-att"): self.set_form_att(attrs["form-att"])
	if attrs.has_key("renamer-att"): self.set_renamer_att(attrs["renamer-att"])
	if attrs.has_key("suppressor-att"): self.set_suppressor_att(attrs["suppressor-att"])
	if attrs.has_key("ignore-data-att"): self.set_ignore_data_att(attrs["ignore-data-att"])
	if attrs.has_key("doc-elem-form"): self.set_doc_elem_form(attrs["doc-elem-form"])
	if attrs.has_key("bridge-form"): self.set_bridge_form(attrs["bridge-form"])
	if attrs.has_key("data-form"): self.set_data_form(attrs["data-form"])

	if attrs.has_key("auto"):
	    if attrs["auto"] == "ArcAuto":
		self.set_auto(1)
	    elif attrs["auto"] == "nArcAuto":
		 self.set_auto(0)
	    else:
		raise ArchException("Bad value auto: " + attrs["auto"])
 
	if attrs.has_key("options"):
	    pass # FIXME: do something with these.

    # ----------------------------------------------------------------------------
    # Setter and getter methods

    def set_name(self, name): self.name = name
    def get_name(self): return self.name

    def set_public_id(self, public_id): self.public_id = public_id
    def get_public_id(self): return self.public_id

    def set_dtd_public_id(self, dtd_public_id): self.dtd_public_id = dtd_public_id
    def get_dtd_public_id(self): return self.dtd_public_id

    def set_dtd_system_id(self, dtd_system_id): self.dtd_system_id = dtd_system_id
    def get_dtd_system_id(self): return self.dtd_system_id

    def set_form_att(self, form_att): self.form_att = form_att
    def get_form_att(self): return self.form_att

    def set_renamer_att(self, renamer_att): self.renamer_att = renamer_att
    def get_renamer_att(self): return self.renamer_att

    def set_suppressor_att(self, suppressor_att): self.suppressor_att = suppressor_att
    def get_suppressor_att(self): return self.suppressor_att

    def set_ignore_data_att(self, ignore_data_att): self.ignore_data_att = ignore_data_att
    def get_ignore_data_att(self): return self.ignore_data_att

    def set_doc_elem_form(self, doc_elem_form): self.doc_elem_form = doc_elem_form
    def get_doc_elem_form(self): return self.doc_elem_form

    def set_bridge_form(self, bridge_form): self.bridge_form = bridge_form
    def get_bridge_form(self): return self.bridge_form

    def set_data_form(self, data_form): self.data_form = data_form
    def get_data_form(self): return self.data_form

    def set_auto(self, auto): self.auto = auto
    def get_auto(self): return self.auto

    def is_declared(self): return self.declared
    
# ============================================================================
# Parse state class
# ============================================================================

class ArchParseState:

    "Class representing parsing state with regard to XML architectures."

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, parent = None):

	# Suppression
	self.sArcAll = 1
	self.sArcForm = 2
	self.sArcNone = 3

	# Ignoration
	self.ArcIgnD = 1
	self.cArcIgnD = 2
	self.nArcIgnD = 3

	if parent:
	    self.suppression = parent.suppression
	    self.ignore_data = parent.ignore_data
	else:
	    self.suppression = self.sArcNone
	    self.ignore_data = self.cArcIgnD

	self.parent = parent # The parent parse state
	self.elem_form = None # Name of the architectual form
	self.renamer = None # Name of the renamer attribute
	
	self.seen_id = None

    # ----------------------------------------------------------------------------
    # Setter and getter methods

    # Suppression methods    

    def set_suppression(self, suppression):

	if not self.suppression == self.sArcAll:
	    self.suppression = suppression

    def get_suppression(self):
	return self.suppression
    
    # Data ignore methods
    
    def set_ignore_data(self, ignore_data):
	self.ignore_data = ignore_data

    def get_ignore_data(self):
	return self.ignore_data
    
    # Parent methods
    
    def set_parent(self, parent):
	self.parent = parent

    def get_parent(self):
	return self.parent
    
    # Form methods
    
    def set_elem_form(self, elem_form):
	self.elem_form = elem_form

    def get_elem_form(self):
	return self.elem_form
    
    # Renamer methods
    
    def set_renamer(self, renamer):
	self.renamer = renamer

    def get_renamer(self):
	return self.renamer

    def set_seen_id(self, seen_id): self.seen_id = seen_id
    def get_seen_id(self): return self.seen_id

# ============================================================================
# XML architecture exception
# ============================================================================

class ArchException(saxlib.SAXException):

    "Architecture Exception"

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, msg, exception = None):
        """Creates an exception. The message is required, but the exception
        can be None."""
        self.msg=msg
        self.exception=exception

    def getMessage(self):
	"Return a message for this exception."
	return self.msg

    def getException(self):
        "Return the embedded exception, if any."
        return self.exception

    def __str__(self):
        "Create a string representation of the exception."
        return self.msg

# ============================================================================
# Attribute parsing class
# ============================================================================

class AttributeParser:

    "Class used for parsing attributes of processing instructions and elements."

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, data):

	self.data = data
	self.pos = 0

    # ----------------------------------------------------------------------------
    # Parse data and return an attribute dict

    def parse(self):

	self.attrs = {}
	name = None
	value = None

	self.pos = 0
	self.skip_whitespace();

	# Read attributes
	while (self.pos < len(self.data)):
	    # Read the attribute name
	    name = self.read_name()
	    # Skip whitespace
	    self.skip_equal()
	    # Read attribute value
	    value = self.read_value()
	    self.attrs[name] = value
	    # Skip whitespace
	    self.skip_whitespace()

	return self.attrs
    
    # ----------------------------------------------------------------------------
    # Skip whitespace
    
    def skip_whitespace(self):
	while (self.pos < len(self.data)):
	    if self.data[self.pos] in (' ', "\t", "\n"):
		self.pos = self.pos + 1
		continue
	    else:
		break
	    
    # ----------------------------------------------------------------------------
    # Skip equal sign

    def skip_equal(self):
	    
	self.skip_whitespace()
	if (self.pos >= len(self.data) or self.data[self.pos] != '='):
	    raise ArchException("Expected '='.")
	
	self.pos = self.pos + 1
	self.skip_whitespace()
	
    # ----------------------------------------------------------------------------
    # Read name
	    
    def read_name(self):

	buf = ""

	while (self.pos < len(self.data)):
	    if self.data[self.pos] in (' ', "\t", "\n", "="):
		if len(buf) == 0:
		    raise ArchException("Name expected.")
		else:
		    return buf
	    else:
		buf = buf + self.data[self.pos]
		self.pos = self.pos + 1

	if len(buf) == 0:
	    raise ArchException("Name expected.")
	else:
	    return buf

    # ----------------------------------------------------------------------------
    # Read literal

    def read_value(self):

	buf = ""
	lit = ""

	if (self.pos < len(self.data)):
	    lit = self.data[self.pos]
	    self.pos = self.pos + 1
	else:
	    raise ArchException("Assignment finished without literal value.")

	if (lit != '\'' and lit != '"'):
	    raise ArchException("Expected '\"' or \"'\".")

	while (self.data[self.pos] != lit):
	    buf =  buf + self.data[self.pos]

	    if self.pos > len(self.data):
		raise ArchException("Unterminated literal")
		
	    self.pos = self.pos + 1

	self.pos = self.pos + 1
	return buf

# ============================================================================
# SAX document handler that produces normalized XML output
# ============================================================================

class Normalizer(saxlib.HandlerBase):
    "A SAX document handler that produces normalized XML output."

    def __init__(self,writer=sys.stdout):
	self.writer=writer
	self.elem_level=0
	self.ignore_outside_docelem = 1
	
    def processingInstruction (self,target, remainder):
	self.writer.write("<?"+target+" "+remainder+"?>")
	if self.elem_level == 0: self.writer.write("\n")
	
    def startElement(self,name,amap):
	self.writer.write("<"+name)
	
	a_names=amap.keys()
	a_names.sort()

	for a_name in a_names:
	    self.writer.write(" "+a_name+"=\"")
	    self.writer.write(amap[a_name])
	    self.writer.write("\"")
	self.writer.write(">")
	self.elem_level=self.elem_level+1

    def endElement(self,name):
	self.writer.write("</"+name+">")
	self.elem_level=self.elem_level-1

    def ignorableWhitespace(self,data,start_ix,length):
	if self.elem_level>0 or self.ignore_outside_docelem:
            self.writer.write(data[start_ix:start_ix+length])
	
    def characters(self,data,start_ix,length):
	if self.elem_level>0 or self.ignore_outside_docelem:
            self.writer.write(data[start_ix:start_ix+length])
	
    def endDocument(self):
        try:
	    self.writer.write("\n")
            self.writer.close()
        except NameError:
            pass # It's OK, if the method isn't there we probably don't need it

