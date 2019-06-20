import logging
from spheroboros.aio.server import Message

logger = logging.getLogger(__name__)


class RvrDal:
    def __init__(self, port):
        self._port = port
        self._sequences = list(range(1, 256))
        pass

    def send_command(self, did, cid, target, timeout=None, inputs=[], outputs=[]):

        message = Message()
        message.did = did
        message.cid = cid
        message.target = target

        if len(outputs) > 0:
            message.requests_response = True
            message.seq = self._sequences.pop()

        for param in inputs:
            message.pack(param.data_type, param.value)

        logger.info("sending message: %s", message)

        self._port.send(message)

    def close(self):
        self._port.close()

    def on_command(self, did, cid, target, handler,
                   timeout=None, outputs=None):
        '''Provide a Handler Function for Data Coming Asynchronously from the Bot
        That handler will operate in a separate Thread, so it's best to put any data
        needed in the main thread into a queue.Queue object

        For Example::
            from queue import Queue
            q = Queue()
            def handler(output0, output1, ... outputN):
                #operates in different thread
                q.put((output0, output1, ... outputN))

            # back in main thread
            (output0, output1, ... outputN) = q.get()

        Should probably create a new thread for this bad larry::
            thread = Thread(
                target=self.on_command,
                args=(did, cid, target, handler),
                kwargs=(
                    timeout=timeout,
                    outputs=[
                        Parameter(name='output0', data_type='output0DataType', index=0),
                        Parameter(name='output1', data_type='output1DataType', index=1),
                        ...
                        Parameter(name='outputN', data_type='outputNDataType', index=N),
                    ]
                )
            )

            thread.start()
        '''
        raise NotImplementedError
