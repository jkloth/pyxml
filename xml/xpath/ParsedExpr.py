########################################################################
#
# File Name:   ParsedExpr.py
#
# Docs:        http://docs.4suite.com/XPATH/ParsedExpr.py.html
#
"""
The implementation of all of the expression pared tokens.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, UserList, types

from xml.dom.ext import SplitQName
from xml.xpath import XPath, g_extFunctions
from xml.xpath import ParsedToken
from xml.xpath import ParsedNodeTest
from xml.xpath import CoreFunctions, Conversions
from xml.xpath import Util
from xml.xpath import ParsedStep
from xml.xpath import ParsedAxisSpecifier
from xml.utils import boolean
import Set

g_printMap = {XPath.GREATER_THAN:'>',
              XPath.GREATER_THAN_EQUAL:'>=',
              XPath.LESS_THAN:'<',
              XPath.LESS_THAN_EQUAL:'<=',
              }

class NodeSet(UserList.UserList):
    def __init__(self, data=None):
        UserList.UserList.__init__(self, data or [])

    def __repr__(self):
        st = '<NodeSet at %x: [' % id(self)
        if len(self):
            for i in self[:-1]:
                st = st + repr(i) + ', '
            st = st + repr(self[-1])
        st = st + ']>'
        return st


class ParsedExpr(ParsedToken.ParsedToken):
    def __init__(self):
        ParsedToken.ParsedToken.__init__(self,"EXPRESSION")
    
    def evaluate(self, context):
        """What does this expression evaluate to in the given context
           Can return:  <boolean>
                        <number>
                        <string>
                        <node-set>
                       result-tree fragment
        """
        pass


class ParsedLiteralExpr(ParsedExpr):
    def __init__(self,literal):
        ParsedExpr.__init__(self)
        if len(literal) >= 2 and (
            literal[0] in ['\'', '"'] and
            literal[0] == literal[-1]):
            literal = string.strip(literal)[1:-1]
        self._literal = literal

    def evaluate(self, context):
        return self._literal

    def __repr__(self):
        return '"' + self._literal + '"'


class ParsedNLiteralExpr(ParsedLiteralExpr):
    def __init__(self,nliteral):
        ParsedLiteralExpr.__init__(self,"")
        self._nliteral = nliteral
        self._literal = float(nliteral)
    def __repr__(self):
        return str(self._nliteral)

from xml.xpath import RuntimeException, Error

class ParsedVariableReferenceExpr(ParsedExpr):
    def __init__(self,name):
        ParsedExpr.__init__(self)
        self._name = name
        self._key = SplitQName(name[1:])
        return

    def evaluate(self, context):
        """Returns a string"""
        (prefix, local) = self._key
        expanded = (prefix and context.processorNss.get(prefix) or '', local)
        try:
            return context.varBindings[expanded]
        except:
            raise RuntimeException(Error.UNDEFINED_VARIABLE,
                                   expanded[0], expanded[1])

    def __repr__(self):
        return self._name


def ParsedFunctionCallExpr(name, args):
    name = string.strip(name)
    key = SplitQName(name)
    count = len(args)
    if count == 0:
        return FunctionCall(name, key, args)
    if count == 1:
        return FunctionCall1(name, key, args)
    if count == 2:
        return FunctionCall2(name, key, args)
    if count == 3:
        return FunctionCall3(name, key, args)
    return FunctionCallN(name, key, args)


class FunctionCall(ParsedExpr):
    def __init__(self, name, key, args):
        ParsedExpr.__init__(self)
        self._name = name
        self._key = key
        self._args = args
        self._func = None

    def pprint(self, indent=''):
        print indent + str(self)
        for arg in self._args:
            arg.pprint(indent + '  ')

    def error(self, *args):
        raise Exception('Unknown function call: %s' % self._name)

    def evaluate(self, context):
        """Call the function"""
        if not self._func:
            (prefix, local) = self._key
            expanded = (prefix and context.processorNss.get(prefix) or '', local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        return self._func(context)

    def __getinitargs__(self):
        return (self._name, self._key, self._args)

    def __getstate__(self):
        state = vars(self).copy()
        del state['_func']
        return state
                    

    def __repr__(self):
        result = self._name + '('
        if len(self._args):
            result = result + repr(self._args[0])
            for arg in self._args[1:]:
                result = result + ', ' + repr(arg)
        return result + ')'
        

class FunctionCall1(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            expanded = (prefix and context.processorNss.get(prefix) or '', local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        return self._func(context, arg0)


class FunctionCall2(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            expanded = (prefix and context.processorNss.get(prefix) or '', local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        return self._func(context, arg0, arg1)


class FunctionCall3(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]
        self._arg2 = args[2]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        arg2 = self._arg2.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            expanded = (prefix and context.processorNss.get(prefix) or '', local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        return self._func(context, arg0, arg1, arg2)


class FunctionCallN(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)

    def evaluate(self, context):
        args = [context] + map(lambda x, c=context:
                               x.evaluate(c),
                               self._args)
        if not self._func:
            (prefix, local) = self._key
            expanded = (prefix and context.processorNss.get(prefix) or '', local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        return apply(self._func, args)


#Node Set Expressions
#These must return a node set

class ParsedUnionExpr(ParsedExpr):
    def __init__(self,left,right):
        ParsedExpr.__init__(self)
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        lSet = self._left.evaluate(context)
        if type(lSet) != type([]):
            raise "Left Expression does not evaluate to a node set"
        rSet = self._right.evaluate(context)
        if type(rSet) != type([]):
            raise "Right Expression does not evaluate to a node set"
        set = Set.Union(lSet, rSet)
        set = Util.SortDocOrder(set)
        return set

    def __repr__(self):
        return repr(self._left) + ' | ' + repr(self._right)


class ParsedPathExpr(ParsedExpr):
    def __init__(self, op, left, right):
        ParsedExpr.__init__(self)
        self._left = left
        self._right = right
        if op == XPath.DOUBLE_SLASH:
            nt = ParsedNodeTest.ParsedNodeTest(XPath.NODE, '')
            axis = ParsedAxisSpecifier.ParsedAxisSpecifier(XPath.DESCENDANT_OR_SELF)
            from xml.xpath import ParsedPredicateList
            pList = ParsedPredicateList.ParsedPredicateList([])
            self._step = ParsedStep.ParsedStep(axis, nt, pList)
        else:
            self._step = None

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        """Evaluate the left, then if op =// the parsedStep, then the right, push context each time"""
        """Returns a node set"""

        rt = self._left.evaluate(context)
        if type(rt) != type([]):
            raise "Invalid Expression for a PathExpr %s" % str(self._left)

        origState = context.copyNodePosSize()
        if self._step:
            res = []
            l = len(rt)
            for ctr in range(l):
                r = rt[ctr]
                context.setNodePosSize((r,ctr+1,l))
                subRt = self._step.select(context)
                res = Set.Union(res,subRt)
            rt = res
        res = []
        l = len(rt)
        for ctr in range(l):
            r = rt[ctr]
            context.setNodePosSize((r,ctr+1,l))
            subRt = self._right.select(context)
            if type(subRt) != type([]):
                raise Exception("Right Expression does not evaluate to a Node Set")
            res = Set.Union(res,subRt)

        context.setNodePosSize(origState)
        return res

    def __repr__(self):
        op = self._step and '//' or '/'
        return repr(self._left) + op + repr(self._right)


