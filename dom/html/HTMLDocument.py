########################################################################
#
# File Name:            HTMLDocument.py
#
# Documentation:        http://docs.4suite.com/4DOM/HTMLDocument.py.html
#
# History:
# $Log: HTMLDocument.py,v $
# Revision 1.1.1.1  2000/06/20 15:40:52  uche
# Merged in the current 4DOM from Fourthought's CVS
#
# Revision 1.38  2000/06/09 01:36:39  jkloth
# Moved to generated source files
# Updated to Level 2 specification
# Fixed Copyright
# Updated to new TraceOut constructor
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

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom.Document import Document
from xml.dom.Node import Node
from xml.dom import implementation
from xml.dom import ext
import string

class HTMLDocument(Document):

    def __init__(self):
        Document.__init__(self, None)
        # These only make sense in a browser environment, therefore
        # they never change
        self.__dict__['__referrer'] = ''
        self.__dict__['__domain'] = None
        self.__dict__['__URL'] = ''

        self.__dict__['__cookie'] = ''
        self.__dict__['__writable'] = 0
        self.__dict__['__htmlModules'] = __import__('xml.dom.html').dom.html
        self.__dict__['_4dom_isNsAware'] = 0

    ### Attribute Methods ###

    def _get_URL(self):
        return self.__dict__['__URL']

    def _get_anchors(self):
        anchors = self.getElementsByTagName('A');
        anchors = filter(lambda x: x._get_name(), anchors)
        return implementation._4dom_createHTMLCollection(anchors)

    def _get_applets(self):
        al = self.getElementsByTagName('APPLET')
        ol = self.getElementsByTagName('OBJECT')
        ol = filter(lambda x: x._get_code(), ol)
        return implementation._4dom_createHTMLCollection(al+ol)

    def _get_body(self):
        body = ''
        #Try to find the body or FRAMESET
        elements = self.getElementsByTagName('FRAMESET')
        if not elements:
            elements = self.getElementsByTagName('BODY')
        if elements:
            body = elements[0]
        else:
            #Create a body
            body = self.createElement('BODY')
            self.documentElement.appendChild(body)
        return body

    def _set_body(self, newBody):
        targetName = body.tagName
        if not targetName in ['BODY','FRAMESET']:
            targetName = 'BODY'
        oldBody = self.getElementsByTagName(targetName)
        if oldBody:
            #Replace with the given body
            oldBody[0].parentNode.replaceChild(newBody, oldBody[0])
        else:
            #Insert
            self.documentElement.appendChild(body)

    def _get_cookie(self):
        return self.__dict__['__cookie']

    def _set_cookie(self, cookie):
        self.__dict__['__cookie'] = cookie

    def _get_domain(self):
        return self.__dict__['__domain']

    def _get_forms(self):
        forms = self.getElementsByTagName('FORM')
        return implementation._4dom_createHTMLCollection(forms)

    def _get_images(self):
        images = self.getElementsByTagName('IMG')
        return implementation._4dom_createHTMLCollection(images)

    def _get_links(self):
        areas = self.getElementsByTagName('AREA')
        anchors = self.getElementsByTagName('A')
        links = filter(lambda x: x._get_href(), areas+anchors)
        return implementation._4dom_createHTMLCollection(links)

    def _get_referrer(self):
        return self.__dict__['__referrer']

    def _get_title(self):
        title = ''
        elements = self.getElementsByTagName('TITLE')
        if elements:
            #Take the first
            title = elements[0].normalize()
            #Get first text node
            text = filter(lambda x: x.nodeType == Node.TEXT_NODE, title.childNodes)
            title = text[0].data
        return title

    def _set_title(self, title):
        # See if we can find the title
        title_nodes = self.getElementsByTagName('TITLE')
        if title_nodes:
            # We will replace the title node data with the new title
            title_nodes[0].data = title
        else:
            text = self.createTextNode(title)
            title_node = self.createElement('TITLE')
            title_node.appendChild(text)
            #Try and find the HEAD node
            self.__getHead().appendChild(title_node)

    ### Methods ###

    def close(self):
        self.__dict__['__writable'] = 0

    def getElementsByName(self, elementName):
        return self.getElementsByAttribute('*', 'NAME', elementName)

    def open(self):
        #Clear out the doc
        self.__dict__['__referrer'] = ''
        self.__dict__['__domain'] = None
        self.__dict__['__url'] = ''
        self.__dict__['__cookie'] = ''
        self.__dict__['__writable'] = 1
        
    def write(self, st):
        if not self.__dict__['__writable']:
            return
        #We need to parse the string here
        from xml.dom.ext.reader.HtmlLib import FromHTML
        d = FromHtml(st, self)
        if d != self:
            self.appendChild(d)

    def writeln(self, st):
        st = st + '\n'
        self.write(st)


    ### Overridden Methods ###

    def createElement(self, tagName):
        return self._4dom_createHTMLElement(tagName)

    def getElementByID(self, ID):
        hc = self.getElementsByAttribute('*','ID',ID)
        if hc.length != 0:
            return hc[0]
        return None

    ### Internal Methods ###

    def _4dom_getElementsByAttribute(self, tagName, attribute, attrValue=None):
        nl = self.getElementsByTagName(tagName)
        hc = implementation._4dom_createHTMLCollection()
        for elem in nl:
            attr = elem.getAttribute(attribute)
            if attrValue == None and attr != '':
                hc.append(elem)
            elif attr == attrValue:
                hc.append(elem)
        return hc

    def _4dom_getHead(self):
        nl = self.getElementsByTagName('HEAD')
        if not nl:
            head = self.createElement('HEAD')
            #The head goes in front of the body
            body = self._get_body()
            self.documentElement.insertBefore(head, body)
        else:
            head = nl[0]
        return head 

    def _4dom_createHTMLElement(self, tagName):
        from xml.dom.html import HTMLElement
        #We only except strings
        pass
        #See if tag name is in the lookup table
        normTagName = string.capitalize(tagName)
        if normTagName in NoClassTags:
            return HTMLElement.HTMLElement(self, tagName)
        if HTMLTagMap.has_key(normTagName):
            className = HTMLTagMap[normTagName]
        else:
            className = normTagName
        klass = 'HTML%sElement' % className
        if not hasattr(self.__dict__['__htmlModules'], klass):
            #Try to import it
            try:
                m = __import__('xml.dom.html.%s' % klass)
            except ImportError:
                raise TypeError('Unknown HTML Element %s' % tagName)
        m = getattr(self.__dict__['__htmlModules'], klass)
        c = getattr(m, klass)
        rt = c(self, tagName)

        return rt

    def cloneNode(self, deep, node=None, newOwner=None):
        if node == None:
            if newOwner == None:
                node = implementation.createHTMLDocument(self._get_title())
            else:
                node = newOwner.createHTMLDocument()
        if deep:
            self.documentElement.cloneNode(1, node.documentElement, newOwner)
        node.__dict__['__referrer'] = self._get_referrer()
        node.__dict__['__domain'] = self._get_domain()
        node.__dict__['__URL'] = self._get_URL()
        node._set_cookie(self._get_cookie())
        return node

    def isXml(self):
        return 0

    def isHtml(self):
        return 1

    ### Attribute Access Mappings ###

    _readComputedAttrs = Document._readComputedAttrs.copy()
    _readComputedAttrs.update ({ 
         'title'         : _get_title,
         'referrer'      : _get_referrer, 
         'domain'        : _get_domain, 
         'URL'           : _get_URL, 
         'body'          : _get_body, 
         'images'        : _get_images,
         'applets'       : _get_applets,
         'links'         : _get_links,
         'forms'         : _get_forms,
         'anchors'       : _get_anchors,
         'cookie'        : _get_cookie
      }) 

    _writeComputedAttrs = Document._writeComputedAttrs.copy() 
    _writeComputedAttrs.update ({ 
         'title'         : _set_title,
         'body'          : _set_body,
         'cookie'        : _set_cookie, 
      }) 

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Document._readOnlyAttrs + _readComputedAttrs.keys())


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
		,'Blockquote':  'Quote'
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
