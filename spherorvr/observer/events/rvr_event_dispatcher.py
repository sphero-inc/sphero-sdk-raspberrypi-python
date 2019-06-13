from spherorvr.observer.observer_base import Observer


class RvrEventDispatcher:
    def __init__(self):
        pass

    def handle_response(self, message):
        for observer in Observer._observers:
            key = (message.did, message.cid)
            if key in observer._callbacks:
                callback, outputs = observer._callbacks[key]
                self._dispatch_event(callback, outputs, message)
                break

    def _dispatch_event(self, callback, outputs, message):
        response = {}
        for param in sorted(outputs, key=lambda x: x.index):
            response[param.name] = message.unpack(
                param.data_type,
                count=param.size
            )
        callback(**response)
