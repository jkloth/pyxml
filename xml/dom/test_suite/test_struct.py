def testRestriction(tester, doc, mapping, node, good):
    # Any keys that are in the mapping but not in good are automaticly bad
    bad = []
    for key in mapping.keys():
        if not key in good:
            bad.append(key)

    df = doc.createDocumentFragment()

    # Make sure none of the good fail
    for type in good:
        try:
            node.appendChild(mapping[type])
        except:
            tester.error('Didn\'t allow addition of %s' % type)
        else:
            df.appendChild(mapping[type])


     # Add the good nodes in a DocFrag too
    try:
        node.appendChild(df)
    except:
        tester.error('Could not append DocumentFragment')

    # And none of the bad work
    for type in bad:
        try:
            node.appendChild(mapping[type])
        except:
            pass
        else:
            tester.error('Allowed addition of %s' % type)


def test(tester):
    tester.startGroup('DOM Structure Model')

    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('dt1', '', '')
    doc = implementation.createDocument('', None, dt)
    df = doc.createDocumentFragment()

    Nodes = {}
    Nodes['Document'] = implementation.createDocument('','ROOT2', dt)
    Nodes['DocType'] = implementation.createDocumentType('dt2', '', '')
    Nodes['Element'] = doc.createElement('tagName1')
    Nodes['Text'] = doc.createTextNode('data')
    Nodes['Comment'] = doc.createComment('data')
    Nodes['CDATA'] = doc.createCDATASection('data')
    Nodes['ProcInstruct'] = doc.createProcessingInstruction('target', 'data')
    Nodes['Attr'] = doc.createAttribute('name')
    Nodes['EntityRef'] = doc.createEntityReference('name')
    tester.testDone()


    tester.startTest('Testing Document')
    good = ['Element',
            'ProcInstruct',
            'Comment',
            ]

    # Add duplicate Element & DocType
    Nodes['Element2'] = doc.createElement('tagName2')

    testRestriction(tester, doc, Nodes, doc, good)

    # Remove added items
    del Nodes['Element2']
    tester.testDone()


    tester.startTest('Testing DocumentFragment')
    good = ['Element',
            'ProcInstruct',
            'Comment',
            'Text',
            'CDATA',
            'EntityRef',
            ]

    testRestriction(tester, doc, Nodes, df, good)
    tester.testDone()


    tester.startTest('Testing DocumentType')
    good = [
            ]
    testRestriction(tester, doc, Nodes, dt, good)
    tester.testDone()


    tester.startTest('Testing EntityReference')
    good = ['Element',
            'ProcInstruct',
            'Comment',
            'Text',
            'CDATA',
            'EntityRef'
            ]

    ref = doc.createEntityReference('test')
    testRestriction(tester, doc, Nodes, ref, good)
    tester.testDone()


    tester.startTest('Testing Element')
    good = ['Element',
            'ProcInstruct',
            'Comment',
            'Text',
            'CDATA',
            'EntityRef',
            ]

    testRestriction(tester, doc, Nodes, Nodes['Element'], good)
    tester.testDone()


    tester.startTest('Testing Attr')
    good = ['Text',
            'EntityRef',
            ]

    testRestriction(tester, doc, Nodes, Nodes['Attr'], good)
    tester.testDone()


    tester.startTest('Testing Comment')
    good = [
            ]

    testRestriction(tester, doc, Nodes, Nodes['Comment'], good)
    tester.testDone()


    tester.startTest('Testing Text')
    good = [
            ]

    testRestriction(tester, doc, Nodes, Nodes['Text'], good)
    tester.testDone()


    tester.startTest('Testing CDATASection')
    good = [
            ]

    testRestriction(tester, doc, Nodes, Nodes['CDATA'], good)
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    from Ft.Lib import TestSuite

    tester = TestSuite.TestSuite(0,1)
    retVal = test(tester)
    sys.exit(retVal)
