# ============================================================================
# xmlarch - an XML architecture processor.
# ============================================================================

"""xmlarch - and XML architecture processor

Version 0.25 (March 22nd 1999)

Copyright (C) 1998 by Geir O. Grønmo, grove@infotek.no

It is free for non-commercial use, if you modify it please let me know.

The xmlarch module contains an XML architectural forms processor written in
Python. It allows you to process XML architectural forms using any parser
that uses the SAX interfaces. The module allow you to process several
architectures in one parse pass.

Architectural document events for an architecture can even be broadcasted
to multiple DocumentHandlers.
"""

__author__ = "Geir Ove Grønmo, grove@infotek.no"
__version__ = "0.25"

# TODO (some is possibly already fixed):
#
# - make sure validation of the renamer attributes always is correct
# - save "deleted" attributes from the new attribute map
# - make access to the original event possible
# - make a test suite and compare output against other architectural engines
# - make sure that it works with JPython
# - support option in archictecture use declaration
# - support the use of ArcBase pi's
# - read meta-dtds
# - add other recognition hooks to add_document_handler not only be
#   arch. name (e.g. by public dd or system id)
# + add support for the new #GI keyword [fixed 990224]

# QUESTIONS:
#
# - should an architecture processor normalize case on architectural forms?
# - should #GIs be mapped both ways?

# ============================================================================
# Imported modules
# ============================================================================

from xml.sax import saxlib, saxutils

import string, sys

# ============================================================================
# DocumentHandler for processing XML architectures
# ============================================================================

