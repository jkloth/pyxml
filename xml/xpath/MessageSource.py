from xml.xpath import Error

try:
    import os, gettext
    locale_dir = os.path.split(__file__)[0]
    gettext.install('4Suite', locale_dir)
#except ImportError, IOError:
#Note, 1.5.2 has gettext, but no install
except (ImportError, AttributeError, IOError):
    def _(msg):
        return msg

g_errorMessages = {
    Error.INTERNAL_ERROR: _('There is an internal bug in 4XPath.  Please report this error code to support@4suite.org: %s'),
    Error.PROCESSING: _('Error evaluating expression.'),

    Error.LEXICAL: _('FIXME'),
    Error.SYNTAX: _('Syntax error in expression at location %s'),

    Error.NO_CONTEXT: _('An XPath Context object is required in order to evaluate an expression.'),
    Error.UNDEFINED_VARIABLE: _('Variable undefined: (%s, %s).'),
    
    #Error.: _(''),

    }

