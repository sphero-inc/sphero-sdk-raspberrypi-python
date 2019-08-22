#!/usr/bin/env python3

from ..parser.sphero_parser_base import SpheroParserBase
from ..handler.sphero_handler_base import SpheroHandlerBase


class SpheroPortBase:
    __slots__ = ['_port_id', '_handler', '_parser']

    def __init__(self, port_id, parser_factory, handler_factory):

        if not issubclass(parser_factory, SpheroParserBase):
            raise TypeError
        if not issubclass(handler_factory, SpheroHandlerBase):
            raise TypeError
        self._port_id = port_id
        self._handler = handler_factory(self)
        self._parser = parser_factory(self.handler.message_handler,
                                      self.handler.error_handler)

    @property
    def port_id(self):

        return self._port_id

    @port_id.setter
    def port_id(self, ID):

        self._port_id = ID

    @property
    def handler(self):

        return self._handler

    def send(self, msg):

        raise NotImplementedError
