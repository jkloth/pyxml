########################################################################
#
# File Name:            Node.py
#
# Documentation:        http://docs.4suite.com/4DOM/Node.py.html
#
# History:
# $Log: Node.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.62  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.61  2000/05/24 07:53:52  molson
# Fixed bug Glenn forgot to check in.,  Ask him what it is a bout
#
# Revision 1.60  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.59  2000/05/06 03:14:05  molson
# Fixed import errors
#
# Revision 1.58  2000/04/27 18:19:54  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.57  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.56  2000/01/26 05:53:31  uche
# Fix AVTs
# Implement optimization by delaying and not repeating parser invocation
# Completed error-message framework
# NaN --> None, hopefully temporarily
#
# Revision 1.55  1999/12/07 08:12:31  molson
# Fixed errors in parser
#
# Revision 1.54  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.53  1999/11/26 08:22:43  uche
# Complete python/DOM binding updates for XML
#
# Revision 1.52  1999/11/19 02:13:23  uche
# Python/DOM binding update.
#
# Revision 1.51  1999/11/19 01:08:12  molson
# Tested Document with new interface
#
# Revision 1.50  1999/11/18 09:59:06  molson
# Converted Element to no python/DOM binding
# Removed Factories
#
# Revision 1.49  1999/11/18 07:50:59  molson
# Added namespaces to Nodes
#
# Revision 1.48  1999/11/18 07:02:09  molson
# Removed Factories from node and node list and named node map
#
# Revision 1.47  1999/11/18 06:42:41  molson
# Convert to new interface
#
# Revision 1.46  1999/11/18 06:38:36  uche
# Changes to new Python/Dom Binding
#
# Revision 1.45  1999/11/16 03:25:43  molson
# Finished testing node in the new format
#
# Revision 1.44  1999/11/16 02:31:43  molson
# Started change over to complete orbless environment
#
# Revision 1.43  1999/10/19 19:12:39  uche
# Fixed TraceOut, docs,  and other minor bugs.
#
# Revision 1.42  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.41  1999/09/08 23:54:07  uche
# Add machinery for updated DOM Level 2 Iterators and Filters (untested)
#
# Revision 1.40  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.39  1999/08/31 19:03:10  uche
# Change NodeLists and NamedNodeMaps to use UserList and UserDict.
#
# Revision 1.38  1999/08/31 15:54:58  molson
# Abstracted node comparision to config_core.  Tested orbless and fnorb
#
# Revision 1.37  1999/08/31 14:45:51  molson
# Tested over the orb with Fnorb
#
# Revision 1.36  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
Implements the basic tree structure of DOM
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import implementation
from xml.dom import DOMException
from xml.dom import NO_MODIFICATION_ALLOWED_ERR
from xml.dom import NOT_FOUND_ERR
from xml.dom import HIERARCHY_REQUEST_ERR
from xml.dom import WRONG_DOCUMENT_ERR
from xml.dom import INVALID_CHARACTER_ERR

import copy, sys

