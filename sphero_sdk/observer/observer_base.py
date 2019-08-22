class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.handlers = {}

    def _register_handler(self, handler, **kwargs):
        did = kwargs['did']
        cid = kwargs['cid']
        seq = kwargs.get('seq', -1)
        target = kwargs['target']

        if seq != -1:
            key = (did, cid, seq, target)
        else:
            key = (did, cid, target)

        outputs = []
        if 'outputs' in kwargs:
            outputs = kwargs['outputs']

        self.handlers[key] = (handler, outputs)

    def unregister_handler(self, key):
        """Removes entry with specified key values from handlers dictionary.

        Args:
            key (tuple): a tuple key that contains did, cid, seq (if command is not an async), and target
        """
        self.handlers.pop(key, None)
