# Parser for XPath in -*- python -*-, as defined in REC-xpath-19991116
# Copyright 2000, Martin v. Löwis

# This parser is generated by Amit J Patel's YAPPS
# http://theory.stanford.edu/~amitp/Yapps/ for documentation and updates
    
# The generated Scanner class is not used, and redefined at the end.
# Therefore, the token definitions are for illustration only, and to
# let YAPPS know what the tokens are.

# The grammar rules attempt to follow the XPath recommendation closely,
# both in textual order and presentation. The following changes have been
# made:
# - left-recursion was replaced with right-recursion
# - left-factorization was applied where necessary
# - semantic values were attached to non-terminals
%%
parser XPath:
    option: "context-insensitive-scanner"
    token Literal: '"[^"]*"|\'[^\']*'
    token Number: "\\d+(.\\d*)?|.\\d+"
    token VariableReference: '\\$[a-zA-Z_][:a-zA-Z0-9_.-]*'
    token NodeType: 'comment|text|processing-instruction|node'
    token AxisName: 'ancestor|ancestor-or-self|attribute|child|descendant|descendant-or-self|following|following-sibling|namespace|parent|preceding|preceding-sibling|self'
    token NCName: '[a-zA-Z_][a-zA-Z0-9_.-]*'
    token NCNameStar: '[a-zA-Z_][a-zA-Z0-9_.-]*:\*'
    token QName: '[a-zA-Z_][a-zA-Z0-9_.-]*(:[a-zA-Z_][a-zA-Z0-9_.-])?'
    token MultiplyOperator: '\\*'
    token LPAREN: '\\('
    token RPAREN: '\\)'
    token STAR: '\\*'
    token PLUS: '\\+'
    token LBRACKET: '\\['
    token RBRACKET: '\\]'
    token FunctionName: '[a-zA-Z_][a-zA-Z0-9_.-]*(:[a-zA-Z_][a-zA-Z0-9_.-]*)?'
    token DOT: '\\.'
    token DOTDOT: '\\.\\.'
    token BAR: '\\|'
    token END: '#'
    #XSLT
    token ID: 'id'
    token KEY: 'key'

    rule Start:
        LocationPath END   {{return LocationPath}}

    rule FullExpr:
        Expr END   {{return Expr}}

    rule LocationPath:
        RelativeLocationPath                        {{return RelativeLocationPath}}
        | AbsoluteLocationPath                      {{return AbsoluteLocationPath}}

    rule AbsoluteLocationPath:
        '/' OptRelativeLocationPath
                  {{return self.absoluteLocationPath(OptRelativeLocationPath)}}
        | AbbreviatedAbsoluteLocationPath
                  {{return AbbreviatedAbsoluteLocationPath}}
    rule OptRelativeLocationPath:
          {{return None}}
        | RelativeLocationPath   {{return RelativeLocationPath}}

    rule RelativeLocationPath:
        Step RelativeLocationPaths<<Step>>       {{return RelativeLocationPaths}}
    rule RelativeLocationPaths<<v>>:
          {{return v}}
        | '/' Step RelativeLocationPaths<<self.rlp(v,Step)>>     {{return RelativeLocationPaths}}
        | '//' Step RelativeLocationPaths<<self.arlp(v,Step)>>    {{return RelativeLocationPaths}}
    
    rule Step:
        AxisSpecifier NodeTest Predicates
                  {{return self.step(AxisSpecifier,NodeTest,Predicates)}}
        | AbbreviatedStep
                  {{return AbbreviatedStep}}
    rule Predicates:
          {{return []}}
        | Predicate Predicates   {{return [Predicate]+Predicates}}

    rule AxisSpecifier:
        AxisName '::'                     {{return self.axisSpecifier(self.anMap[AxisName])}}
        | AbbreviatedAxisSpecifier        {{return AbbreviatedAxisSpecifier}}

    rule NodeTest:
        NameTest                               {{return NameTest}}
        | NodeType LPAREN OptLiteral RPAREN    {{return self.mkNodeTest(NodeType,OptLiteral)}}
    rule OptLiteral:
          {{return None}}
        | Literal   {{return Literal}}

    rule NameTest:
        STAR              {{return self.nameTest(None,"*")}}
	| QName           {{return self.mkQName(QName)}}
        | NCNameStar      {{return self.nameTest(NCNameStar[:-2],'*')}}
        | NCName          {{return self.nameTest(None,NCName)}}

    rule Predicate: LBRACKET PredicateExpr RBRACKET   {{return PredicateExpr}}

    rule PredicateExpr:  Expr   {{return Expr}}

    rule AbbreviatedAbsoluteLocationPath:
        '//' RelativeLocationPath    {{return self.aalp(RelativeLocationPath)}}

    rule AbbreviatedStep:
        DOT               {{return self.abbreviatedStep(0)}}
        | DOTDOT          {{return self.abbreviatedStep(1)}}

    rule AbbreviatedAxisSpecifier:
          {{return self.axisSpecifier(pyxpath.CHILD_AXIS)}}
        |'@'   {{return self.axisSpecifier(pyxpath.ATTRIBUTE_AXIS)}}

    rule Expr: OrExpr    {{return OrExpr}}

    rule PrimaryExpr:
        VariableReference    {{return self.mkVariableReference(VariableReference)}}
        | LPAREN Expr RPAREN       {{return Expr}}
        | Literal   {{return self.literal(Literal)}}
        | Number   {{return self.number(Number)}}
        | FunctionCall   {{return FunctionCall}}

    rule FunctionCall:
        FunctionName LPAREN Arguments RPAREN
                  {{return self.mkFunctionCall(FunctionName,Arguments)}}
        | ID LPAREN Arguments RPAREN
                  {{return self.functionCall(None,'id',Arguments)}}
        | KEY LPAREN Arguments RPAREN
                  {{return self.functionCall(None,'key',Arguments)}}

    rule Arguments:
          {{return []}}
        | Argument KommaArguments<<[Argument]>>   {{return KommaArguments}}
    rule KommaArguments<<v>>:
          {{return v}}
        | ',' Argument KommaArguments<<v+[Argument]>>   {{return KommaArguments}}

    rule Argument: Expr   {{return Expr}}

    rule UnionExpr:
        PathExpr UnionExprs<<PathExpr>>   {{return UnionExprs}}
    rule UnionExprs<<v>>:
           {{return v}}
        | BAR PathExpr UnionExprs<<self.nop(self.UNION,v,PathExpr)>>    {{return UnionExprs}}

    rule PathExpr:
        LocationPath   {{return LocationPath}}
        | FilterExpr PathExprRest<<FilterExpr>>   {{return PathExprRest}}
    rule PathExprRest<<v>>:
          {{return v}}
        | '/' RelativeLocationPath   {{return self.pathExpr(v,RelativeLocationPath)}}
        | '//' RelativeLocationPath   {{return self.abbreviatedPathExpr(v,RelativeLocationPath)}}
        
    rule FilterExpr:
        PrimaryExpr FilterExprs<<PrimaryExpr>>   {{return FilterExprs}}
    rule FilterExprs<<v>>:
          {{return v}}
        | Predicate FilterExprs<<self.filterExpr(v,Predicate)>>   {{return FilterExprs}}

    rule OrExpr:
        AndExpr OrExprs<<AndExpr>>   {{return OrExprs}}
    rule OrExprs<<v>>:
        'or' AndExpr OrExprs<<self.bop(self.OR,v,AndExpr)>>   {{return OrExprs}}
        |   {{return v}}

    rule AndExpr:
        EqualityExpr AndExprs<<EqualityExpr>>   {{return AndExprs}}
    rule AndExprs<<v>>:
        'and' EqualityExpr AndExprs<<self.bop(self.AND,v,EqualityExpr)>>    {{return AndExprs}}
        |   {{return v}}

    rule EqualityExpr:
        RelationalExpr EqualityExprs<<RelationalExpr>>   {{return EqualityExprs}}
    rule EqualityExprs<<v>>:
          '=' RelationalExpr EqualityExprs<<self.bop(self.EQ,v,RelationalExpr)>>
                  {{return EqualityExprs}}
        | '!=' RelationalExpr EqualityExprs<<self.bop(self.NE,v,RelationalExpr)>>
                  {{return EqualityExprs}}
        |   {{return v}}

    rule RelationalExpr:
        AdditiveExpr RelationalExprs<<AdditiveExpr>>   {{return RelationalExprs}}
    rule RelationalExprs<<v>>:
          '<' AdditiveExpr RelationalExprs<<self.bop(self.LT,v,AdditiveExpr)>>
                  {{return RelationalExprs}}
        | '<=' AdditiveExpr RelationalExprs<<self.bop(self.LE,v,AdditiveExpr)>>
                  {{return RelationalExprs}}
        | '>' AdditiveExpr RelationalExprs<<self.bop(self.GT,v,AdditiveExpr)>>
                  {{return RelationalExprs}}
        | '>=' AdditiveExpr RelationalExprs<<self.bop(self.GE,v,AdditiveExpr)>>
                  {{return RelationalExprs}}
        |   {{return v}}

    rule AdditiveExpr:
        MultiplicativeExpr AdditiveExprs<<MultiplicativeExpr>>   {{return AdditiveExprs}}
    rule AdditiveExprs<<v>>:
          PLUS MultiplicativeExpr AdditiveExprs<<self.nop(self.PLUS,v,MultiplicativeExpr)>>
                  {{return AdditiveExprs}}
        | '-' MultiplicativeExpr AdditiveExprs<<self.nop(self.MINUS,v,MultiplicativeExpr)>>
                  {{return AdditiveExprs}}
        |   {{return v}}

    rule MultiplicativeExpr:
        UnaryExpr MultiplicativeExprs<<UnaryExpr>>   {{return MultiplicativeExprs}}
    rule MultiplicativeExprs<<v>>:
          MultiplyOperator UnaryExpr MultiplicativeExprs<<self.nop(self.TIMES,v,UnaryExpr)>>
                  {{return MultiplicativeExprs}}
        | 'div' UnaryExpr MultiplicativeExprs<<self.nop(self.DIV,v,UnaryExpr)>>
                  {{return MultiplicativeExprs}}
        | 'mod' UnaryExpr MultiplicativeExprs<<self.nop(self.MOD,v,UnaryExpr)>>
                  {{return MultiplicativeExprs}}
        |   {{return v}}

    rule UnaryExpr:
        '-' UnaryExpr   {{return self.unaryExpr(UnaryExpr)}}
        | UnionExpr   {{return UnionExpr}}

    #XSLT patterns
    rule FullPattern:
        Pattern END             {{return Pattern}}

    rule Pattern:
        LocationPathPattern     {{p = self.pattern(LocationPathPattern)}}
        ( BAR LocationPathPattern
                {{p.append(LocationPathPattern)}}
        )*
        {{return p}}

    rule LocationPathPattern:
          '/' OptRelativePathPattern
                {{return self.locationPathPattern(None,1,OptRelativePathPattern)}}
        | IdKeyPattern IdTail
                {{return self.locationPathPattern(IdKeyPattern,IdTail[0],IdTail[1])}}
        | RelativePathPattern
                {{return RelativePathPattern}}
        | '//' RelativePathPattern
                {{return self.locationPathPattern(None,0,RelativePathPattern)}}
    rule OptRelativePathPattern:
                                {{return None}}
        | RelativePathPattern   {{return RelativePathPattern}}
    rule IdTail:
                                        {{return (0,None)}}
        | '/' RelativePathPattern       {{return (1,RelativePathPattern)}}
        | '//' RelativePathPattern      {{return (0,RelativePathPattern)}}

    rule IdKeyPattern:
        ID LPAREN Argument RPAREN
                {{ return self.functionCall(None,"id", [Argument])}}
        | KEY LPAREN Argument {{a1=Argument}} ',' Argument RPAREN
                {{ return self.functionCall(None,"key", [a1,Argument])}}

    rule RelativePathPattern:
        StepPattern       {{p=StepPattern}}
        (('/' StepPattern {{p=self.rpp(p, 1, StepPattern)}}    )
         |('//' StepPattern {{p=self.rpp(p, 0, StepPattern)}} )
        )*
        {{return p}}

    rule StepPattern:
        ChildOrAttributeAxisSpecifier NodeTest
        {{pred=[]}} (Predicate {{pred.append(Predicate)}} )*
        {{return self.stepPattern(ChildOrAttributeAxisSpecifier,NodeTest,pred)}}
        
    rule ChildOrAttributeAxisSpecifier:
        AbbreviatedAxisSpecifier
                {{return AbbreviatedAxisSpecifier}}
        | AxisName '::'
                {{return self.axisSpecifier(self.anMap[AxisName])}}