class ArchDocHandler(saxlib.DocumentHandler):

    """SAX DocumentHandler for processing XML architectures.

    This class is responsible for doing architectural processing of all SAX
    events that it receives.

    The ArchDocHandler instance must be registered with a parser that triggers
    SAX events during parsing. This is usually done by calling the parsers
    *setDocumentHandler* method.

    DocumentHandlers that is interested in listening to architectural events must
    register itself using the *add_document_handler* method of the ArchDocHandler
    instance. They may remove themselves by calling *remove_document_handler*.

    All registered DocumentHandlers can be removed by calling *clear_document_handlers*.
    """

    def __init__(self, default_doc_handler = None):

        """Initialize a new instance."""

        self.architectures = {}
        self.default_doc_handler = default_doc_handler
        
        self.debug_level = 0
        self.debug_file = sys.stderr

        # Reserved renamer tokens
        self.renamer_keywords = ("#DEFAULT", "#CONTENT", "#ARCCONT", "#MAPTOKEN", "#GI")

        self.context = []

    # ----------------------------------------------------------------------------
    # Set methods

    def set_debug_level(self, debug_level, debug_file = sys.stderr):
        
        """Set the debug level and the debug file.

        Debug information is by default written to sys.stderr when debugging is active.
        This can be changed by specifying the *debug_file* parameter with a file
        object. The default debug level is 0, i.e no debugging information is written.
        """
        
        self.debug_level = debug_level
        self.debug_file = debug_file

    def set_default_document_handler(self, handler):

        """Set a default document handler that receives the same events as this class.

        A default DocumentHandler is only used if you want the incoming events passed
        on to another DocumentHandler."""
        
        self.default_doc_handler = handler

    # ----------------------------------------------------------------------------
    # Administer the architecture document handlers
        
    def add_document_handler(self, arch_name, doc_handler):

        """Add an architecture document handler.
        
        This method adds the DocumentHandler to the architecture's list of architectural
        event listeners."""
        
        # Create new broadcaster if none has already been created
        if not self.architectures.has_key(arch_name):
            arch = Architecture()
            arch.set_name(arch_name)
            self.architectures[arch_name] = arch

        # Reqister document handler with broadcaster
        self.architectures[arch_name].broadcaster.list.append(doc_handler)
        
    def remove_document_handler(self, arch_name, doc_handler):
        
        """Remove an architecture document handler.

        This method removes all occurences of the DocumentHandler in the architecture's
        list of architectural event listeners."""

        while 1:
            try:
                i = self.architectures[arch_name].broadcaster.list.index(doc_handler)
                del self.architectures[arch_name].broadcaster.list[i]
            except:
                break

    def clear_document_handlers(self):

        """Remove all registered architecture document handlers.

        This method removes all DocumentHandlers in the architecture's list of
        architectural event listeners."""
        
        self.architectures[arch_name].broadcaster.list = []

    def get_architecture(self, arch_name):

        """Get the Architecture object for a given architecture.


        The Architecture object will allow you to get information about the architecture
        and information about its parse state."""
        
        return self.architectures[arch_name]

    def get_current_element_name(self):

        if len(self.context) > 0:
            return self.context[-1]
        
    # ----------------------------------------------------------------------------
    # SAX events
            
    def startDocument(self):
        
        """Handle an event for the beginning of a document."""

        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.startDocument()
        
        # Loop over architectures
        for arch in self.architectures.values():
            arch.broadcaster.startDocument()

    def endDocument(self):
        
        """Handle an event for the end of a document."""

        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.endDocument()

        # Loop over architectures
        for arch in self.architectures.values():
            arch.broadcaster.endDocument()

    def startElement(self, name, attrs):

        """Handle an event for the beginning of an element."""

        # Store parse context [elements]
        self.context.append(name)
        
        # Write debug information
        if self.debug_level: self.debug_file.write("<" + str(name) + " " + str(attrs.keys()) + " >\n")
        
        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.startElement(name, attrs)

        # Loop over architectures
        for arch in self.architectures.values():

            # Set new parsestate
            arch.parse_state = ArchParseState(arch.parse_state)

            # Is this the document element?
            if arch.parse_state.get_parent() == None:

                # Is this architecture declared?
                if not arch.is_declared():
                    raise ArchException("Architecture " + str(arch.get_name()) + " not declared.")

                # Scan attributes
                arch.parse_state.set_attributes(self.scan_arch_attrs(arch, attrs))

                # If not document element form is declared set it to the architecture name
                if not arch.parse_state.get_elem_form():
                    arch.parse_state.set_elem_form(arch.get_doc_elem_form())

                # Check whether document element form is equal to the one this was declared
                if arch.parse_state.get_elem_form() != arch.get_doc_elem_form():
                    raise ArchException("Document element form should be %s -- not %s." % (arch.get_doc_elem_form(), arch.parse_state.get_elem_form()))

            # Should the element be suppressed?
            else:

                # Element should be suppressed
                if arch.parse_state.get_parent_suppression() == arch.parse_state.sArcAll:
                    arch.parse_state.set_elem_form(None)
                else:
                    
                    # Scan attributes
                    arch.parse_state.set_attributes(self.scan_arch_attrs(arch, attrs))
                    
                    # Element should be suppressed
                    if arch.parse_state.get_parent_suppression() == arch.parse_state.sArcForm:
                        arch.parse_state.set_elem_form(None)
                        
                    elif not arch.parse_state.get_elem_form():
                
                        # Automatic element form mapping
                        if arch.get_auto() == "ArcAuto":
                            arch.parse_state.set_elem_form(name)
                    
                        # Brigde element form
                        # Help! What should happen when a bridging element isn't specified?
                        elif arch.parse_state.get_seen_id() and arch.get_bridge_form():
                            arch.parse_state.set_elem_form(arch.get_bridge_form())

                # Need this to switch off automatic mapping. This is not conforming
                # to ISO 10744:1997
                if arch.parse_state.get_elem_form() == "#IMPLIED":
                    arch.parse_state.set_elem_form(None)


            att_items = arch.parse_state.get_attributes().items()

            # Don't trigger any architectural events yet when #CONTENT is active.
            # I have to read the content first.
            if arch.parse_state.is_CONTENT_active(): return
            
            # Trigger startElement event if element form exist
            if arch.parse_state.get_elem_form():
                # Write debug information
                if self.debug_level:
                    self.debug_file.write(" + " + str(arch.get_name()) + " -> " + str(arch.parse_state.get_elem_form()))
                    if self.debug_level >= 2: self.debug_file.write(att_items)
                    self.debug_file.write("\n")
                arch.broadcaster.startElement(arch.parse_state.get_elem_form(), saxutils.AttributeMap(arch.parse_state.get_attributes()))

            else:
                # Write debug information
                if self.debug_level:
                    self.debug_file.write(" - " + str(arch.get_name()))
                    if self.debug_level >= 2: self.debug_file.write(att_items)
                    self.debug_file.write("\n")

    def endElement(self, name):

        """Handle an event for the end of an element."""

        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.endElement(name)

        # Loop over architectures
        for arch in self.architectures.values():

            parent_parse_state = arch.parse_state.get_parent()

            if parent_parse_state:
                # If CONTENT processing is active, add distribute content to parent
                if parent_parse_state.is_CONTENT_active():
                    parent_parse_state.add_CONTENT_value(arch.parse_state.get_CONTENT_value())

                elif not parent_parse_state.is_CONTENT_active() and arch.parse_state.is_CONTENT_active():

                    # Update attribute content of #CONTENT attributes
                    for attr in arch.parse_state.CONTENT_attributes.keys():
                        arch.parse_state.set_attribute_value(attr, arch.parse_state.get_CONTENT_value())

                    # Trigger startElement event
                    arch.broadcaster.startElement(arch.parse_state.get_elem_form(), arch.parse_state.get_attributes())
            # Output mapped #ARCCONT content
            if arch.parse_state.is_ARCCONT_active():
                ARCCONT_value = arch.parse_state.get_ARCCONT_value()

                # Trigger character event
                arch.broadcaster.characters(ARCCONT_value, 0, len(ARCCONT_value))
                            
            # Trigger endElement event if element form exist
            if arch.parse_state.get_elem_form():
                arch.broadcaster.endElement(arch.parse_state.get_elem_form())

            # Set current parse state to the one of the parent element
            arch.parse_state = parent_parse_state

        # Pop this element off the context list
        del self.context[-1]

    def characters(self, ch, start, length):

        """Handle a character data event."""

        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.characters(ch, start, length)

        # Loop over architectures
        for arch in self.architectures.values():

            # Outside the document element
            if arch.parse_state == None:
                # Help! Should this data be suppressed?
                # Write debug information
                if self.debug_level >= 2: self.debug_file.write("[or:" + ch[start:start+length] + "]")
                continue
        
            # If CONTENT processing is active, store content for later
            if arch.parse_state.is_CONTENT_active():
                arch.parse_state.add_CONTENT_value(ch[start:start+length])

            # If suppression is sArcAll - all data is ignored
            if arch.parse_state.get_parent_suppression() == arch.parse_state.sArcAll:
                # Write debug information
                if self.debug_level >= 2: self.debug_file.write("[sa:" + ch[start:start+length] + "]")
                continue
            
            # If ignore data is ArcIgnD - data is always ignored
            if arch.parse_state.get_ignore_data() == arch.parse_state.ArcIgnD:
                # Write debug information
                if self.debug_level >= 2: self.debug_file.write("[ia:" + ch[start:start+length] + "]")
                continue

            # If ignore data is cArcIgnD - data is only ignored when element form doesn't exist
            elif arch.parse_state.get_ignore_data() == arch.parse_state.cArcIgnD:
                
                if arch.parse_state.get_elem_form() and not arch.parse_state.is_ARCCONT_active() and not arch.parse_state.is_CONTENT_active():
                    arch.broadcaster.characters(ch, start, length)
                    
                else:
                    # Write debug information
                    if self.debug_level >= 2: self.debug_file.write("[ic:" + ch[start:start+length] + "]")
                    continue

            # If ignore data is nArcIgnD - data is not ignored
            elif arch.parse_state.get_ignore_data() == arch.parse_state.nArcIgnD:
                arch.broadcaster.characters(ch, start, length)

    def ignorableWhitespace(self, ch, start, length):

        """Handle an event for ignorable whitespace in element content."""

        # Send event to default handler
        if self.default_doc_handler: self.default_doc_handler.ignorableWhitespace(ch, start, length)

        # Ignorable data can be processed as normal characters
        self.characters(ch, start, length)

    def processingInstruction(self, target, data):

        """Handle a processing instruction event."""

        # Send event to default handler
        if self.default_doc_handler:
            self.default_doc_handler.processingInstruction(target, data)

        # If target is IS10744, remove "arch" part from pi data
        is_arch_pi = 0
        if target == "IS10744" and data[:4] == "arch" and data[4:5] in (' ', "\t", "\n"):
                data = data[4:]
                is_arch_pi = 1
        elif target == "IS10744:arch":
            is_arch_pi = 1
        
        # Recognize architecture use declaration (could be several)
        if is_arch_pi:

            # Read attributes
            attrs = AttributeParser(data).parse()

            # Load architecture
            new_arch = Architecture(attrs)

            # Write debug information
            if self.debug_level: self.debug_file.write("Found use declaration for " + str(new_arch.get_name()) + " " + str(attrs) + "\n")
            
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

                # FIXME: should I output the architectural use declaration PI?
                # arch.broadcaster.processingInstruction(target, data)

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

        """Receive an object for locating the origin of SAX document events."""

        # Help what should I do with this one?
        pass
        
    # ----------------------------------------------------------------------------
    # Utility methods

    def scan_arch_attrs(self, arch, org_attrs):

        """Scan an elements attributes for architectural information, and return a modified set of attributes.

        *arch* must be an object that implements the Architecture interface. *org_attrs* must
        be a hash containing attribute name/values."""

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

            # Split attribute value into tokens
            values = string.split(org_attrs[renamer])

            # Loop over all tokens and do renaming of attributes
            toknum = -1

            while 1:

                toknum = toknum + 1
                if toknum > len(values) - 1: break # No more tokens
                    
                # NAME
                
                #if org_attrs.has_key(values[toknum]): #FIXME mapped attribute must not necessarily exist
                if not values[toknum] in self.renamer_keywords:
                    # FIXME: should check whether name is truly an XML NAME.
                    name = values[toknum]

                    if new_attrs.has_key(name): # Attribute already exists
                        attval = new_attrs[name]
                    else: # Attribute doesn't exist
                        attval = ""
                        new_attrs[name] = attval
                    
                    toknum = toknum + 1
                    if toknum > len(values) - 1: break # No more tokens
                    
                    # NAME, (ATTORCON|"#DEFAULT"), ("#MAPTOKEN", NMTOKEN, NMTOKEN)*
                    # or                       
                    # "#ARCCONT", ATTNAME

                    maptoken_toknum = toknum
                    if not maptoken_toknum + 3 > len(values) - 1:

                        # #MAPTOKEN
                        while 1:
                            if not maptoken_toknum + 3 > len(values) - 1:
                                if not values[maptoken_toknum+1] == "#MAPTOKEN": break
                                nmtokens = []
                                
                                # Rename attribute value tokens
                                for nmt in string.split(attval):
                                    if nmt == values[maptoken_toknum+2]:
                                        nmtokens.append(values[maptoken_toknum+3]) # Renamed
                                    else:
                                        nmtokens.append(nmt) # Not renamed
                                
                                attval = string.join(nmtokens, " ")
                                maptoken_toknum = maptoken_toknum + 3
                                continue
                            else:
                                break
                            
                    # #DEFAULT
                    if values[toknum] == "#DEFAULT":
                        # Attribute value is going to be defaulted.
                        # FIXME: do I have to know what the defaulted value is, or can I
                        # just delete the original attribute?
                        del new_attrs[name]
                        #new_attrs[name] = attval
                    
                    # #CONTENT
                    elif values[toknum] == "#CONTENT":

                        # Map content to attribute value

                        arch.parse_state.add_CONTENT_attribute(name)
                        del new_attrs[name]
                    
                    # ATT(ORCON)
                    elif not values[toknum] in self.renamer_keywords:
                        
                        # Rename attribute
                        # Check if attribute exist before deleting, unless an exception might be thrown
                        del new_attrs[name]
                        new_attrs[values[toknum]] = attval
                        
                    else:
                        raise ArchException("Bad value for renamer attribute: %s (token %d: %s)" % (values, toknum, values[toknum]))
                    toknum = maptoken_toknum
                    continue

                # ARCCONT
                elif values[toknum] == "#ARCCONT":
                    toknum = toknum + 1
                    if toknum > len(values) - 1:
                        raise ArchException("ATTNAME value for #ARCCONT missing: %s (token %d)" % (values, toknum))

                    # Attribute is deleted, but content of attribute is to become
                    # the content of the element

                    #FIXME: check whether the attribute already exist
                    arch.parse_state.set_ARCCONT_value(new_attrs[values[toknum]])
                    del new_attrs[values[toknum]]
                    
                # #GI
                elif values[toknum] == "#GI":
                    toknum = toknum + 1

                    # Map generic identifier to attribute value
                    new_attrs[values[toknum]] = self.get_current_element_name()
                    
                # Illegal token
                else:
                    raise ArchException("Bad value for renamer attribute: %s (token %d: %s)" % (values, toknum, values[toknum]))
            
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

        # Write debug information
        if self.debug_level >= 3: self.debug_file.write("{" + str(arch.parse_state.get_suppression()) + "," + str(arch.parse_state.get_ignore_data()) + "}")

        return new_attrs

