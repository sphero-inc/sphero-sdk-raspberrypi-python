class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.__callbacks = {}

    def _register_callback(self, did, cid, callback, outputs=[]):
        self.__callbacks[(did, cid)] = (callback, outputs)
