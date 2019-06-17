from spherorvr.observer.observer_base import Observer


class RvrEventDispatcher:
    def __init__(self):
        pass

    def handle_message(self, message):
        # TODO AC - Do we need 'sequence numbers' for command responses?
        # TODO AC - Do we need 'source node' for async responses
        # TODO AC - Implement error handling
        for observer in Observer._observers:
            key = (message.did, message.did)
            if key in observer._callbacks:
                callback, outputs = observer._callbacks[key]
                self._dispatch_event(callback, outputs, message)
                break

    def _dispatch_event(self, callback, outputs, message):
        if len(outputs) > 0:
            response = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response[param.name] = message.unpack(
                    param.data_type,
                    count=param.size
                )
            callback(**response)
        else:
            callback()