# ============================================================================
# XML architecture class
# ============================================================================

class Architecture:

    """Class that represents an XML architecture."""

    def __init__(self, attrs = None):

        """Initialize a new instance."""
        
        self.reset()

        if attrs: self.load(attrs)
        
        self.parse_state = None
        self.broadcaster = saxutils.EventBroadcaster([])

    # ----------------------------------------------------------------------------
    # Set methods

    def set_broadcaster(self, broadcaster):

        """Set the event broadcaster to use.

        The default broadcaster is xml.sax.saxutils.EventBroadcaster([]). See the python SAX
        modules for more information about EventBroadcaster."""

        self.broadcaster = broadcaster

    def get_broadcaster(self):

        """Get the current event broadcaster.

        The default broadcaster is xml.sax.saxutils.EventBroadcaster([])."""

        return self.broadcaster
    
    def reset (self):

        """Reset the architecure.

        This method clears all architectual information stored within the Architecture object.

        get_name(), get_public_id(), get_dtd_public_id(), get_dtd_system_id(), get_form_att(),
        get_renamer_att(), get_suppressor_att, get_ignore_data_att(), get_doc_elem_form(),
        get_bridge_form(), get_data_form(), get_auto is set to None. is_declared()
        returns 0."""

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

        """Load information about the architecture based on preparsed attribute list.

        The prepared  attribute list usually comes from the architecture use declaration.
        You may also supply your own when needed. This is more or less the same as using
        the setter/getter methods."""
        
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
            self.set_auto(attrs["auto"])
 
        if attrs.has_key("options"):
            pass # FIXME: do something with these.

    # ----------------------------------------------------------------------------
    # Parsestate methods

    def set_parse_state(self, parse_state):
        """Set the architecture parse_state."""
        self.parse_state = parse_state

    def get_parse_state(self, parse_state):
        """Get the architecture parse_state."""
        return self.parse_state

    # ----------------------------------------------------------------------------
    # Architecture information methods

    def set_name(self, name):
        """Set the architecture name."""
        self.name = name
        
    def get_name(self):
        """Get the architecture name."""
        return self.name

    def set_public_id(self, public_id):
        """Set the public identifier of the architecture specification document."""
        self.public_id = public_id
        
    def get_public_id(self):
        """Get the public identifier of the architecture specification document."""
        return self.public_id

    def set_dtd_public_id(self, dtd_public_id):
        """Set the public identifier of the architectural meta-DTD."""
        self.dtd_public_id = dtd_public_id
        
    def get_dtd_public_id(self):
        """Get the public identifier of the architectural meta-DTD."""
        return self.dtd_public_id

    def set_dtd_system_id(self, dtd_system_id):
        """Set the system identifier of the architectural meta-DTD."""
        self.dtd_system_id = dtd_system_id
        
    def get_dtd_system_id(self):
        """Get the system identifier of the architectural meta-DTD."""
        return self.dtd_system_id

    def set_form_att(self, form_att):
        """Set the architectural form attribute name."""
        self.form_att = form_att
        
    def get_form_att(self):
        """Get the architectural form attribute name."""
        return self.form_att

    def set_renamer_att(self, renamer_att):
        """Set the architectural attribute renamer attribute name."""
        self.renamer_att = renamer_att
        
    def get_renamer_att(self):
        """Get the architectural attribute renamer attribute name."""
        return self.renamer_att

    def set_suppressor_att(self, suppressor_att):
        """Set the architecture suppressor attribute name."""
        self.suppressor_att = suppressor_att
        
    def get_suppressor_att(self):
        """Get the architecture suppressor attribute name."""
        return self.suppressor_att

    def set_ignore_data_att(self, ignore_data_att):
        """Set the architecture ignore data attribute name."""
        self.ignore_data_att = ignore_data_att
        
    def get_ignore_data_att(self):
        """Get the architecture ignore data attribute name."""
        return self.ignore_data_att

    def set_doc_elem_form(self, doc_elem_form):
        """Set the architecture document element form name."""
        self.doc_elem_form = doc_elem_form
        
    def get_doc_elem_form(self):
        """Get the architecture document element form name."""
        return self.doc_elem_form

    def set_bridge_form(self, bridge_form):
        """Set the architecture bridge form name."""
        self.bridge_form = bridge_form
        
    def get_bridge_form(self):
        """Get the architecture bridge form name."""
        return self.bridge_form

    def set_data_form(self, data_form):
        """Set the architecture data form name."""
        self.data_form = data_form
        
    def get_data_form(self):
        """Get the architecture data form name."""
        return self.data_form

    def set_auto(self, auto):
        """Set the architecture automatic form mapping type."""
        if auto in ("ArcAuto", "nArcAuto"):
            self.auto = auto
        else:
            raise ArchException("Bad value auto: %s" % (auto))
        
    def get_auto(self):
        """Get the architecture automatic form mapping type."""
        return self.auto

    def is_declared(self):
        """Has the architecture been declared?"""
        return self.declared
    
