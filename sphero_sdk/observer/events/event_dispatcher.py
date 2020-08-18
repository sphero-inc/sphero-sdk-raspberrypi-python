import logging
from sphero_sdk.common.protocol import ErrorCode
from sphero_sdk.observer.observer_base import Observer

logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self):
        pass

    def handle_message(self, message):
        """Uses the message did and cid properties as keys to check if a handler exists in the master dictionary of
        registered handlers.  If an entry is found, an event is raised.

        Args:
            message (Message): Used to look for registered handlers for this message.

        """

        if message.err is not None and message.err is not ErrorCode.success:
            raise Exception(message.err.name)

        if message.is_response:
            key = (message.did, message.cid, message.seq, message.source)
            logger.debug(
                'Looking for entries with key (CID: 0x{:02x}, DID: 0x{:02x}, Seq: {}, Source: {})'.format(
                key[0], key[1], key[2], key[3]
                )
            )
        else:
            key = (message.did, message.cid, message.source)
            logger.debug(
                'Looking for entries with key (CID: 0x{:02x}, DID: 0x{:02x}, Source: {})'.format(
                    key[0], key[1], key[2]
                )
            )

        for observer in Observer.observers:
            if key in observer.handlers:
                handler, outputs = observer.handlers[key]

                if message.is_response:
                    observer.unregister_handler(key)

                logger.debug('Entry found, dispatching!')
                self.__dispatch_event(handler, outputs, message)
                break

    def __dispatch_event(self, handler, outputs, message):
        if len(outputs) > 0:
            logger.debug('Unpacking output from message')
            response_dictionary = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response_dictionary[param.name] = message.unpack(
                    param.data_type,
                    count=param.size
                )
            logger.debug('Invoking callback with response data: {}'.format(response_dictionary))
            handler(response_dictionary)
        else:
            logger.debug('No outputs expected, invoking callback.')
            handler()