%%

# Reimplement scanner, to properly use disambiguation
import re, sys
NCName = "[a-zA-Z_](\w|[_.-])*"
# In this version of QName, the namespace prefix is not optional.
# As a result, QName matches iff there is a colon, NCName otherwise.
# All appearances of QName in the grammar then need to allow NCName
# as an alternative; currently, QName is used only once.
QName = NCName + ":" + NCName
XPathExpr="""
  (?P<Literal>\"[^\"]*\"|\'[^\']*\')|
  (?P<Number>\\d+(\\.\\d*)?|\\.\\d+)|
  (?P<VariableReference>\\$""" + NCName + "(:" + NCName + """)?)|
  (?P<QName>"""+QName+""")|
  (?P<NCNameStar>"""+NCName+""":\*)|
  (?P<NCName>"""+NCName+""")|
  (?P<LPAREN>\\()|
  (?P<RPAREN>\\))|
  (?P<STAR>\\*)|
  (?P<PLUS>\\+)|
  (?P<LBRACKET>\\[)|
  (?P<RBRACKET>\\])|
  (?P<DOTDOT>\\.\\.)|
  (?P<DOT>\\.)|
  (?P<BAR>\\|)|
  (?P<Operator>//|::|>=|<=|!=)|
  (?P<SingleOperator>[<>=,/@:-])|
  (?P<ExprWhiteSpace>[ \t\n\r]+)
"""

