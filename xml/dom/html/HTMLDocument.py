########################################################################
#
# File Name:            HTMLDocument.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLDocument.py.html
#
# History:
# $Log: HTMLDocument.py,v $
# Revision 1.1  2000/06/06 01:36:07  amkcvs
# Added 4DOM code as provided; I haven't tested it to see if something
#    broke in the process.
#
# Revision 1.37  2000/05/24 18:14:48  molson
# Fixed tab errors
#
# Revision 1.36  2000/05/06 09:12:18  jkloth
# fixed problems with allowed children on HTML elements
#
# Revision 1.35  2000/05/05 02:48:26  pweinstein
# ...
#
# Revision 1.33  2000/05/04 01:24:07  pweinstein
# changing xml.dom.Html to xml.dom.html
#
# Revision 1.32  2000/05/03 23:38:15  pweinstein
# Migration to xml.doc, but still xml.doc.Html, pre-w3 conformance check
#
# Revision 1.31  2000/04/27 19:08:49  jkloth
# fixed imports for xml-sig
#
# Revision 1.30  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.29  2000/01/25 07:56:17  uche
# Fix DOM Namespace compliance & update XPath and XSLT accordingly.
# More Error checks in XSLT.
# Add i18n hooks.
#
# Revision 1.28  1999/12/15 04:18:21  uche
# Fixes to HTML Properties
# Update XSLT test suite
# Many bug fixes
#
# Revision 1.27  1999/12/10 02:19:31  molson
# Fixed some bugs in Html
#
# Revision 1.26  1999/12/04 19:31:17  uche
# Completed update to latest Python/DOM so that it goes through HTML test suite.
#
# Revision 1.25  1999/12/03 23:14:00  uche
# More Python/DOM binding updates.
#
# Revision 1.24  1999/12/03 17:52:09  uche
# Complete first pass of new Python/DOM conersion for HTML
# Normalize staging scripts and rename from 'promote' to 'stage'
#
# Revision 1.23  1999/12/02 20:39:59  uche
# More changes to conform to new Python/DOM binding.
#
# Revision 1.22  1999/09/26 00:14:31  uche
# Added the reader ext module to supersede Builder.  Made the appropriate conversions to other 4Suite components.
#
# Revision 1.21  1999/09/09 05:40:33  molson
# Implemented Core Level 2.  Tested in all three makes
#
# Revision 1.20  1999/08/31 21:02:16  molson
# Fixed to work over ilu orb
#
# Revision 1.19  1999/08/29 04:08:00  uche
# Added headers to 4DOM
# Added COPYRIGHT files
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Document import Document
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom import ext
import string

rwattrs = ('title','referrer','domain','URL','body','cookie',)
rattrs = ('images','applets','links','forms','anchors',)