class Node:
    """
    Encapsulates the pieces that DOM builds on the basic tree structure,
    Which is implemented by composition of TreeNode
    """

    # Node types
    ELEMENT_NODE                = 1
    ATTRIBUTE_NODE              = 2
    TEXT_NODE                   = 3
    CDATA_SECTION_NODE          = 4
    ENTITY_REFERENCE_NODE       = 5
    ENTITY_NODE                 = 6
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE                = 8
    DOCUMENT_NODE               = 9
    DOCUMENT_TYPE_NODE          = 10
    DOCUMENT_FRAGMENT_NODE      = 11
    NOTATION_NODE               = 12

    nodeType = None
    # Children that this node is allowed to have
    _allowedChildren = []

    def __init__(self, ownerDocument, namespaceURI, prefix, localName):
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
            raise DOMException(NO_MODIFICATION_ALLOWED_ERR)
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
        self._4dom_validateName(value)
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
                pass
                raise DOMException(NOT_FOUND_ERR)

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
        
            return newChild

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            self._4dom_replaceDocumentFragment(newChild, oldChild)
        else:
            self._4dom_validateNode(newChild)
            #Make sure the oldChild is indeed our child
            index = self._4dom_getChildIndex(oldChild)
            if index == -1:
                pass
                raise DOMException(NOT_FOUND_ERR)

            self.__dict__['__childNodes'][index] = newChild
            newChild._4dom_setNextSibling(oldChild.nextSibling)
            newChild._4dom_setPreviousSibling(oldChild.previousSibling)

            if newChild.nextSibling:
                newChild.nextSibling._4dom_setPreviousSibling(newChild)
            if newChild.previousSibling:
                newChild.previousSibling._4dom_setNextSibling(newChild)
            newChild._4dom_setParentNode(self)


            oldChild._4dom_setNextSibling(None)
            oldChild._4dom_setPreviousSibling(None)
            oldChild._4dom_setParentNode(None)

            if self.__dict__['__childNodes'].length:
                self.__dict__['__firstChild'] = self.__dict__['__childNodes'][0]
                self.__dict__['__lastChild'] = self.__dict__['__childNodes'][-1]
                
            return oldChild

    def removeChild(self, childNode):
        #Make sure the childNode is indeed our child
        #FIXME: more efficient using list.remove()
        index = self._4dom_getChildIndex(childNode)
        if index == -1:
            pass
            raise DOMException(NOT_FOUND_ERR)
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
            return newChild

    def hasChildNodes(self):
        return self.__dict__['__childNodes'].length != 0

    def cloneNode(self, deep, newNode=None, newOwner=None):
        if newNode == None:
            newNode = Node(self.ownerDocument, self.namespaceURI, self.prefix, self.localName)
        if newOwner == None:
            newOwner = newNode.ownerDocument
        newNode.nodeValue = self.__dict__['__nodeValue']
        if deep:
            for child in self.__dict__['__childNodes']:
                new_child = child.cloneNode(1, newOwner=newOwner)
                newNode.appendChild(new_child)
        return newNode

    def normalize(self):
        #This one needs to join all adjacent text nodes 
        curr_node = self.__dict__['__firstChild']
        if not curr_node:
            return
        while curr_node:
            while curr_node.nextSibling != None:
                if curr_node.nodeType == Node.TEXT_NODE and \
                    curr_node.nextSibling.nodeType == Node.TEXT_NODE:
                        #Join the next one and this one
                        curr_node = curr_node._4dom_joinText(curr_node,curr_node.nextSibling)
                else:
                    curr_node = curr_node.nextSibling
            curr_node = curr_node.nextSibling

        #Normalize the elements
        for child in self.__dict__['__childNodes']:
            if child.nodeType == Node.ELEMENT_NODE:
                child.normalize()
        return
                
    def supports(self, feature, version):
        return implementation.hasFeature(feature,version)

    #Functions not defined in the standard
    #All are fourthought internal functions
    #and should only be called by you if you specifically
    #don't want your program to run :)

    def _4dom_appendDocumentFragment(self, frag):
        """Insert all of the top level nodes"""
        pass
        head = frag.firstChild
        while head != None:
            frag.removeChild(head)
            self.appendChild(head)
            head = frag.firstChild
        return frag

    def _4dom_insertDocFragmentBefore(self,frag,oldChild):
        """Insert all of the top level nodes before the oldChild"""
        pass
        head = frag.firstChild
        while head != None:
            frag.removeChild(head)
            self.insertBefore(head,oldChild)
            head = frag.firstChild
        return frag
                                
    def _4dom_replaceDocumentFragment(self,frag,oldChild):
        #Do a insertBefore on oldChild->NextSibling
        pass
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
            pass
            pass
            raise DOMException(HIERARCHY_REQUEST_ERR)
        if self.ownerDocument != newNode.ownerDocument:
            pass
            raise DOMException(WRONG_DOCUMENT_ERR)

    def _4dom_validateString(self, string):
        #FIXME: complete list of invalid characters
        for char in string:
            if char in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)

    def _4dom_validateName(self, name):
        #FIXME: complete list of invalid characters
        for char in name:
            if char in ['<','>','&']:
                pass
                raise DOMException(INVALID_CHARACTER_ERR)

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
