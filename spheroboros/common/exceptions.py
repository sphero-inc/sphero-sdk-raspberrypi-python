#! /usr/bin/env python3

class Error(Exception):
    pass

class BadConnection(Error):
    def __init__(self):
        pass

    def __str__(self):
        return "Could not connect to the Sphero Service"

class BadResponse(Error):
    def __init__(self, helper=None):
        self.helper = helper
        pass

    def __str__(self):
        return "There was a mismatch between this Library and the Sphero Service: {}".format(self.helper)