class HTMLDocument(Document):

    def __init__(self):
        Document.__init__(self, None)
    #Some init stuff
        self.__dict__['referrer'] = ''
        self.__dict__['domain'] = ''
        self.__dict__['URL'] = ''
        self.__dict__['cookie'] = ''
        self.__dict__['writable'] = 0
        self.__dict__['htmlModules'] = __import__('xml.dom.html').dom.html
        self.__dict__['_4dom_isNsAware'] = 0

    def _get_title(self):
        title = ''
        nl = self.getElementsByTagName('TITLE')
        if nl.length:
            #Take the first
            title = nl[0]
            title.normalize()
            #Get first text node
            for child in title.childNodes:
                if child.nodeType == Node.TEXT_NODE:
                    title = child.data
        return title

    def _set_title(self, title):
        #See if we can find the title
        nl = self.getElementsByTagName('TITLE')
        #We will replace the title node with a new title
        text = self.createTextNode(title)
        title_node = self.createElement('Title')
        tn = self.createTextNode(title)
        title_node.appendChild(tn)
        if nl.length == 0:
            #Try and find a HEAD
            self.__get_head().appendChild(title_node)
        else:
            #Replace with new text
            nl[0].parentNode.replaceChild(title_node, nl[0])

    def _get_referrer(self):
        return self.referrer

    def _set_referrer(self, referrer):
        self.__dict__['referrer'] = referrer

    def _get_domain(self):
        return self.domain

    def _set_domain(self, domain):
        self.__dict__['domain'] = domain

    def _get_URL(self):
        return self.URL

    def _set_URL(self, url):
        self.__dict__['URL'] = url

    def _get_body(self):
        body = ''
        #Try to find the body or FRAMESET
        nl = self.getElementsByTagName('BODY')
        if nl:
            body = nl[0]
        else:
            nl = self.getElementsByTagName('FRAMESET')
            if nl: body = nl[0]
        if not body:
            #Create a body
            body = self.createElement('BODY')
            self.documentElement.appendChild(body)
        return body

    def _set_body(self, body):
        targetName = body.tagName
        if not targetName in ['BODY','FRAMESET']:
            targetName = 'BODY'
        nl = self.getElementsByTagName(targetName)
        if nl:
            #Replace with the given body
            nl[0].parentNode.replaceChild(body, nl[0])
        else:
            #Insert 
            self.documentElement.appendChild(body)

    def _get_images(self):
        nl = self.getElementsByTagName('IMG')
        hc = implementation._4dom_createHTMLCollection(nl)
        return hc

    def _get_applets(self):
        al = self.getElementsByTagName('APPLET')
        ol = self.getElementsByTagName('OBJECT')
        ol = filter(lambda x: x._get_code(), ol)
        return implementation._4dom_createHTMLCollection(al+ol)

    def _get_links(self):
        areal = self.getElementsByTagName('AREA')
        al = self.getElementsByTagName('A')
        al = filter(lambda x: x._get_href(), al+areal)
        return implementation._4dom_createHTMLCollection(areal+al)

    def _get_forms(self):
        fl = self.getElementsByTagName('FORM')
        return implementation._4dom_createHTMLCollection(fl)

    def _get_anchors(self):
        nl = self.getElementsByTagName('A');
        nl = filter(lambda x: x._get_name(), nl)
        return implementation._4dom_createHTMLCollection(nl)

    def _get_cookie(self):
        return self.cookie

    def _set_cookie(self,cookie):
        self.__dict__['cookie'] = cookie

    def open(self):
        #Clear out the doc
        self.__dict__['referer'] = ''
        self.__dict__['domain'] = ''
        self.__dict__['url'] = ''
        self.__dict__['cookie'] = ''
        self.__dict__['writable'] = 1
        
    def write(self, st):
        if not self.writable:
            return
    #We need to parse the string here
        from xml.dom.ext.reader.HtmlLib import FromHTML
        d = FromHtml(st, self)
        if d != self:
            self.appendChild(d)

    def writeln(self, st):
        st = st + '\n'
        self.write(st)

    def close(self):
        self.__dict__['writable'] = 0

    def _get_elementByID(self, ID):
        hc = self.getElementsByAttribute('*','ID',ID)
        if hc.length != 0:
            return hc[0]
        return None

    def _get_elementsByName(self,name):
        return self.getElementsByAttribute('*', 'NAME', name)

    #Overridden function
    def _get_documentElement(self):
        #We cannot use getElementsByTagName because of recursion
        documentElement = None
        for child in self.childNodes:
            if child.tagName == 'HTML':
                documentElement = child
                break
        if documentElement == None:
            documentElement = self.createElement('HTML')
            #We cannot just do an appendChild as we run into recursion
            self.children.append(documentElement)
            documentElement._set_parentNode(self)
        return documentElement

    #Not in spec
    def _get_elementsByAttribute(self, tagName, attribute, attrValue=None):
        nl = self.getElementsByTagName(tagName)
        hc = implementation._4dom_createHTMLCollection()
        for elem in nl:
            attr = elem.getAttribute(attribute)
            if attrValue == None and attr != '':
                hc.append(elem)
            elif attr == attrValue:
                hc.append(elem)
        return hc

    def __get_head(self):
        nl = self.getElementsByTagName('HEAD')
        if not nl:
            head = self.createElement('HEAD')
            #The head goes in front of the body
            body = self._get_body()
            self.documentElement.insertBefore(head, body)
        else:
            head = nl[0]
        return head 

    #Overridden
    def createElement(self, tagName):
        return self._4dom_createHTMLElement(tagName)

    def _4dom_createHTMLElement(self, tagName):
        from xml.dom.html import HTMLElement
        #We only except strings
        pass
        #See if tag name is in the lookup table
        normTagName = string.capitalize(tagName)
        if normTagName in NoClassTags:
            return HTMLElement.HTMLElement(self, string.upper(tagName), tagName)
        if HTMLTagMap.has_key(normTagName):
            className = HTMLTagMap[normTagName]
        else:
            className = normTagName
        klass = 'HTML%sElement' % className
        if not hasattr(self.htmlModules, klass):
            #Try to import it
            try:
                m = __import__('xml.dom.html.%s' % klass)
            except ImportError:
                raise TypeError('Unknown HTML Element %s' % tagName)
        m = getattr(self.htmlModules, klass)
        c = getattr(m, klass)
        rt = c(self, tagName)
        
        #if HTMLTagMap.has_key(normTagName):
        #    rt = c(self, tagName)
        #else:
        #    rt = c(self)
        return rt

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = implementation.createHTMLDocument(self._get_title())
            else:
                node = newOwner.createHTMLDocument()
        if deep:
            self.documentElement.cloneNode(1, node.documentElement, newOwner)
        node._set_referrer(self._get_referrer())
        node._set_domain(self._get_domain())
        node._set_URL(self._get_URL())
        node._set_cookie(self._get_cookie())
        return node

    def isXml(self):
        return 0

    def isHtml(self):
        return 1

