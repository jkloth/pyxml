from xml.xpath import RuntimeException, CompiletimeException

try:
    import os, gettext
    locale_dir = os.path.split(__file__)[0]
    gettext.install('4Suite', locale_dir)
#except ImportError, IOError:
#Note, 1.5.2 has gettext, but no install
except (ImportError, AttributeError, IOError):
    def _(msg):
        return msg

COMPILETIME = {
    CompiletimeException.INTERNAL: _('There is an internal bug in 4XPath.  Please report this error code to support@4suite.org: %s'),
    CompiletimeException.SYNTAX: _('Parse error at line %d, column %d: %s'),
    CompiletimeException.PROCESSING: _('Error evaluating expression.'),
    #CompiletimeException.: _(''),
    }

RUNTIME = {
    RuntimeException.INTERNAL: _('There is an internal bug in 4XPath.  Please report this error code to support@4suite.org: %s'),

    RuntimeException.NO_CONTEXT: _('An XPath Context object is required in order to evaluate an expression.'),
    RuntimeException.UNDEFINED_VARIABLE: _('Variable undefined: ("%s", "%s").'),
    RuntimeException.UNDEFINED_PREFIX: _('Undefined namespace prefix: "%s".'),
    RuntimeException.WRONG_ARGUMENTS: _('Error in arguments to %s: %s'),
    #RuntimeException.: _(''),
    }

