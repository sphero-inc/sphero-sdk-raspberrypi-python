#!/usr/bin/env python3


class SpheroParserBase:
    __slots__ = ['_message_handler', '_error_handler']

    def __init__(self, message_handler, error_handler):
        self._message_handler = message_handler
        self._error_handler = error_handler

    def feed(self, data):
        '''Feed the Parser new data
        Calls message_handler and error_handler
        '''
        raise NotImplementedError

    def set_message_handler(self, message_handler):
        self._message_handler = message_handler

    def set_error_handler(self, error_handler):
        self._error_handler = error_handler

    @staticmethod
    def from_type_string(type_string):
        if type_string == 'api':
            import parser.api_sphero_parser as api_sphero_parser
            return api_sphero_parser.Parser
        if type_string == 'shell':
            raise NotImplementedError
        else:
            raise AttributeError