# ============================================================================
# Parse state class
# ============================================================================

class ArchParseState:

    """Class representing parsing state with regard to XML architectures."""

    def __init__(self, parent = None):

        """Initialize a new instance."""

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
            self.ignore_data = parent.ignore_data
            self.CONTENT_active = parent.CONTENT_active
        else:
            self.suppression = self.sArcNone
            self.ignore_data = self.cArcIgnD
            self.CONTENT_active = 0

        self.attributes = {}
        self.parent = parent # The parent parse state
        self.elem_form = None # Name of the architectual form
        self.renamer = None # Name of the renamer attribute

        # ARCCONT and CONTENT
        self.CONTENT_value = []
        self.CONTENT_attributes = {}

        self.ARCCONT_active = 0
        self.ARCCONT_value = None
        
        self.seen_id = None

    # ----------------------------------------------------------------------------
    # Setter and getter methods

    def set_attribute_value(self, attribute, value):

        """Set a attribute value."""

        self.attributes[attribute] = value

    def set_attributes(self, attributes):

        """Set the attributes."""

        self.attributes = attributes

    def get_attributes(self):

        """Get the attributes."""

        return self.attributes

    # Suppression methods    

    def set_suppression(self, suppression):

        """Set a new suppression state."""

        if not self.suppression == self.sArcAll:
            self.suppression = suppression

    def get_suppression(self):

        """Get the suppression state."""

        return self.suppression
    
    def get_parent_suppression(self):

        """Get the suppression state of the parent."""

        if self.parent:
            return self.parent.suppression
        
        return self.suppression

    # Data ignore methods
    
    def set_ignore_data(self, ignore_data):

        """Set the ignore data state."""

        self.ignore_data = ignore_data

    def get_ignore_data(self):

        """Get the ignore data state."""

        return self.ignore_data
    
    # Parent methods
    
    def set_parent(self, parent):

        """Set the parent state."""

        self.parent = parent

    def get_parent(self):

        """Get the parent state."""

        return self.parent
    
    # Form methods
    
    def set_elem_form(self, elem_form):

        """Set the element form."""
        
        self.elem_form = elem_form

    def get_elem_form(self):

        """Get the element form."""

        return self.elem_form
    
    # Renamer methods
    
    def set_renamer(self, renamer):

        """Set the renamer."""

        self.renamer = renamer

    def get_renamer(self):

        """Get the renamer."""

        return self.renamer

    def set_ARCCONT_value(self, ARCCONT_value):

        """Set mapped #ARCCONT content."""

        self.ARCCONT_active = 1
        self.ARCCONT_value = ARCCONT_value
        self.set_suppression(self.sArcAll)

    def get_ARCCONT_value(self):
        
        """Get mapped #ARCCONT content."""

        return self.ARCCONT_value

    def is_ARCCONT_active(self):
        
        """Returns true if an attribute value should be mapped to content."""

        if self.ARCCONT_active:
            return 1
        else:
            return 0

    def add_CONTENT_attribute(self, attr):

        """Add an attribute as a target of the mapping of the content."""

        self.CONTENT_active = 1
        self.CONTENT_attributes[attr] = ""
        self.set_suppression(self.sArcAll)

    def set_CONTENT_attribute_value(self, attr, value):

        """Set mapped attribute content."""

        # FIXME: do we also need a getter for this one?
        self.CONTENT_attributes[attr] = value

    def is_CONTENT_active(self):
        
        """Returns true if content should be mapped to attribute(s)."""

        if self.CONTENT_active:
            return 1
        else:
            return 0

    def add_CONTENT_value(self, CONTENT_value):

        """Add value to mapped #CONTENT content."""

        self.CONTENT_value.append(CONTENT_value)

    def get_CONTENT_value(self):
        
        """Get mapped #CONTENT content."""

        return string.join(self.CONTENT_value, "")

    def set_seen_id(self, seen_id):

        """Set the seen id flag."""

        self.seen_id = seen_id

    def get_seen_id(self):
        
        """Get the seen id flag."""

        return self.seen_id

