########################################################################
#
# File Name:            ParamElement.py
#
# Documentation:        http://docs.4suite.com/4XSLT/ParamElement.py.html
#
"""
Implementation of the XSLT Spec param stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import CoreFunctions, Util
from xml.xpath import XPathParser

class ParamElement(XsltElement):
    legalAttrs = ('name', 'select')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='param', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        name_attr = self.getAttributeNS('', 'name')
        split_name = Util.ExpandQName(
            name_attr,
            namespaces=self._nss
            )
        self.__dict__['_name'] = split_name
        self.__dict__['_select'] = self.getAttributeNS('', 'select')
        if self._select:
            parser = XPathParser.XPathParser()
            self.__dict__['_expr'] = parser.parseExpression(self._select)
        else:
            self.__dict__['_expr'] = None
        return

    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)

        if self._select:
            result = self._expr.evaluate(context)
        else:
            processor.pushResult()
            for child in self.childNodes:
                context = child.instantiate(context, processor)[0]
            result = processor.popResult()
            context.rtfs.append(result)

        context.set(origState)
        context.varBindings[self._name] = result
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix, self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name, self._select, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._select = state[3]
        self._expr = state[4]
        return
