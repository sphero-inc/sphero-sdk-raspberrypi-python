#!/usr/bin/env python3

import asyncio
import serial
import logging
from serial_asyncio import SerialTransport
from .sphero_port_base import SpheroPortBase

logger = logging.getLogger(__name__)


class SerialSpheroPort(SpheroPortBase, asyncio.Protocol):
    __slots__ = ['__loop', '__transport']

    def __init__(self, loop, port_id,
                 parser_factory, handler_factory, dev, baud=115200):
        """Class that moves bytes from a serial port to a Parser
            and messages to that serial port (typically from the Handler)

        Args:
            loop: asyncio event loop
            port_id: an ID for the port, used mostly by Handler
            parser_factory: Parser Class
            handler_factory: Handler Class
            dev: Serial Device
            baud: Serial Device baud rate
        """
        SpheroPortBase.__init__(self, port_id, parser_factory, handler_factory)
        asyncio.Protocol.__init__(self)
        self.__loop = loop
        ser = serial.Serial(dev, baud)
        self.__transport = SerialTransport(loop, self, ser)

    def connection_made(self, transport):

        self.__transport = transport

    def connection_lost(self, exc):
        pass

    def send(self, msg):
        """Send a Message instance to the port

        Args:
            msg (Message): Instance of Message

        """
        # data = msg.serialise()
        # print(data)
        # data = b'\x8d\x1A\x02\x18\x4a\x01\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\xE7\xd8'  # get_temperature
        data = b'\x8d\x1A\x01\x10\x0A\x01\x01\xC8\xd8'  # error 1
        # data = b'\x8d\x1A\x01\x10\x09\x01\x02\xC8\xd8'  # error 2
        # data = b'\x8d\x1A\x01\x10\x09\x01\x03\xC7\xd8'  # error 3
        # data = b'\x8d\x1A\x01\x10\x09\x01\x04\xC6\xd8'  # error 4
        # data = b'\x8d\x1A\x01\x10\x09\x01\x05\xC5\xd8'  # error 5
        # data = b'\x8d\x1A\x01\x10\x09\x01\x06\xC4\xd8'  # error 6
        logger.debug('Writing serial data: [{}]'.format(', '.join('0x{:02x}'.format(x) for x in data)))
        self.__transport.write(data)

    def data_received(self, data):
        logger.debug('Reading serial data: [{}]'.format(', '.join('0x{:02x}'.format(x) for x in data)))
        self._parser.feed(data)

    def pause_writing(self):
        pass

    def resume_writing(self):
        """Not implemented

        """
        pass

    def eof_received(self):
        pass

    def close(self):
        self.__transport.close()
