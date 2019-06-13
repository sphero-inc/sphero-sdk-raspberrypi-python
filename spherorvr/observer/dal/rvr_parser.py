import logging
from spheroboros.aio.server.protocol.api_sphero_message import Message

logger = logging.getLogger(__name__)


class RvrParser:
    __slots__ = ['_buf', '_dispatcher']

    def __init__(self, dispatcher):
        self._buf = bytearray()
        self._dispatcher = dispatcher

    def feed(self, data):
        self._buf += data
        self._read()

    def _read(self):
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
            skip_future_reads = True
            self._dispatcher.handle_response(msg)
        finally:
            # Regardless of outcome, we should rerun _read until no SOP or EOP
            if not skip_future_reads:
                self._read()

        # Consume the bytes from the buffer
        try:
            self._buf = self._buf[self._buf.index(Message.END_OF_PACKET)+1:]
            logger.info(msg)
        except Exception:
            self._buf.clear()

    def _handle_error(self, buf):
        '''
        try:
            asyncio.ensure_future(self._error_handler(buf))
        except TypeError:
            logger.warning("Parser Fed without Error Handler Set")
            raise
        except Exception as e:
            logger.critical("Exception in Error Handler: {}".format(e))
            raise
        '''
        pass

