
__all__ = ['iso8601']

import string
def escape(data, entities = {}):
    """Escape &, <, and > in a string of data.
    You can escape other strings of data by passing a dictionary as 
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """
    data = string.replace(data, "&", "&amp;")
    data = string.replace(data, "<", "&lt;")
    data = string.replace(data, ">", "&gt;")
    for chars, entity in entities.items():
        data = string.replace(data, chars, entity)        
    return data

    
