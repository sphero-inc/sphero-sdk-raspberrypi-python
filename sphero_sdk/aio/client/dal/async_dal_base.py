#! /usr/bin/env python3


class AsyncDalBase:
    def __init__(self):
        pass

    async def send_command(self, did, cid, target,
                           timeout=None, inputs=[], outputs=[]):
        '''Returns the response.

        Call the Coroutine like so::
            output0, output1, ... outputN = await self.send_command(
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

    async def on_command(self, did, cid, target, handler,
                         timeout=None, outputs=[]):
        '''Provide a Handler Coroutine for Data Comming Asynchronously from the Bot
        Handler Should Take the Form::
            async def handler(output0, output1, ... outputN):
                # Do your work in here
                pass

        Don't call the coroutine directly, it needs its own task::
            asyncio.ensure_future(
                self.on_command(
                    did,
                    cid,
                    target,
                    handler
                    timout,
                    outputs=[
                        Parameter(name='output0', data_type='output0DataType', index=0),
                        Parameter(name='output1', data_type='output1DataType', index=1),
                        ...
                        Parameter(name='outputN', data_type='outputNDataType', index=N),
                    ]
                )
            )
        '''
        raise NotImplementedError
