"""Python version compatibility support for minidom."""

# XXX This module needs more explanation!
# It should only be imported using "import *".

__all__ = ["isinstance", "NodeList", "EmptyNodeList",
           "StringTypes", "TupleType", "defproperty", "GetattrMagic"]

try:
    unicode
except NameError:
    StringTypes = type(''),
else:
    StringTypes = type(''), type(unicode(''))

TupleType = type(StringTypes)


# define True and False only if not defined as built-ins
try:
    True
except NameError:
    True = 1
    False = 0
    __all__.extend(["True", "False"])


try:
    isinstance('', StringTypes)
except TypeError:
    #
    # Wrap isinstance() to make it compatible with the version in
    # Python 2.2 and newer.
    #
    _isinstance = isinstance
    def isinstance(obj, type_or_seq):
        try:
            return _isinstance(obj, type_or_seq)
        except TypeError:
            for t in type_or_seq:
                if _isinstance(obj, t):
                    return 1
            return 0
else:
    # make this exportable from this module
    isinstance = isinstance


if list is type([]):
    class NodeList(list):
        def item(self, index):
            if 0 <= index < len(self):
                return self[index]

        def _get_length(self):
            return len(self)

        length = property(_get_length,
                          doc="The number of nodes in the NodeList.")

    class EmptyNodeList(tuple):
        def item(self, index):
            return None

        length = 0

        def _get_length(self):
            return 0

else:
    def NodeList():
        return []

    def EmptyNodeList():
        return ()

try:
    property
except NameError:
    def defproperty(klass, name, doc):
        # taken care of by the base __getattr__()
        pass

    class GetattrMagic:
        def __getattr__(self, key):
            if key.startswith("_"):
                raise AttributeError, key

            try:
                get = getattr(self, "_get_" + key)
            except AttributeError:
                raise AttributeError, key
            return get()

else:
    def defproperty(klass, name, doc):
        get = getattr(klass, ("_get_" + name)).im_func
        assert not hasattr(klass, "_set_" + name)
        prop = property(get, doc=doc)
        setattr(klass, name, prop)

    class GetattrMagic:
        pass
