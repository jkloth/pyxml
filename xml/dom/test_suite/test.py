#!/usr/bin/env python
import string, time
from Ft.Lib import TestSuite, TraceOut

### Methods ###

def runTests(list, testSuite):
    print '#'*19, "Performing a test of DOM Core/Traversal", '#'*19

    start = time.time()
    for module in list:
        mod = __import__('test_' + string.lower(module))
        TraceOut.AddModule('xml.dom.' + module)
        rt = mod.test(testSuite)
        TraceOut.RemoveModule('xml.dom.' + module)

    print "Test Time - %f secs" %(time.time() - start)

### Application ###

if __name__ == '__main__':
    logLevel = TraceOut.INFO
    logFile = None
    haltOnError = 1

    test_list = [
        'Node',
        'NodeList',
        'NamedNodeMap',
        'NodeIterator',
        'TreeWalker',
        'Attr',
        'Element',
        'DocumentFragment',
        'Document',
        'DOMImplementation',
        'CharacterData',
        'Comment',
        'Text',
        'CDATASection',
        'DocumentType',
        'Entity',
        'EntityReference',
        'Notation',
        'ProcessingInstruction',
        'Struct',
#        'HTML',
#        'Demo',
#        'Pythonic'
         ]

    import sys, os, getopt

    prog_name = os.path.split(sys.argv[0])[1]
    short_opts = 'hl:nqtv:'
    long_opts = ['help',
                 'log=',
                 'no-error'
                 'tests'
                 'quiet',
                 'verbose='
                 ]

    usage = '''Usage: %s [options] [[all] [test]...]
Options:
  -h, --help             Print this message and exit
  -l, --log <file>       Write output to a log file (default=%s)
  -n, --no-error         Continue testing if error condition
  -q, --quiet            Display as little as possible
  -t, --tests            Show a list of tests that can be run
  -v, --verbose <level>  Set the output level (default=%s)
                           0 - display nothing
                           1 - errors only (same as --quiet)
                           2 - warnings and errors
                           3 - information, warnings and errors
                           4 - display everything
''' %(prog_name, logFile, logLevel)

    command_line_error = 0
    bad_options = []

    finished = 0
    args = sys.argv[1:]
    while not finished:
        try:
            optlist, args = getopt.getopt(args, short_opts, long_opts)
        except getopt.error, data:
            bad_options.append(string.split(data)[1])
            args.remove(bad_options[-1])
            command_line_error = 1
        else:
            finished = 1

    display_usage = 0
    display_tests = 0
    for op in optlist:
        if op[0] == '-h' or op[0] == '--help':
            display_usage = 1
        elif op[0] == "-l" or op[0] == '--log':
            logFile = op[1]
        elif op[0] == '-n' or op[0] == '--no-error':
            haltOnError = 0
        elif op[0] == '-t' or op[0] == '--tests':
            display_tests = 1
        elif op[0] == '-q' or op[0] == '--quiet':
            logLevel = 1
        elif op[0] == '-v' or op[0] == '--verbose':
            logLevel = int(op[1])

    all_tests = 0
    if args:
        lower_test = []
        for test in test_list:
            lower_test.append(string.lower(test))
        for test in args:
            if string.lower(test) == 'all':
                all_tests = 1
                break
            if string.lower(test) not in lower_test:
                print "%s: Test not found '%s'" %(prog_name, test)
                args.remove(test)
                display_tests = 1

    if len(args) and not all_tests:
        tests = args
    elif not display_tests:
        tests = test_list

    if command_line_error or display_usage or display_tests:
        for op in bad_options:
            print "%s: Unrecognized option '%s'" %(prog_name,op)
        if display_usage:
            print usage
        if display_tests:
            print 'Available tests are:'
            for t in test_list:
                print '  %s' % t
        sys.exit(command_line_error)

    testSuite = TestSuite.TestSuite(haltOnError, 1)
    TraceOut.SetLevel(logLevel)
    if logFile:
        TraceOut.SetOutput(logFile)
    runTests(tests, testSuite)

