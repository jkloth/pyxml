########################################################################
#
# File Name:            Visitor.py
#
# Documentation:        http://docs.4suite.com/4DOM/Visitor.py.html
#
# History:
# $Log: Visitor.py,v $
# Revision 1.2  2000/06/20 15:51:29  uche
# first stumblings through 4Suite integration
#
# Revision 1.3  2000/06/09 01:37:43  jkloth
# Fixed copyright to Fourthought, Inc
#
# Revision 1.2  2000/05/22 16:29:33  uogbuji
# Kill tabs
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.9  2000/03/01 03:23:14  uche
# Fix Oracle driver EscapeQuotes
# Add credits file
# Fix Various DOM bugs
#
# Revision 1.8  1999/11/18 09:30:02  uche
# Python/DOM binding update.
#
# Revision 1.7  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.6  1999/08/29 04:07:59  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""



class Visitor:
    def visit(self, node):
        """Default behavior for the visitor is simply to print an informational message"""
        print "Visiting %s node %s\n"%(node.nodeType, node.nodeName)
        return None

class WalkerInterface:
    def __init__(self, visitor):
        self.visitor = visitor
        pass

    def step(self):
        """Advance to the next item in order, visit, and then pause"""
        pass

    def run(self):
        """Continue advancing from the current position through the last leaf node without pausing."""
        pass


class PreOrderWalker(WalkerInterface):
    def __init__(self, visitor, startNode):
        WalkerInterface.__init__(self, visitor)
        self.node_stack = []
        self.node_stack.append(startNode)

    def step(self):
        """
        Visits the current node, and then advances to its first child,
        if any, else the next sibling.
        returns a tuple completed, ret_val
        completed -- flags whether or not we've traversed the entire tree
        ret_val -- return value from the visitor
        """
        completed = 0
        ret_val = self.visitor.visit(self.node_stack[-1])
        if (self.node_stack[-1].hasChildNodes()):
            self.node_stack.append(self.node_stack[-1].firstChild)
        else:
            #Back-track until we can find a node with an unprocessed sibling
            next_sib = None
            while not next_sib and not completed:
                next_sib = self.node_stack[-1].nextSibling
                del self.node_stack[-1]
                if next_sib:
                    self.node_stack.append(next_sib)
                else:
                    if not len(self.node_stack):
                        completed = 1
        return completed, ret_val

    def run(self):
        completed = 0
        while not completed:
            completed, ret_val = self.step()


#Set the default Walker class to the PreOrderWalker.
#User can change this according to preferences
Walker = PreOrderWalker