# ============================================================================
# XML architecture exception
# ============================================================================

class ArchException(saxlib.SAXException):

    """Architecture Exception"""

    def __init__(self, msg, exception = None):

        """Intitialize a new instance."""

        self.msg=msg
        self.exception=exception

    def get_message(self):

        """Return a message for this exception."""

        return self.msg

    def get_exception(self):

        """Return the embedded exception, if any."""

        return self.exception

    def __str__(self):

        """Create a string representation of the exception."""

        return self.msg

# ============================================================================
# Attribute parsing class
# ============================================================================

class AttributeParser:

    """Class used for parsing attribute specification strings.

    xmlarch uses it to parse the data part of processing instructions (the architectural
    use declaration)."""

    # ----------------------------------------------------------------------------
    # Initialization

    def __init__(self, data):

        """Initialize a new instance."""
        
        self.data = data
        self.pos = 0

    # ----------------------------------------------------------------------------
    # Parse data and return an attribute dict

    def parse(self):

        """Parse the attribute specification string."""

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

        """Skip whitespace."""

        while (self.pos < len(self.data)):
            if self.data[self.pos] in (' ', "\t", "\n"):
                self.pos = self.pos + 1
                continue
            else:
                break
            
    # ----------------------------------------------------------------------------
    # Skip equal sign

    def skip_equal(self):

        """Skip equal sign."""
            
        self.skip_whitespace()
        if (self.pos >= len(self.data) or self.data[self.pos] != '='):
            raise ArchException("AttributeParser: Expected '='.")
        
        self.pos = self.pos + 1
        self.skip_whitespace()
        
    # ----------------------------------------------------------------------------
    # Read name
            
    def read_name(self):

        """Read attribute name."""

        buf = ""

        while (self.pos < len(self.data)):
            if self.data[self.pos] in (' ', "\t", "\n", "="):
                if len(buf) == 0:
                    raise ArchException("AttributeParser: Name expected.")
                else:
                    return buf
            else:
                buf = buf + self.data[self.pos]
                self.pos = self.pos + 1

        if len(buf) == 0:
            raise ArchException("AttributeParser: Name expected.")
        else:
            return buf

    # ----------------------------------------------------------------------------
    # Read literal

    def read_value(self):

        """Read attribute value."""

        buf = ""
        lit = ""

        if (self.pos < len(self.data)):
            lit = self.data[self.pos]
            self.pos = self.pos + 1
        else:
            raise ArchException("AttributeParser: Assignment finished without literal value.")

        if (lit != '\'' and lit != '"'):
            raise ArchException("AttributeParser: Expected '\"' or \"'\".")

        while (self.data[self.pos] != lit):
            buf =  buf + self.data[self.pos]

            if self.pos > len(self.data):
                raise ArchException("AttributeParser: Unterminated literal.")
                
            self.pos = self.pos + 1

        self.pos = self.pos + 1
        return buf

