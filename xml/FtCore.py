"""
Contains various definitions common to modules acquired from 4Suite
"""

class FtException(Exception):
    def __init__(self, errorCode, messages, args):
        # By defining __str__, args will be available.  Otherwise
        # the __init__ of Exception sets it to the passed in arguments.
        self.params = args
        self.errorCode = errorCode
        self.message = messages[errorCode] % args
        Exception.__init__(self, self.message, args)

    def __str__(self):
        return self.message
