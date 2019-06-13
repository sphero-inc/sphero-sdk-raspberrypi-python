class Observer():
    _observers = []

    def __init__(self):
        self._observers.append(self)
        self._callbacks = {}

    def _register_callback(self, did, cid, callback, outputs):
        self._callbacks[(did, cid)] = (callback, outputs)