# ============================================================================
# SAX document handler that produces prettified XML output
# ============================================================================

class Prettifier(saxlib.HandlerBase):

    """A SAX document handler that produces normalized/prettified XML output.

    This class produces a prettified XML document instance."""

    def __init__(self, writer=sys.stdout):

        """Initialize a new instance."""

        self.writer = writer
        self.elem_level=0
        self.indentor = "  "
        self.ignore_outside_docelem = 1
        self.elem_stack = []
        
        self.FULLINDENT = 0
        self.NOINDENT = 1

        self.CHILDREN = 0
        self.NOCHILDREN = 1

        self.xmldecl = '<?xml version="1.0" standalone="yes"?>\n'
        
    def indent(self, mode):

        """Method for doing indenting."""

        if mode == self.FULLINDENT:
            self.writer.write("\n")
        elif mode == self.NOINDENT:
            return
        
        self.writer.write(self.indentor * self.elem_level)

    def set_xml_decl(self, xmldecl):

        """Set the xml declaration that should be output."""

        self.xmldecl = xmldecl

    def set_writer(self, writer):

        """Set the output stream to use."""

        self.writer = writer
        
    # ----------------------------------------------------------------------------
    # SAX events

    def processingInstruction (self, target, remainder):

        """Handle a processing instruction event."""

        self.writer.write("<?" + target + " " + remainder + "?>\n")
        
    def startElement(self, name, amap):

        """Handle an event for the beginning of an element."""
            
        if not self.elem_stack:
            self.elem_stack.append(self.NOCHILDREN)
        else:
            self.elem_stack[-1] = self.CHILDREN
            self.indent(self.FULLINDENT)
            self.elem_stack.append(self.NOCHILDREN)
            
        self.writer.write("<" + name)
        
        a_names=amap.keys()
        a_names.sort()

        for a_name in a_names:
            self.writer.write(" " + a_name + "=\"")
            self.writer.write(amap[a_name])
            self.writer.write("\"")
        self.writer.write(">")

        self.elem_level = self.elem_level + 1
        
    def endElement(self, name):

        """Handle an event for the end of an element."""

        if self.elem_stack[-1] == self.CHILDREN:
            self.indent(self.FULLINDENT)
            
        self.writer.write("</" + name + ">")
        
        self.elem_level= self.elem_level - 1
        del self.elem_stack[-1]
        
    def ignorableWhitespace(self, data, start_ix, length):

        """Handle an event for ignorable whitespace in element content."""

        return
        
    def characters(self, data, start_ix, length):

        """Handle a character data event."""
        
        self.writer.write(string.strip(data[start_ix:start_ix+length]))

    def startDocument(self):
        
        """Handle an event for the beginning of a document."""

        self.writer.write(self.xmldecl)

    def endDocument(self):

        """Handle an event for the end of a document."""

        self.writer.write("\n")

# ============================================================================
# Class that tracks method calls on itself.
# ============================================================================

class EventTracker:

    """Class that tracks method calls on itself."""

    def __init__(self):

        """Initialize a new instance."""

        self.events = {}
        self.name = None
        
    def __repr__(self):

        """Return a textual representation of the object."""
        
        return "<OriginalEvent instance at %d>" % id(self)

    def __nonzero__(self):

        """Return true when asked if __nonzero__"""
        
        return 1

    def __getattr__(self, name):

        """Get attribute."""
        
        self.name = name
        return self

    def __call__(self, *args):

        """Call method."""
        
        self.set_event(self.name, args)

    def set_event(self, name, args):

        """Register a method call name with the arguments args."""
        
        self.events[name] = args
        
    def get_event(self, name):

        """Returns the arguments of the given method."""
        
        return self.events[name]
    
    def get_events(self):

        """Returns a hash containing the arguments - indexed my method name."""
        
        return self.events
