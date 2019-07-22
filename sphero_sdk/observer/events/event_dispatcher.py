import logging
from sphero_sdk.observer.observer_base import Observer

logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self):
        pass

    def handle_message(self, message):
        # TODO AC - Do we need 'sequence numbers' for command responses?
        # TODO AC - Do we need 'source node' for async responses
        # TODO AC - Implement error handling
        for observer in Observer.observers:
            key = (message.did, message.cid)
            logger.debug("looking for entries with key %s.", key)
            if key in observer.handlers:
                handler, outputs = observer.handlers[key]
                logger.debug("entry found, dispatching!")
                self.__dispatch_event(handler, outputs, message)
                break

    def __dispatch_event(self, handler, outputs, message):
        if len(outputs) > 0:
            logger.debug("unpacking output from message")
            response = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response[param.name] = message.unpack(
                    param.data_type,
                    count=param.size
                )
            logger.debug("invoking callback")
            handler(**response)
        else:
            logger.debug("no outputs expected, invoking callback.")
            handler()