_xpath_exp = re.compile(XPathExpr,re.VERBOSE)

OperatorName = ['and','or','mod','div']
AxisName = ['ancestor', 'ancestor-or-self', 'attribute', 'child',
            'descendant', 'descendant-or-self', 'following',
            'following-sibling', 'namespace', 'parent', 'preceding',
            'preceding-sibling', 'self']

SpecialPreceding = map(repr,["@","::","(","["] + OperatorName + ['/', '//', '+', '-', '=', '!=', '<', '<=', '>', '>=']) + ["BAR","MultiplyOperator"]

if sys.hexversion > 0x2000000:
    def _get_type(match):
        return match.lastgroup,match.group()
else:
    def _get_type(match):
        type = val = None
        for t,v in match.groupdict().items():
            if v is None: continue
            if val:
                raise SyntaxError(pos,
                                  "ambiguity:%s could be %s or %s" % (val,type,t))
            type = t
            val = v
        return type,val
        
        

class XPathScanner:
    def __init__(self,input):
        self.tokens = tokens = []

        pos = 0

        # Process all tokens, advancing pos for each one
        while pos != len(input):
            m = _xpath_exp.match(input, pos)
            if not m:
                msg = "Bad Token"
                raise SyntaxError(pos, msg)

            type, val = _get_type(m)
            if type == "ExprWhiteSpace":
                # If we got white space, ignore it
                pos = pos + len(val)
                continue

            if type in ['SingleOperator', 'Operator']:
                type = repr(str(val))
            start = pos
            pos = pos + len(val)
            tokens.append((start, pos, type, val))
            
        # If we are at the end of the string, add END token
        tokens.append((pos,pos,'END',""))

        # Adjust token type according to additional semantic rules

        for i in range(len(tokens)-1):
            start,stop,type,val = tokens[i]
            changed = 0
            # If there is a preceding token and the preceding token is not
            # one of @, ::, (, [, , or an Operator
            if i>=1 and tokens[i-1][2] not in SpecialPreceding:
                if type == 'STAR':
                    #  then a * must be recognized as a MultiplyOperator
                    type = 'MultiplyOperator'
                    tokens[i] = (start,stop,type,val)
                elif type == 'NCName' and val in OperatorName:
                    # and an NCName must be recognized as an OperatorName
                    type = repr(str(val))
                    tokens[i] = (start,stop,type,val)
            # If the character following an NCName (possibly after
            # intervening ExprWhitespace) is (
            if tokens[i][2] in ['QName','NCName'] and tokens[i+1][2]=='LPAREN':
                # then the token must be recognized as a NodeType or a
                # FunctionName
                if val in ['comment','text','processing-instruction','node']:
                    type = 'NodeType'
                elif val == 'id':
                    type = 'ID'
                elif val == 'key':
                    type = 'KEY'
                else:
                    type = 'FunctionName'
                tokens[i] = (start,stop,type,val)

            # If the two characters following an NCName (possibly
            # after intervening ExprWhitespace) are ::
            if tokens[i][2] == 'NCName' and tokens[i+1][3]=='::' \
               and val in AxisName:
                # then the token must be recognized as an AxisName.
                type = 'AxisName'
                tokens[i] = (start,stop,type,val)

    def token(self, i, expected):
        return self.tokens[i]

