#! /usr/bin/env python3

class BaseError(Exception):
    pass

class BadConnection(BaseError):
    pass

class BadResponse(BaseError):
    def __init__(self):
        pass

    def __str__(self):
        return '''The Response returned from the Server suggests a mismatch between library versions'''
