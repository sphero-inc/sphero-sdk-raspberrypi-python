#! /usr/bin/env python3

import logging
from sphero_sdk.common.protocol.api_sphero_message import Message

logger = logging.getLogger(__name__)


class ObserverParser:
    __slots__ = ['__buf', '__dispatcher']

    def __init__(self, dispatcher):
        self.__buf = bytearray()
        self.__dispatcher = dispatcher

    def feed(self, data):
        self.__buf += data
        logger.debug('Appending bytes: [{}]'.format(', '.join('0x{:02x}'.format(x) for x in self.__buf)))
        self.__read()

    def __read(self):
        # Discard Any bytes received before a SOP is received
        try:
            start_index = self.__buf.index(Message.START_OF_PACKET)
            self.__buf = self.__buf[start_index:]
        except Exception as e:
            self.__buf.clear()
            return

        # Try to Parse a Message
        msg = None
        skip_future_reads = False
        try:
            msg = Message.from_buffer(self.__buf)
        except ValueError:  # Missing SOP, EOP
            logger.debug('Packet missing SOP/EOP!')
            skip_future_reads = True
            return
        except AttributeError:  # Bad Packet
            logger.error('Invalid packet received!')
            error_buf = (self.__buf[self.__buf.index(Message.START_OF_PACKET):
                                   self.__buf.index(Message.END_OF_PACKET) + 1])
            self.__handle_error(error_buf)
        else:
            skip_future_reads = True
            logger.info('Parsing packet complete: %s', msg)
            self.__dispatcher.handle_message(msg)
        finally:
            # Regardless of outcome, we should rerun _read until no SOP or EOP
            if not skip_future_reads:
                self.__read()

        # Consume the bytes from the buffer
        try:
            logger.debug('Consuming bytes in packet.')
            self.__buf = self.__buf[self.__buf.index(Message.END_OF_PACKET) + 1:]
        except Exception:
            self.__buf.clear()

    def __handle_error(self, buf):
        '''
        try:
            asyncio.ensure_future(self._error_handler(buf))
        except TypeError:
            logger.warning('Parser Fed without Error Handler Set')
            raise
        except Exception as e:
            logger.critical('Exception in Error Handler: {}'.format(e))
            raise
        '''
        pass

