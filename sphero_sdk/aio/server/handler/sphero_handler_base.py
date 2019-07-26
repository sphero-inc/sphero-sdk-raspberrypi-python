#!/usr/bin/env python3


class SpheroHandlerBase:

    __slots__ = ['_port']

    def __init__(self, port):

        self._port = port

    async def message_handler(self, msg):

        raise NotImplementedError

    async def error_handler(self, msg):

        raise NotImplementedError

    @staticmethod
    def from_type_string(type_string):

        if type_string == 'api':
            import handler.api_sphero_handler as api_sphero_handler
            return api_sphero_handler.Handler
        if type_string == 'shell':
            return NotImplementedError
        else:
            raise AttributeError
