'''HTML parser, built from standard lib's sgmllib.

Tag names are normalised to upper case, the usual HTML fashion.
'''

from sgmllib import SGMLParser
from xml.dom import core
from xml.dom.builder import Builder
import string

BadHTMLError = "Bad HTML error"

class HtmlBuilder(SGMLParser, Builder):
    from htmlentitydefs import entitydefs
    
    def __init__(self, ignore_mismatched_end_tags = 0):
        """HtmlBuilder constructor:
        ignore_mismatched_end_tags -- Boolean; if true, ending tags without
                                      a corresponding start tag are ignored.
        """
        SGMLParser.__init__(self)
        Builder.__init__(self)

        # Save the option settings
        self.ignore_mismatched_end_tags = ignore_mismatched_end_tags 

        self.empties = [
            'META', 'BASE', 'LINK', 
            'HR', 'BR',
            'IMG', 'PARAM',
            'INPUT', 'OPTION', 'ISINDEX'
        ]
        list = ('OL', 'UL', 'DL')
        heading = ('H1', 'H2', 'H3', 'H4', 'H5', 'H6')
        blocks = ('P', 'ADDRESS', 'BLOCKQUOTE', 'FORM', 'TABLE', 'PRE') + \
            heading # + list
        self.infer_ends = {
            'P': blocks,

            'LI': ('LI',),
            'DT': ('DT',),
            'DD': ('DT', 'DD'),

            'TR': ('TR',), 
            'TH': ('TH', 'TD', 'TR'),
            'TD': ('TH', 'TD', 'TR'),
        }

        # Names of entities that will be converted to their character
        # representation.  Entities not listed here will be left as 
        # entity references.
        self.expand_entities = ('lt', 'gt', 'apos', 'quot')
    
    def unknown_starttag(self, tag, attrs):
        tag = string.upper(tag)
        #print 'starting', tag
        attributes = {}
        for k, v in attrs:
            attributes[string.upper(k)] = v

        #print self.stack
        while self.stack:
            if self.infer_ends.has_key(self.stack[-1]): 
                if tag in self.infer_ends[self.stack[-1]]:
                    #print tag, 'ending', self.stack[-1]
                    Builder.endElement(self, self.stack[-1])
                    del self.stack[-1]
                    #print self.stack
                else:
                    break
            else:
                break
#        print self.stack, tag, attributes
        
        Builder.startElement(self, tag, attributes)
        if not tag in self.empties:
            self.stack.append(tag)
        else:
            Builder.endElement(self, tag)


    def unknown_endtag(self, tag):
        tag = string.upper(tag)
        #print 'ending', tag

        if tag not in self.stack:
            if self.ignore_mismatched_end_tags:
                #print "ignoring end tag with no start", tag
                return
            else:
                raise BadHTMLError, ("End tag </%s> without start tag" %(tag,))

        while self.stack:
            if tag in self.empties:
                continue
            start_tag = self.stack[-1]
            del self.stack[-1]
            Builder.endElement(self, start_tag)
            if start_tag == tag:
                break

    def unknown_charref(self, ref):
        raise BadHTMLError, ('Unknown character reference: &#' + ref + ';')

    def handle_data(self, s):
        #print `s`
        Builder.text(self, s)

    def handle_comment(self, s):
        Builder.comment(self, s)

    def handle_entityref(self, name):
        table = self.entitydefs
        if name in self.expand_entities and table.has_key(name):
            self.handle_data(table[name])
        else:
            Builder.entityref(self, name)

# Test.
if __name__ == '__main__':
    import sys
    b = HtmlBuilder()
    b.feed(open(sys.argv[1]).read())
    b.close()
#    print b.document
#    print b.document.documentElement

    from writer import HtmlLineariser
    w = HtmlLineariser()
    print w.linearise(b.document)

