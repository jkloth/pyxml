########################################################################
#
# File Name:            Event.py
#
# Documentation:        http://docs.4suite.com/4DOM/Event.py.html
#
# History:
# $Log: Event.py,v $
# Revision 1.1  2000/09/27 23:45:24  uche
# Update to 4DOM from 4Suite 0.9.1
#
# Revision 1.1  2000/07/09 19:02:20  uogbuji
# Begin implementing Events
# bug-fixes
#
#
#
"""
Implements DOM level 2 Mutation Events
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""



supportedEvents = [
    "DOMSubtreeModified",
    "DOMNodeInserted",
    "DOMNodeRemoved",
    "DOMNodeRemovedFromDocument",
    "DOMNodeInsertedIntoDocument",
    "DOMAttrModified",
    "DOMCharacterDataModified"
    ]

#Event Exception code
UNSPECIFIED_EVENT_TYPE_ERR = 0

class EventException:
    def __init__(self, code):
        self.code = code

        
class EventTarget:
    """
    """
    def __init__(self):
        self.listeners = {}
        for etype in supportedEvents:
            self.listeners[etype] = []
        return

    def addEventListener(self, etype, listener, useCapture):
        if listener not in listeners[etype]:
            self.listeners[etype].append(listener)
        return

    def removeEventListener(self, etype, listener, useCapture):
        self.listeners[etype].remove(listener)
        return

    def dispatchEvent(self, evt):
        #No bubbling or capturing yet
        for listener in self.listeners[evt.type]:
            listener.handleEvent(evt)
        return evt._4dom_preventDefaultCalled


class EventListener:
    def __init__(self):
        pass

    def handleEvent(evt):
        pass


class Event:
    CAPTURING_PHASE = 1
    AT_TARGET = 2
    BUBBLING_PHASE = 3

    def __init__(self, target=None, currNode=None):
        self.target = target
        self.currentNode = currNode
        self.eventPhase = Event.CAPTURING_PHASE
        return

    def stopPropagation(self):
        pass

    def preventDefault(self):
        self._4dom_preventDefaultCalled = 1

    def initEvent(self, eventTypeArg, canBubbleArg, cancelableArg):
        self.type = eventTypeArg
        self.bubbles = canBubbleArg
        self.cancelable = cancelableArg
        self._4dom_preventDefaultCalled = 0
        return


class MutationEvent(Event):
    #Whether or not the event bubbles
    eventSpec = {
        "DOMSubtreeModified": 1,
        "DOMNodeInserted": 1,
        "DOMNodeRemoved": 1,
        "DOMNodeRemovedFromDocument": 0,
        "DOMNodeInsertedIntoDocument": 0,
        "DOMAttrModified": 1,
        "DOMCharacterDataModified": 1
        }

    def __init__(self, target=None, currNode=None):
        Event.__init__(self)
        return

    def initMutationEvent(self, typeArg, canBubbleArg, cancelableArg, relatedNodeArg, prevValueArg, newValueArg, attrNameArg):
        Event.initEvent(eventTypeArg, canBubbleArg, cancelableArg)
        self.relatedNode = relatedNode
        self.relatedNode = relatedNodeArg
        self.prevValue = prevValueArg
        self.nextValue = nextValueArg
        self.newValue = newValueArg
        self.attrName = attrNameArg
        #No mutation events are cancelable
        self.cancelable = 0
        return

