"""Python version compatibility support for minidom."""

# This module should only be imported using "import *".
#
# The following names are defined:
#
#   isinstance    -- version of the isinstance() function that accepts
#                    tuples as the second parameter regardless of the
#                    Python version
#
#   NodeList      -- lightest possible NodeList implementation
#
#   EmptyNodeList -- lightest possible NodeList that is guarateed to
#                    remain empty (immutable)
#
#   StringTypes   -- tuple of defined string types
#
#   GetattrMagic  -- base class used to make _get_<attr> be magically
#                    invoked when available
#   defproperty   -- function used in conjunction with GetattrMagic;
#                    using these together is needed to make them work
#                    as efficiently as possible in both Python 2.2+
#                    and older versions.  For example:
#
#                        class MyClass(GetattrMagic):
#                            def _get_myattr(self):
#                                return something
#
#                        defproperty(MyClass, "myattr",
#                                    "return some value")
#
#                    For Python 2.2 and newer, this will construct a
#                    property object on the class, which avoids
#                    needing to override __getattr__().  It will only
#                    work for read-only attributes.
#
#                    For older versions of Python, inheriting from
#                    GetattrMagic will use the traditional
#                    __getattr__() hackery to achieve the same effect,
#                    but less efficiently.
#
#   NewStyle      -- base class to cause __slots__ to be honored in
#                    the new world
#
#   True, False   -- only for Python 2.2 and earlier

__all__ = ["NodeList", "EmptyNodeList", "NewStyle",
           "StringTypes", "defproperty", "GetattrMagic"]

try:
    unicode
except NameError:
    StringTypes = type(''),
else:
    StringTypes = type(''), type(unicode(''))


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
    __all__.append("isinstance")


if list is type([]):
    class NodeList(list):
        __slots__ = ()

        def item(self, index):
            if 0 <= index < len(self):
                return self[index]

        def _get_length(self):
            return len(self)

        length = property(_get_length,
                          doc="The number of nodes in the NodeList.")

    class EmptyNodeList(list):
        __slots__ = ()

        def item(self, index):
            return None

        length = 0

        def _get_length(self):
            return 0

else:
    def NodeList():
        return []

    def EmptyNodeList():
        return []


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

    class NewStyle:
        pass

else:
    def defproperty(klass, name, doc):
        get = getattr(klass, ("_get_" + name)).im_func
        assert not hasattr(klass, "_set_" + name)
        prop = property(get, doc=doc)
        setattr(klass, name, prop)

    class GetattrMagic:
        pass

    NewStyle = object
