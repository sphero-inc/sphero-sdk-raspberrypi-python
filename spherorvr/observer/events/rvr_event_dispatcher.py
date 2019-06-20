import logging
from spherorvr.observer.observer_base import Observer

logger = logging.getLogger(__name__)


class RvrEventDispatcher:
    def __init__(self):
        pass

    def handle_message(self, message):
        # TODO AC - Do we need 'sequence numbers' for command responses?
        # TODO AC - Do we need 'source node' for async responses
        # TODO AC - Implement error handling
        for observer in Observer.observers:
            key = (message.did, message.cid)
            logger.debug("looking for entries with key %s.", key)
            if key in observer._callbacks:
                callback, outputs = observer._callbacks[key]
                logger.debug("entry found, dispatching!")
                self.__dispatch_event(callback, outputs, message)
                break

    def __dispatch_event(self, callback, outputs, message):
        if len(outputs) > 0:
            logger.debug("unpacking output from message")
            response = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response[param.name] = message.unpack(
                    param.data_type,
                    count=param.size
                )
            logger.debug("invoking callback")
            callback(**response)
        else:
            logger.debug("no outputs expected, invoking callback.")
            callback()

