"""
Wrapper around drivers2.drv_pyexpat, for compatibility with Python 2.
This driver works with pyexpat.__version__ == '1.5'.

$Id: expatreader.py,v 1.1 2000/09/17 18:27:07 loewis Exp $
"""

import drivers2.drv_pyexpat

ExpatParser = drivers2.drv_pyexpat.ExpatDriver

def create_parser(*args, **kwargs):
    return apply(ExpatParser, args, kwargs)
