from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR

def test(tester):

    tester.startGroup('Text')
	
    tester.startTest('Testing syntax')
    try:
        from xml.dom import Text
        from xml.dom.Text import Text
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument('','ROOT',dt)

    t = doc.createTextNode("ONETWO")
    tester.testDone()


    tester.startTest('Testing splitText()')
    t2 = t.splitText(3)
    if t.data != 'ONE':
       	tester.error('splitText did not properly split first half')
    if t2.data != 'TWO':
	tester.error('splitText did not properly split second half')
    try:
	t.splitText(100)
    except DOMException, x:
	if x.code != INDEX_SIZE_ERR:
	    raise x
    else:
 	tester.error('splitText doesn\'t catch an invalid index')
    tester.testDone()


    tester.startTest('Testing _4dom_joinText()')
    t = t._4dom_joinText(t,t2)
    if t.data != 'ONETWO':
	tester.error('joinText did not join');
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    t3 = t.cloneNode(0)
    if t3.data != t.data:
	error("cloneNode does not copy data")
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    from Ft.Lib import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