#=== BEGIN COMPUTED ATTRIBUTES ===

    ### Attribute Access Mappings ### 

    from xml.dom.Document import Document 

    _readComputedAttrs = Document._readComputedAttrs.copy() 
    _readComputedAttrs.update ({ 
         'images'        : _get_images, 
         'applets'       : _get_applets, 
         'links'         : _get_links, 
         'forms'         : _get_forms, 
         'anchors'       : _get_anchors, 
         'title'         : _get_title, 
         'referrer'      : _get_referrer, 
         'domain'        : _get_domain, 
         'URL'           : _get_URL, 
         'body'          : _get_body, 
         'cookie'        : _get_cookie, 
      }) 

    _writeComputedAttrs = Document._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'title'         : _set_title, 
         'referrer'      : _set_referrer, 
         'domain'        : _set_domain, 
         'URL'           : _set_URL, 
         'body'          : _set_body, 
         'cookie'        : _set_cookie, 
      }) 

    # Create the read-only list of attributes 
    _readOnlyAttrs = [] 
    for attr in Document._readOnlyAttrs: 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 
    for attr in _readComputedAttrs.keys(): 
        if not _writeComputedAttrs.has_key(attr): 
            _readOnlyAttrs.append(attr) 

#=== END COMPUTED ATTRIBUTES ===

HTMLTagMap =    {'Isindex':     'IsIndex'
                ,'Optgroup':    'OptGroup'
                ,'Textarea':    'TextArea'
                ,'Fieldset':    'FieldSet'
                ,'Ul':          'UList'
                ,'Ol':          'OList'
                ,'Dl':          'DList'
                ,'Dir':         'Directory'
                ,'Li':          'LI'
                ,'P':           'Paragraph'
                ,'H1':          'Heading'
                ,'H2':          'Heading'
                ,'H3':          'Heading'
                ,'H4':          'Heading'
                ,'H5':          'Heading'
                ,'H6':          'Heading'
                ,'Q':           'Quote'
                ,'Br':          'BR'
                ,'Basefont':    'BaseFont'
                ,'Hr':          'HR'
                ,'A':           'Anchor'
                ,'Img':         'Image'
                ,'Caption':     'TableCaption'
                ,'Col':         'TableCol'
                ,'Colgroup':    'TableCol'
                ,'Td':          'TableCell'
                ,'Th':          'TableCell'
                ,'Tr':          'TableRow'
                ,'Thead':       'TableSection'
                ,'Tbody':       'TableSection'
                ,'Tfoot':       'TableSection'
                ,'Frameset':    'FrameSet'
                ,'Iframe':      'IFrame'
                ,'Form':        'Form'
                }

#HTML Elements with no specific DOM Interface of their own
NoClassTags =   ['Sub'
                ,'Sup'
                ,'Span'
                ,'Bdo'
                ,'Tt'
                ,'I'
                ,'B'
                ,'U'
                ,'S'
                ,'Strike'
                ,'Big'
                ,'Small'
                ,'Em'
                ,'Strong'
                ,'Dfn'
                ,'Code'
                ,'Samp'
                ,'Kbd'
                ,'Var'
                ,'Cite'
                ,'Acronym'
                ,'Abbr'
                ,'Dd'
                ,'Dt'
                ,'Noframes'
                ,'Noscript'
                ,'Address'
                ,'Center'
                ]


#--- (end HTMLDocument.py) ---
