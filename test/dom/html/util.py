def error(msg):
    raise 'ERROR: ' + msg


def testAttribute(elem,attr):
    #First do a set
    exec 'elem._set_%s("TEST")' % attr
    exec 'rt = elem._get_%s()' % attr
    if rt != 'TEST':
        error('get/set of %s Failed' % attr);

def testIntAttribute(elem,attr):
    exec 'elem._set_%s(1)' % attr
    exec 'rt = elem._get_%s()' % attr
    if rt != 1:
        error('get/set of %s Failed' % attr);
    exec 'elem._set_%s(0)' % attr
    exec 'rt = elem._get_%s()' % attr
    if rt != 0:
        error('get/set of %s Failed' % attr);


