#!/usr/bin/env python
import os

def test(testSuite):

    rt = os.system('cd ../Html/test_suite/ && python test.py')
    if rt:
        return 0
    return 1
