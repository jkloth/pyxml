# 
# Top-level program for XML test suite
#

import sys, regrtest, getopt, string

if __name__ == '__main__':
    tests = regrtest.findtests(testdir = '.', stdtests = [], nottests = [])
    regrtest.main( tests, '.' )
