#!/usr/bin/env python3

from .sphero_port_base import SpheroPortBase
import asyncio
import serial
from serial_asyncio import SerialTransport


class SerialSpheroPort(SpheroPortBase, asyncio.Protocol):
    __slots__ = ['__loop', '__transport']

    def __init__(self, loop, port_id,
                 parser_factory, handler_factory, dev, baud=115200):
        '''Class that moves bytes from a serial port to a Parser
            and messages to that serial port (typically from the Handler)

        Args:
            loop: asyncio event loop
            port_id: an ID for the port, used mostly by Handler
            parser_factory: Parser Class
            handler_factory: Handler Class
            dev: Serial Device
            baud: Serial Device baud rate
        '''
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
        '''Send a Message to the port'''
        self.__transport.write(msg.serialise())

    def data_received(self, data):
        self._parser.feed(data)

    def pause_writing(self):
        pass

    def resume_writing(self):
        pass

    def eof_received(self):
        pass

    def close(self):
        '''Close the Serial Transport'''
        self.__transport.close()
