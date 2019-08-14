class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.handlers = {}

    def _register_handler(self, handler, **kwargs):
        did = kwargs['did']
        cid = kwargs['cid']

        outputs = []
        if 'outputs' in kwargs:
            outputs = kwargs['outputs']

        self.handlers[(did, cid)] = (handler, outputs)
