# 
# Top-level program for XML test suite
#

import regrtest

if __name__ == '__main__':
    tests = regrtest.findtests(testdir = '.', stdtests = [], nottests = [])
    regrtest.main( tests, '.' )
