class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.callbacks = {}

    def _register_callback(self, did, cid, callback, outputs=[]):
        self.callbacks[(did, cid)] = (callback, outputs)