class ParsedFilterExpr(ParsedExpr):
    def __init__(self,filter,pred):
        ParsedExpr.__init__(self)
        self._filter = filter
        self._pred = pred

    def evaluate(self, context):
        """Evaluate our filter into a node set, filter that through the predicate"""
        """Returns a node-set"""
        rt = self._filter.evaluate(context)
        if type(rt) != type([]):
            raise "ParsedFilterExpr: return value must evalute to a node-set"

        length = len(rt)
        result = []
        for ctr in range(length):
            context.setNodePosSize((rt[ctr],ctr+1,length))
            if Conversions.BooleanEvaluate(self._pred, context):
                result.append(rt[ctr])

        return result

    def pprint(self, indent=''):
        print indent + str(self)
        self._filter.pprint(indent + '  ')
        self._pred.pprint(indent + '  ')

    def shiftContext(self,context,index,set,len,func):
        return func(context)

    def __repr__(self):
        return repr(self._filter) + '[' + repr(self._pred) + ']'

#Boolean Expressions
#All will return a boolean value

class ParsedOrExpr(ParsedExpr):
    def __init__(self, left, right):
        ParsedExpr.__init__(self)
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        rt = Conversions.BooleanEvaluate(self._left, context)
        if not rt:
            rt = Conversions.BooleanEvaluate(self._right, context)
        return rt

    def __repr__(self):
        return repr(self._left) +' or ' + repr(self._right)


