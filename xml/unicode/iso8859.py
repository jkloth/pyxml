"""This module adds a backwards-compatibility to the older wstring module.
It is intended for use by 4Suite only; do not use it in your own code."""

import string
import utf8_iso

_trans = string.maketrans("_-:","   ")
def _normalize(codeset):
    codeset = string.lower(codeset)
    codeset = string.translate(codeset, _trans)
    return codeset

class _Wstringmod:
    "Emulator for old wstring module"
    def __init__(self):
        self.aliases={}

    def install_alias(self, newname, oldname):
        self.aliases[_normalize(newname)] = _normalize(oldname)

    def from_utf8(self, utf8):
        return UTF8String(utf8)

wstring = _Wstringmod()

class UTF8String:
    "Emulator for the wstring type"
    def __init__(self, utf8):
        self.utf8 = utf8

    def encode(self, codeset):
        codeset = _normalize(codeset)
        if codeset == "utf 8":
            return self.utf8
        if codeset[:8] == "iso 8859":
            codeset = string.atoi(string.split(codeset)[2])
            input = self.utf8
            output = ""
            while input:
                for i in range(len(input)):
                    if ord(input[i])>128:
                        break
                if i == 0:
                    char, input = utf8_iso.utf8_to_code(codeset, input)
                    output = output + char
                else:
                    output = output + input[:i]
                    input = input[i:]
            return output
        try:
            self.encode(wstring.aliases[codeset])
        except KeyError:
            raise utf8_iso.ConvertError("unknown encoding")