# redefine to add additional attributes
import pyxpath,string
GeneratedXPath = XPath
class XPath(GeneratedXPath):
    OR = pyxpath.OR_OPERATOR
    AND = pyxpath.AND_OPERATOR
    EQ = pyxpath.EQ_OPERATOR
    NEQ = pyxpath.NEQ_OPERATOR
    LT = pyxpath.LT_OPERATOR
    GT = pyxpath.GT_OPERATOR
    LE = pyxpath.LE_OPERATOR
    GE = pyxpath.GE_OPERATOR
    PLUS = pyxpath.PLUS_OPERATOR
    MINUS = pyxpath.MINUS_OPERATOR
    TIMES = pyxpath.TIMES_OPERATOR
    DIV = pyxpath.DIV_OPERATOR
    MOD = pyxpath.MOD_OPERATOR
    UNION = pyxpath.UNION_OPERATOR

    def __init__(self, scanner, factory):
        GeneratedXPath.__init__(self, scanner)
        self.factory = factory
        # shorthands
        self.rlp = self.factory.createRelativeLocationPath
        self.arlp = self.factory.createAbbreviatedRelativeLocationPath
        self.aalp = self.factory.createAbbreviatedAbsoluteLocationPath

        self.nop = self.factory.createNumericExpr
        self.bop = self.factory.createBooleanExpr

        self.rpp = self.factory.createRelativePathPattern
        
    def __getattr__(self, name):
        # convert 
        newname = "create"+string.upper(name[0])+name[1:]
        try:
            return getattr(self.factory, newname)
        except AttributeError:
            raise AttributeError,"parser has no attribute "+name

    anMap = {
        'ancestor':pyxpath.ANCESTOR_AXIS,
        'ancestor-or-self':pyxpath.ANCESTOR_OR_SELF_AXIS,
        'attribute':pyxpath.ATTRIBUTE_AXIS,
        'child':pyxpath.CHILD_AXIS,
        'descendant':pyxpath.DESCENDANT_AXIS,
        'descendant-or-self':pyxpath.DESCENDANT_OR_SELF_AXIS,
        'following':pyxpath.FOLLOWING_AXIS,
        'following-sibling':pyxpath.FOLLOWING_SIBLING_AXIS,
        'namespace':pyxpath.NAMESPACE_AXIS,
        'parent':pyxpath.PARENT_AXIS,
        'preceding':pyxpath.PRECEDING_AXIS,
        'preceding-sibling':pyxpath.PRECEDING_SIBLING_AXIS,
        'self':pyxpath.SELF_AXIS
        }

    
    nodeTestMap = {
        'node': pyxpath.NODE,
        'comment': pyxpath.COMMENT,
        'text': pyxpath.TEXT,
        'processing-instruction': pyxpath.PROCESSING_INSTRUCTION
        }
    def mkNodeTest(self,op,val):
        type = self.nodeTestMap[op]
        if type != pyxpath.PROCESSING_INSTRUCTION and val is not None:
                raise SyntaxError("parameter not allowed for "+op)
        return self.factory.createNodeTest(type,val)

    def mkQName(self,str):
        prefix,local = string.split(str,":")
        return self.factory.createNameTest(prefix,local)

    def mkVariableReference(self, qname):
        colon = string.find(qname,':')
        if colon == -1:
            return self.variableReference(None, qname[1:])
        return self.variableReference(qname[1:colon],qname[colon+1:])

    def mkFunctionCall(self, qname, args):
        colon = string.find(qname,':')
        if colon == -1:
            return self.functionCall(None, qname, args)
        return self.functionCall(qname[:colon],qname[colon+1:],args)