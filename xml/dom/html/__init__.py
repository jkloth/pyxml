HTML_4_STRICT_INLINE = ['TT', 'I', 'B', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'OBJECT', 'BR', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP' 'SPAN', 'BDO', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_4_TRANSITIONAL_INLINE = ['TT', 'I', 'B', 'U', 'S', 'STRIKE', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'APPLET', 'OBJECT', 'FONT', 'BASEFONT', 'BR', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP', 'SPAN', 'BDO', 'IFRAME', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_FORBIDDEN_END = ['AREA', 'BASE', 'BASEFONT', 'BR', 'COL', 'FRAME', 'HR', 'IMG', 'INPUT', 'ISINDEX', 'LINK', 'META', 'PARAM']

HTML_OPT_END = ['BODY', 'COLGROUP', 'DD', 'DT', 'HEAD', 'HTML', 'LI', 'OPTION', 'P', 'TBODY', 'TD', 'TFOOT', 'TH', 'THEAD', 'TR']

HTML_CHARACTER_ENTITIES = {
    160: 'nbsp',
    161: 'iexcl',
    162: 'cent',
    163: 'pount',
    164: 'curren',
    165: 'yen',
    166: 'brvbar',
    167: 'sect',
    168: 'uml',
    169: 'copy',
    170: 'ordf',
    171: 'laquo',
    172: 'not',
    173: 'shy',
    174: 'reg',
    175: 'macr',
    176: 'deg',
    177: 'plusmn',
    178: 'sup2',
    179: 'sup3',
    180: 'acute',
    181: 'micro',
    182: 'para',
    183: 'middot',
    184: 'cedil',
    185: 'sup1',
    186: 'ordm',
    187: 'raquo',
    188: 'frac14',
    189: 'frac12',
    190: 'frac34',
    191: 'iquest',
    192: 'Agrave',
    193: 'Aacute',
    194: 'Acirc',
    195: 'Atilde',
    196: 'Auml',
    197: 'Aring',
    198: 'AElig',
    199: 'Ccedil',
    200: 'Egrave',
    201: 'Eacute',
    202: 'Ecirc',
    203: 'Euml',
    204: 'Igrave',
    205: 'Iacute',
    206: 'Icirc',
    207: 'Iuml',
    208: 'ETH',
    209: 'Ntilde',
    210: 'Ograve',
    211: 'Oacute',
    212: 'Ocirc',
    213: 'Otilde',
    214: 'Ouml',
    215: 'times',
    216: 'Oslash',
    217: 'Ugrave',
    218: 'Uacute',
    219: 'Ucirc',
    220: 'Uuml',
    221: 'Yacute',
    222: 'THORN',
    223: 'szlig',
    224: 'agrave',
    225: 'aacute',
    226: 'acirc',
    227: 'atilde',
    228: 'auml',
    229: 'aring',
    230: 'aelig',
    231: 'ccedil',
    232: 'egrave',
    233: 'eacute',
    234: 'ecirc',
    235: 'euml',
    236: 'igrave',
    237: 'iacute',
    238: 'icirc',
    239: 'iuml',
    240: 'eth',
    241: 'ntilde',
    242: 'ograve',
    243: 'oacute',
    244: 'ocirc',
    245: 'otilde',
    246: 'ouml',
    247: 'divide',
    248: 'oslash',
    249: 'ugrave',
    250: 'uacute',
    251: 'ucirc',
    252: 'uuml',
    253: 'yacute',
    254: 'thorn',
    255: 'yuml',
    }

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

from xml.unicode.iso8859 import wstring
wstring.install_alias('ISO-8859-1','ISO_8859-1:1987')

import re, string
g_xmlIllegalCharPattern = re.compile('[\x01-\x08\x0B-\x0D\x0E-\x1F\x80-\xFF]')
g_numCharEntityPattern = re.compile('&#(\d+);')
g_utf8TwoBytePattern = re.compile('([\xC0-\xC3])([\x80-\xBF])')
g_cdataCharPattern = re.compile('[&<]|]]>')
g_charToEntity = {
        '&': '&amp;',
        '<': '&lt;',
        ']]>': ']]&gt;',
        }


def ConvertChar(m):
    char = ((int(ord(m.group(1))) & 0x03) << 6) | (int(ord(m.group(2))) & 0x3F)
    if HTML_CHARACTER_ENTITIES.has_key(char):
        return '&'+HTML_CHARACTER_ENTITIES[char]+';'
    else:
        return m.group()


def TranslateHtmlCdata(characters, encoding='UTF-8', prev_chars=''):
    #Translate numerical char entity references with HTML entity equivalents
    if not characters:
        return ''
    new_string, num_subst = re.subn(
        g_cdataCharPattern,
        lambda m, d=g_charToEntity: d[m.group()],
        characters
        )
    if prev_chars[-2:] == ']]' and new_string[0] == '>':
        new_string = '&gt;' + new_string[1:]
    new_string, num_subst = re.subn(g_utf8TwoBytePattern, ConvertChar,
                                    new_string)
    encoding = string.upper(encoding)
    if encoding == 'UTF-8':
        pass
    else:
        try: 
            ws = wstring.from_utf8(new_string)
            new_string = ws.encode(encoding)
        except wstring.ConvertError:
            raise Exception('Unsupported output encoding')
    #Note: use decimal char entity rep because some browsers are broken
    new_string, num_subst = re.subn(g_xmlIllegalCharPattern, lambda m: '&#%i;'%ord(m.group()), new_string)
    return new_string


