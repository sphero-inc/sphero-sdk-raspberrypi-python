#!/usr/bin/env python3

import asyncio
import logging
from .sphero_parser_base import SpheroParserBase
from sphero_sdk.common.protocol.api_sphero_message import Message


logger = logging.getLogger(__name__)


class Parser(SpheroParserBase):
    __slots__ = ['_buf']

    def __init__(self, message_handler, error_handler):
        '''Class that Turns bytearrays into Messages

        Args:
            message_handler (coro): Takes Message
            error_handler (coro): Takes Malformed Message
        '''
        SpheroParserBase.__init__(self, message_handler, error_handler)
        self._buf = bytearray()

    def feed(self, data):
        '''Feed in raw byte data to the parser using this function'''
        self._buf += data
        asyncio.ensure_future(self._read())

    async def _read(self):
        # Discard Any bytes received before a SOP is received
        try:
            start_index = self._buf.index(Message.START_OF_PACKET)
            self._buf = self._buf[start_index:]
        except Exception as e:
            self._buf.clear()
            return

        # Try to Parse a Message
        msg = None
        skip_future_reads = False
        try:
            msg = Message.from_buffer(self._buf)
        except ValueError:  # Missing SOP, EOP
            skip_future_reads = True
            return
        except AttributeError:  # Bad Packet
            logger.warning('Invalid Packet Received!')
            error_buf = (self._buf[self._buf.index(Message.START_OF_PACKET):
                                   self._buf.index(Message.END_OF_PACKET) + 1])
            self._handle_error(error_buf)
        else:
            self._handle_message(msg)
        finally:
            # Regardless of outcome, we should rerun _read until no SOP or EOP
            if not skip_future_reads:
                asyncio.ensure_future(self._read())

        # Consume the bytes from the buffer
        try:
            self._buf = self._buf[self._buf.index(Message.END_OF_PACKET)+1:]
            logger.info(msg)
        except Exception:
            self._buf.clear()

    def _handle_message(self, msg):
        try:
            asyncio.ensure_future(self._message_handler(msg))
        except TypeError:
            logger.warning("Parser Fed without Message Handler Set")
            raise
        except Exception as e:
            logger.critical("Exception in Message Handler: {}".format(e))
            raise

    def _handle_error(self, buf):
        try:
            asyncio.ensure_future(self._error_handler(buf))
        except TypeError:
            logger.warning("Parser Fed without Error Handler Set")
            raise
        except Exception as e:
            logger.critical("Exception in Error Handler: {}".format(e))
            raise
