########################################################################
#
# File Name:            Node.py
#
# Documentation:        http://docs.4suite.com/4DOM/Node.py.html
#
"""
Implements the basic tree structure of DOM
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import DOMImplementation
implementation = DOMImplementation.implementation
dom = implementation._4dom_fileImport('')
Event = implementation._4dom_fileImport('Event')

DOMException = dom.DOMException
NoModificationAllowedErr = dom.NoModificationAllowedErr
NotFoundErr = dom.NotFoundErr
HierarchyRequestErr = dom.HierarchyRequestErr
WrongDocumentErr = dom.WrongDocumentErr
InvalidCharacterErr = dom.InvalidCharacterErr

import re, copy, sys
#FIXME: should allow combining characters: fix when Python gets Unicode
g_namePattern = re.compile('[a-zA-Z_:][\w\.\-_:]*\Z')

import types
StringTypes = [types.StringType]
if sys.version[0] == '2':
    StringTypes.append(types.UnicodeType)

class Node(dom.Node,Event.EventTarget):
    """
    Encapsulates the pieces that DOM builds on the basic tree structure,
    Which is implemented by composition of TreeNode
    """

    # Internally used node types
    # Node types up to 200 are reserved by W3C
    _NODE_LIST                  = 201
    _NAMED_NODE_MAP             = 202

    nodeType = None
    # Children that this node is allowed to have
    _allowedChildren = []

    def __init__(self, ownerDocument, namespaceURI, prefix, localName):
        Event.EventTarget.__init__(self)
        self.__dict__['__nodeName'] = ''
        self.__dict__['__nodeValue'] = ''
        self.__dict__['__parentNode'] = None
        self.__dict__['__childNodes'] = None
        self.__dict__['__firstChild'] = None
        self.__dict__['__lastChild'] = None
        self.__dict__['__previousSibling'] = None
        self.__dict__['__nextSibling'] = None
        self.__dict__['__attributes'] = None
        self.__dict__['__ownerDocument'] = ownerDocument
        self.__dict__['__namespaceURI'] = namespaceURI
        self.__dict__['__prefix'] = prefix
        self.__dict__['__localName'] = localName
        self.__dict__['__childNodes'] = implementation._4dom_createNodeList([])
        self.__dict__['__readOnly'] = 0

    ### Attribute Access Methods -- Node.attr ###

    def __getattr__(self, name):
        attrFunc = self._readComputedAttrs.get(name)
        if attrFunc:
            return attrFunc(self)
        else:
            return getattr(Node, name)

    def __setattr__(self, name, value):
        #Make sure attribute is not read-only
        if name in self.__class__._readOnlyAttrs:
            raise NoModificationAllowedErr()
        #If it's computed execute that function
        attrFunc = self.__class__._writeComputedAttrs.get(name)
        if attrFunc:
            attrFunc(self, value)
        #Otherwise, just set the attribute
        else:
            self.__dict__[name] = value

    ### Attribute Methods -- Node._get_attr() ###

    def _get_nodeName(self):
        return self.__dict__['__nodeName']

    def _get_nodeValue(self):
        return self.__dict__['__nodeValue']

    def _set_nodeValue(self,value):
        self.__dict__['__nodeValue'] = value

    def _get_nodeType(self):
        return getattr(self.__class__,'nodeType')

    def _get_parentNode(self):
        return self.__dict__['__parentNode']

    def _get_childNodes(self):
        return self.__dict__['__childNodes']

    def _get_firstChild(self):
        return self.__dict__['__firstChild']

    def _get_lastChild(self):
        return self.__dict__['__lastChild']

    def _get_previousSibling(self):
        return self.__dict__['__previousSibling']

    def _get_nextSibling(self):
        return self.__dict__['__nextSibling']

    def _get_ownerDocument(self):
        return self.__dict__['__ownerDocument']

    def _get_attributes(self):
        return self.__dict__['__attributes']

    def _get_namespaceURI(self):
        return self.__dict__['__namespaceURI']

    def _get_prefix(self):
        return self.__dict__['__prefix']

    def _set_prefix(self, value):
        # Check for invalid characters
        if not g_namePattern.match(value):
            raise InvalidCharacterErr()
        #FIXME: Check for NAMESPACE_ERR
        self.__dict__['__prefix'] = value

    def _get_localName(self):
        return self.__dict__['__localName']

    ### Methods ###

    def insertBefore(self, newChild, refChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            self._4dom_insertDocFragmentBefore(newChild, refChild);
        elif refChild == None:
            return self.appendChild(newChild);
        else:
            #Make sure the newChild is all it is cracked up to be
            self._4dom_validateNode(newChild)

            #Make sure the refChild is indeed our child
            index = self._4dom_getChildIndex(refChild)
            if index == -1:
                raise NotFoundErr()

            #Remove from old parent
            if newChild.parentNode != None:
                newChild.parentNode.removeChild(newChild);

            #Insert it
            self.__dict__['__childNodes'].insert(index, newChild)

            #Setup the caches
            if index == 0:
                self.__dict__['__firstChild'] = newChild

            #Update the child caches
            if index != 0:
                if self.__dict__['__childNodes'][index-1].nextSibling != None:
                    newChild._4dom_setNextSibling(self.__dict__['__childNodes'][index-1].nextSibling)
                    newChild.nextSibling._4dom_setPreviousSibling(newChild)
                newChild._4dom_setPreviousSibling(self.__dict__['__childNodes'][index-1])
                self.__dict__['__childNodes'][index-1]._4dom_setNextSibling(newChild)
            elif self.__dict__['__childNodes'].length >= 2:
                newChild._4dom_setNextSibling(self.__dict__['__childNodes'][1])
                self.__dict__['__childNodes'][1]._4dom_setPreviousSibling(newChild)
            newChild._4dom_setParentNode(self)

            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
            return newChild

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            self._4dom_replaceDocumentFragment(newChild, oldChild)
        else:
            self._4dom_validateNode(newChild)
            #Make sure the oldChild is indeed our child
            index = self._4dom_getChildIndex(oldChild)
            if index == -1:
                raise NotFoundErr()

            self.__dict__['__childNodes'][index] = newChild
            if newChild.parentNode is not None:
                newChild.parentNode.removeChild(newChild)
                
            newChild._4dom_setNextSibling(oldChild.nextSibling)
            newChild._4dom_setPreviousSibling(oldChild.previousSibling)

            if newChild.nextSibling:
                newChild.nextSibling._4dom_setPreviousSibling(newChild)
            if newChild.previousSibling:
                newChild.previousSibling._4dom_setNextSibling(newChild)
            newChild._4dom_setParentNode(self)


            oldChild._4dom_fireMutationEvent('DOMNodeRemoved',relatedNode=self)
            oldChild._4dom_setNextSibling(None)
            oldChild._4dom_setPreviousSibling(None)
            oldChild._4dom_setParentNode(None)
            
            if self.__dict__['__childNodes'].length:
                self.__dict__['__firstChild'] = self.__dict__['__childNodes'][0]
                self.__dict__['__lastChild'] = self.__dict__['__childNodes'][-1]

            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
            return oldChild

    def removeChild(self, childNode):
        #Make sure the childNode is indeed our child
        #FIXME: more efficient using list.remove()
        index = self._4dom_getChildIndex(childNode)
        if index == -1:
            raise NotFoundErr()
        childNode._4dom_fireMutationEvent('DOMNodeRemoved',relatedNode=self)
        self._4dom_fireMutationEvent('DOMSubtreeModified')
        del self.childNodes[index]
        #Adjust caches
        if self.__dict__['__childNodes'].length:
            self.__dict__['__firstChild'] = self.__dict__['__childNodes'][0]
            self.__dict__['__lastChild'] = self.__dict__['__childNodes'][-1]
            if index != 0:
                if childNode.nextSibling:
                    childNode.nextSibling._4dom_setPreviousSibling(childNode.previousSibling)
                childNode.previousSibling._4dom_setNextSibling(childNode.nextSibling)
            else:
                self.childNodes[0]._4dom_setPreviousSibling(None)
        else:
            self.__dict__['__firstChild'] = None
            self.__dict__['__lastChild'] = None
        childNode._4dom_setNextSibling(None)
        childNode._4dom_setPreviousSibling(None)
        childNode._4dom_setParentNode(None)
        return childNode

    def appendChild(self, newChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            self._4dom_appendDocumentFragment(newChild)
        else:
            self._4dom_validateNode(newChild)
            #Remove from old parent
            if newChild.parentNode != None:
                newChild.parentNode.removeChild(newChild);
            self.childNodes.append(newChild)
            #Adjust our pointers
            if self.__dict__['__childNodes'].length == 1:
                self.__dict__['__firstChild'] = newChild
            self.__dict__['__lastChild'] = newChild
            #Adjust our child's pointers
            if self.__dict__['__childNodes'].length >= 2:
                newChild._4dom_setPreviousSibling(self.__dict__['__childNodes'][-2])
                self.__dict__['__childNodes'][-2]._4dom_setNextSibling(newChild)
            newChild._4dom_setParentNode(self)
            newChild._4dom_fireMutationEvent('DOMNodeInserted',relatedNode=self)
            self._4dom_fireMutationEvent('DOMSubtreeModified')
            return newChild

    def hasChildNodes(self):
        return self.__dict__['__childNodes'].length != 0

    def cloneNode(self, deep, newOwner=None, readOnly=0):
        # Get constructor values
        if hasattr(self, '__getinitargs__'):
            args = self.__getinitargs__()
        else:
            args = []

        # Create the copy
        newNode = apply(self.__class__, args)

        # Set when cloning EntRef children
        if readOnly:
            newNode._4dom_setReadOnly(readOnly)

        # Get the current state
        getstate = getattr(self, '__getstate__', None)
        if getstate:
            state = getstate()
        else:
            state = {}

        # Set when clone is used for import
        if newOwner:
            newNode._4dom_setOwnerDocument(newOwner)

        # Assign the current state to the copy
        setstate = getattr(newNode, '__setstate__', None)
        if setstate:
            setstate(state)
        else:
            newNode.__dict__.update(state)

        # Copy the child nodes if deep
        if deep or self.nodeType == Node.ATTRIBUTE_NODE:
            # Children of EntRefs are cloned readOnly
            if self.nodeType == Node.ENTITY_REFERENCE_NODE:
                readOnly = 1
                
            for child in self.childNodes:
                new_child = child.cloneNode(1, newOwner, readOnly)
                newNode.appendChild(new_child)

        return newNode

    def normalize(self):
        #This one needs to join all adjacent text nodes
        node = self.__dict__['__firstChild']
        if not node:
            return
        while node and node.nextSibling:
            if node.nodeType == Node.TEXT_NODE:
                next = node.nextSibling
                while next and next.nodeType == Node.TEXT_NODE:
                    node.appendData(next.data)
                    node.parentNode.removeChild(next)
                    next = node.nextSibling
            elif node.nodeType == Node.ELEMENT_NODE:
                node.normalize()
            node = node.nextSibling

    def supports(self, feature, version):
        return implementation.hasFeature(feature,version)

    #
    # Event Target interface implementation
    #
    def dispatchEvent(self, evt):
        if not evt.type:
            raise Event.EventError(UNSPECIFIED_EVENT_TYPE)

        # the list of my ancestors for capture or bubbling
        # we are lazy, so we initialize this list only if required
        if evt._4dom_propagate and \
           (evt.eventPhase == evt.CAPTURING_PHASE or evt.bubbles):
            ancestors = [self]
            while  ancestors[-1].parentNode :
                ancestors.append(ancestors[-1].parentNode)

        # event capture
        if evt._4dom_propagate and evt.eventPhase == evt.CAPTURING_PHASE :
            ancestors.reverse()
            for a in ancestors[:-1]:
                evt.currentTarget = a
                for captor in a.capture_listeners[evt.type]:
                    captor.handleEvent(evt)
                if not evt._4dom_propagate:
                    break
            # let's put back the list in the right order
            # and move on to the next phase
            ancestors.reverse()
            evt.eventPhase = evt.AT_TARGET


        # event handling by the target
        if evt._4dom_propagate and evt.eventPhase == evt.AT_TARGET :
            evt.currentTarget = self
            for listener in self.listeners[evt.type]:
                listener.handleEvent(evt)
            # prepare for the next phase, if necessary
            if evt.bubbles:
                evt.eventPhase = evt.BUBBLING_PHASE

        # event bubbling
        if evt._4dom_propagate and evt.eventPhase == evt.BUBBLING_PHASE :
            for a in ancestors[1:]:
                evt.currentTarget = a
                for listener in a.listeners[evt.type]:
                    listener.handleEvent(evt)
                if not evt._4dom_propagate:
                    break
                
        return evt._4dom_preventDefaultCalled



    #Functions not defined in the standard
    #All are fourthought internal functions
    #and should only be called by you if you specifically
    #don't want your program to run :)

    def _4dom_fireMutationEvent(self,eventType,target=None,
                                 relatedNode=None,prevValue=None,
                                 newValue=None,attrName=None,attrChange=None):
        if self.supports('MutationEvents', 2.0):
            evt = self.ownerDocument.createEvent(eventType)
            evt.target = target or self
            evt.initMutationEvent(eventType,evt.eventSpec[eventType],0,
                                  relatedNode,prevValue,newValue,attrName)
            evt.attrChange = attrChange
            evt.target.dispatchEvent(evt)
            
    def _4dom_appendDocumentFragment(self, frag):
        """Insert all of the top level nodes"""
        head = frag.firstChild
        while head != None:
            frag.removeChild(head)
            self.appendChild(head)
            head = frag.firstChild
        return frag

    def _4dom_insertDocFragmentBefore(self,frag,oldChild):
        """Insert all of the top level nodes before the oldChild"""
        head = frag.firstChild
        while head != None:
            frag.removeChild(head)
            self.insertBefore(head,oldChild)
            head = frag.firstChild
        return frag

    def _4dom_replaceDocumentFragment(self,frag,oldChild):
        #Do a insertBefore on oldChild->NextSibling
        nextSib = oldChild.nextSibling;
        #get rid of the old Child
        self.removeChild(oldChild);
        if nextSib == None:
            self._4dom_appendDocumentFragment(frag);
        else:
            self._4dom_insertDocFragmentBefore(frag,nextSib);
        return oldChild

    def _4dom_validateNode(self, newNode):
        if not newNode.nodeType in self.__class__._allowedChildren:
            raise HierarchyRequestErr()
        if self.ownerDocument != newNode.ownerDocument:
            raise WrongDocumentErr()

    def _4dom_validateString(self, value):
        if type(value) not in StringTypes:
            raise InvalidCharacterErr()
        return value

    def _4dom_getChildIndex(self,child):
        if child in self.__dict__['__childNodes']:
            return self.__dict__['__childNodes'].index(child)
        return -1

    def _4dom_setParentNode(self, parent):
        self.__dict__['__parentNode'] = parent

    def _4dom_setNextSibling(self,next):
        self.__dict__['__nextSibling'] = next

    def _4dom_setPreviousSibling(self,prev):
        self.__dict__['__previousSibling'] = prev

    def _4dom_setOwnerDocument(self, owner):
        self.__dict__['__ownerDocument'] = owner

    def _4dom_setReadOnly(self, flag):
        self.__dict__['__readOnly'] = flag

    ### Helper Functions For Cloning ###

    def __getinitargs__(self):
        return (self.__dict__['__ownerDocument'],
                self.__dict__['__namespaceURI'],
                self.__dict__['__prefix'],
                self.__dict__['__localName']
                )

    def __getstate__(self):
        return {'__nodeValue':self.nodeValue}

    def __setstate__(self, state):
        self.__dict__.update(state)

    ### Attribute Access Mappings ###

    _readComputedAttrs = {'nodeName':_get_nodeName,
                          'nodeValue':_get_nodeValue,
                          'nodeType':_get_nodeType,
                          'parentNode':_get_parentNode,
                          'childNodes':_get_childNodes,
                          'firstChild':_get_firstChild,
                          'lastChild':_get_lastChild,
                          'previousSibling':_get_previousSibling,
                          'nextSibling':_get_nextSibling,
                          'attributes':_get_attributes,
                          'ownerDocument':_get_ownerDocument,
                          'namespaceURI':_get_namespaceURI,
                          'prefix':_get_prefix,
                          'localName':_get_localName
                          }

    _writeComputedAttrs = {'nodeValue':_set_nodeValue,
                           'prefix':_set_prefix
                           }

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            _readComputedAttrs.keys())