class ParsedAndExpr(ParsedExpr):
    def __init__(self,left,right):
        ParsedExpr.__init__(self)
        self._left = left
        self._right = right

    def evaluate(self, context):
        rt = Conversions.BooleanEvaluate(self._left, context)
        if rt:
            rt = Conversions.BooleanEvaluate(self._right, context)
        return rt

    def __repr__(self):
        return repr(self._left) + ' and ' + repr(self._right)

NumberTypes = [types.IntType, types.FloatType, types.LongType]

class ParsedEqualityExpr(ParsedExpr):
    def __init__(self, op, left, right):
        ParsedExpr.__init__(self)
        self._op = op
        self._left = left
        self._right = right

    def evaluate(self, context):
        if self._op == '=':
            true = boolean.true
            false = boolean.false
        else:
            true = boolean.false
            false = boolean.true

        lrt = self._left.evaluate(context)
        rrt = self._right.evaluate(context)
        lType = type(lrt)
        rType = type(rrt)
        if lType == types.ListType == rType:
            #Node set to node set
            for right_curr in rrt:
                right_curr = Conversions.StringValue(right_curr)
                for left_curr in lrt:
                    if right_curr == Conversions.StringValue(left_curr):
                        return true
            return false
        elif lType == types.ListType or rType == types.ListType:
            func = None
            if lType == types.ListType:
                set = lrt
                val = rrt
            else:
                set = rrt
                val = lrt
            if type(val) in NumberTypes:
                func = Conversions.NumberValue
            elif boolean.IsBooleanType(val):
                func = Conversions.BooleanValue
            elif type(val) == types.StringType:
                func = Conversions.StringValue
            else:
                #Deal with e.g. RTFs
                val = Conversions.StringValue(val)
                func = Conversions.StringValue
            for n in set:
                if func(n) == val:
                    return true
            return false

        if boolean.IsBooleanType(lrt) or boolean.IsBooleanType(rrt):
            rt = Conversions.BooleanValue(lrt) == Conversions.BooleanValue(rrt)
        elif lType in NumberTypes or rType in NumberTypes:
            rt = Conversions.NumberValue(lrt) == Conversions.NumberValue(rrt)
        else:
            rt = Conversions.StringValue(lrt) == Conversions.StringValue(rrt)
        if rt:
            # Due to the swapping of true/false, true might evaluate to 0
            # We cannot compact this to 'rt and true or false'
            return true
        return false
        
    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __repr__(self):
        if self._op == '=':
            op = ' = '
        else:
            op = ' != '
        return repr(self._left) + op + repr(self._right)



