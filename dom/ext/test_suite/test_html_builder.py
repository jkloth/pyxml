########################################################################
#
# File Name:   TestHtmlBuilder.py
#
# Docs:        http://docs.4suite.com/4Dom/TestHtmlBuilder.py.html
#
# History:
# $Log: test_html_builder.py,v $
# Revision 1.1  2000/06/20 15:40:51  uche
# Initial revision
#
# Revision 1.1  2000/05/24 04:05:47  uogbuji
# fixed tab issues
# fixed nasty recursion bug in HtmlLib
#
# Revision 1.1  2000/04/27 18:19:55  uogbuji
# Checking in XML-SIG/Zope conversion for Jeremy (jkloth), who made the changes
#
# Revision 1.3  2000/01/03 23:50:25  uche
# Implemented xsl:sort
# Many bug-fixes and additions
#
# Revision 1.2  1999/08/31 14:29:23  molson
# Expanded the list of allowable single tags
#
# Revision 1.1  1999/08/30 18:18:58  molson
# Fixed the HTML Builder so it now handles some tags that do not commonly
# have end tags. BR, HR, and IMG
#
#
#
#
"""
Test suite for the Html portion of the builder.
WWW: http://4suite.com/4Dom        e-mail: support@4suite.com
Copyright (c) 2000 Fourthought, Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


def test():
     from xml.dom.ext.reader import HtmlLib
     from xml.dom import ext

     d = HtmlLib.FromHtmlFile('single.html')
     ext.PrettyPrint(d)

     d = HtmlLib.FromHtmlFile('mulit-single.html')
     ext.PrettyPrint(d)

     d = HtmlLib.FromHtmlFile('bigTest.html')
     ext.PrettyPrint(d)

if __name__ == '__main__':
    test()
    

    
