import wstring

funcs=(
    ("utf8",lambda s:wstring.from_utf8(s.utf8())),
    ("utf7",lambda s:wstring.from_utf7(s.utf7())),
    ("ucs2",lambda s:wstring.from_ucs2(s.ucs2())),
    ("ucs4",lambda s:wstring.from_ucs4(s.ucs4())),
    ("utf16",lambda s:wstring.from_utf16(s.utf16())))

def test():
    runes=wstring.L("")
    for i in range(16):
        rune = 1<<i
        for rune in (rune, rune+1, rune*2-2, rune*2-1):
            s = wstring.chr(rune)
            runes=runes+s
            r = wstring.ord(s)
            print i, rune, `s`, r,
            if r != rune:
                print "Ouch!",
            print
	    for n,f in funcs:
		if f(s)!=s:
		    print "Ouch! %s failed for %x" %(n,rune)
    if runes!=wstring.from_utf8(runes.utf8()):
	print "Ouch!"
    if runes!=wstring.from_utf7(runes.utf7()):
	print "Ouch!"
    if runes!=wstring.from_ucs2(runes.ucs2()):
	print "Ouch!"
    if runes!=wstring.from_ucs4(runes.ucs4()):
	print "Ouch!"
    if runes!=wstring.from_utf16(runes.utf16()):
	print "Ouch!"
    
test()