class ParsedRelationalExpr(ParsedExpr):
    def __init__(self, op, left, right):
        ParsedExpr.__init__(self)
        if not op in [XPath.LESS_THAN,
                      XPath.LESS_THAN_EQUAL,
                      XPath.GREATER_THAN,
                      XPath.GREATER_THAN_EQUAL
                      ]:
            raise Exception('Invalid operand for RelationalExpr:' + str(op))
        self._op = op

        if isinstance(left, ParsedLiteralExpr):
            self._left = Conversions.NumberValue(left.evaluate(None))
            self._leftLit = 1
        else:
            self._left = left
            self._leftLit = 0

        if isinstance(right, ParsedLiteralExpr):
            self._right = Conversions.NumberValue(right.evaluate(None))
            self._rightLit = 1
        else:
            self._right = right
            self._rightLit = 0

    def evaluate(self, context):
        if self._leftLit:
            lrt = self._left
        else:
            lrt = Conversions.NumberValue(self._left.evaluate(context))
        if self._rightLit:
            rrt = self._right
        else:
            rrt = Conversions.NumberValue(self._right.evaluate(context))

        if self._op == XPath.LESS_THAN:
            rt = (lrt < rrt)
        elif self._op == XPath.LESS_THAN_EQUAL:
            rt = (lrt <= rrt)
        elif self._op == XPath.GREATER_THAN:
            rt = (lrt > rrt)
        elif self._op == XPath.GREATER_THAN_EQUAL:
            rt = (lrt >= rrt)
        return rt and boolean.true or boolean.false

    def __repr__(self):
        # Calling __repr__ directly avoids additional quotes on return value
        op = ' %s ' % g_printMap[self._op]
        return repr(self._left) + op + repr(self._right)

#Number Expressions


class ParsedAdditiveExpr(ParsedExpr):
    def __init__(self, op, left, right):
        ParsedExpr.__init__(self)
        self._op = op
        self._leftLit = 0
        self._rightLit = 0
        if isinstance(left, ParsedLiteralExpr):
            self._leftLit = 1
            self._left = Conversions.NumberValue(left.evaluate(None))
        else:
            self._left = left
        if isinstance(right, ParsedLiteralExpr):
            self._rightLit = 1
            self._right = Conversions.NumberValue(right.evaluate(None))
        else:
            self._right = right
        return

    def evaluate(self, context):
        '''returns a number'''
        if self._leftLit:
            lrt = self._left
        else:
            lrt = self._left.evaluate(context)
            lrt = Conversions.NumberValue(lrt)
        if self._rightLit:
            rrt = self._right
        else:
            rrt = self._right.evaluate(context)
            rrt = Conversions.NumberValue(rrt)
        if self._op == '+':
            rt = lrt + rrt
        elif self._op == '-':
            rt = lrt - rrt
        return rt

    def __repr__(self):
        op = ' ' + str(self._op) + ' '
        return repr(self._left) + op + repr(self._right)


from xml.xpath import Inf, NaN

class ParsedMultiplicativeExpr(ParsedExpr):
    def __init__(self, operator, left, right):
        ParsedExpr.__init__(self)
        self._op = operator
        self._left = left
        self._right = right

    def evaluate(self, context):
        '''returns a number'''
        lrt = self._left.evaluate(context)
        lrt = Conversions.NumberValue(lrt)
        rrt = self._right.evaluate(context)
        rrt = Conversions.NumberValue(rrt)
        res = 0
        if self._op == XPath.MULTIPLY_OPERATOR:
            res = lrt * rrt
        elif self._op == XPath.DIV:
            if rrt == 0:
                res = NaN
            else:
                res = lrt / rrt
        elif self._op == XPath.MOD:
            if rrt == 0:
                res = NaN
            else:
                res = lrt % rrt
        return res

    def __repr__(self):
        if self._op == XPath.DIV:
            op = ' div '
        elif self._op == XPath.MOD:
            op = ' mod '
        else:
            op = ' * '
        return repr(self._left) + op + repr(self._right)

class ParsedUnaryExpr(ParsedExpr):
    def __init__(self,exp):
        ParsedExpr.__init__(self)
        self._exp = exp

    def evaluate(self, context):
        '''returns a number'''
        exp = self._exp.evaluate(context)
        exp = Conversions.NumberValue(exp)
        rt = exp * -1.0
        return rt

    def __repr__(self):
        return '-' + repr(self._exp)
