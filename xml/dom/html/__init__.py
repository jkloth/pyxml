HTML_4_STRICT_INLINE = ['TT', 'I', 'B', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'OBJECT', 'BR', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP' 'SPAN', 'BDO', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_4_TRANSITIONAL_INLINE = ['TT', 'I', 'B', 'U', 'S', 'STRIKE', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'APPLET', 'OBJECT', 'FONT', 'BASEFONT', 'BR', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP', 'SPAN', 'BDO', 'IFRAME', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_FORBIDDEN_END = ['AREA', 'BASE', 'BASEFONT', 'BR', 'COL', 'FRAME', 'HR', 'IMG', 'INPUT', 'ISINDEX', 'LINK', 'META', 'PARAM']

HTML_OPT_END = ['BODY', 'COLGROUP', 'DD', 'DT', 'HEAD', 'HTML', 'LI', 'OPTION', 'P', 'TBODY', 'TD', 'TFOOT', 'TH', 'THEAD', 'TR']

HTML_NAME_ALLOWED = ['A',
                     'APPLET',
                     'BUTTON',
                     'FORM',
                     'FRAME',
                     'IFRAME',
                     'IMG',
                     'INPUT',
                     'MAP',
                     'META',
                     'OBJECT',
                     'PARAM',
                     'SELECT',
                     'TEXTAREA']

from xml.dom.html import HTMLDOMImplementation

htmlImplementation = HTMLDOMImplementation.HTMLDOMImplementation()
