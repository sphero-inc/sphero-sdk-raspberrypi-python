#! /usr/bin/env python3


class BlockingDalBase:
    def __init__(self):
        pass

    def send_command(self, did, cid, target,
                     timeout=None, inputs=None, outputs=None):
        '''Returns the response.

        Call the Coroutine like so::
            output0, output1, ... outputN = self.send_command(
                did,
                cid,
                target,
                timeout,
                inputs=[
                    Parameter(name='input0', data_type='input0DataType', value=input0),
                    Parameter(name='input1', data_type='input1DataType', value=input1),
                    ...
                    Parameter(name='inputM', data_type='inputMDataType', value=inputM),
                ],
                outputs=[
                    Parameter(name='output0', data_type='output0DataType', index=0),
                    Parameter(name='output1', data_type='output1DataType', index=1),
                    ...
                    Parameter(name='outputN', data_type='outputNDataType', index=N),
                ]
            )

        '''
        raise NotImplementedError

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
