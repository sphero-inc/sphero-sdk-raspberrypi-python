import logging
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
        # TODO AC - Implement error handling

        if message.is_response:
            key = (message.did, message.cid, message.seq, message.source)
        else:
            key = (message.did, message.cid, message.source)

        for observer in Observer.observers:
            logger.debug("looking for entries with key %s.", key)
            if key in observer.handlers:
                handler, outputs = observer.handlers[key]

                if message.is_response:
                    observer.unregister_handler(key)

                logger.debug("entry found, dispatching!")
                self.__dispatch_event(handler, outputs, message)
                break

    def __dispatch_event(self, handler, outputs, message):
        if len(outputs) > 0:
            logger.debug("unpacking output from message")
            response_dictionary = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response_dictionary[param.name] = message.unpack(
                    param.data_type,
                    count=param.size
                )
            logger.debug("invoking callback")
            handler(response_dictionary)
        else:
            logger.debug("no outputs expected, invoking callback.")
            handler()

