# 
# Top-level program for XML test suite
#

import regrtest
del regrtest.STDTESTS[:]

if __name__ == '__main__':
    regrtest.main( tests = [],  testdir = '.' )
