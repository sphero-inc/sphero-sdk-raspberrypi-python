#! /usr/bin/env python3

from spheroboros.aio.common.dal.async_dal_base import AsyncDalBase
from spheroboros.aio.server import SerialSpheroPort,\
                                   Parser,\
                                   Handler,\
                                   Message,\
                                   ErrorCode,\
                                   Flags


class SerialAsyncDal(AsyncDalBase, SerialSpheroPort):
    def __init__(self, loop=None, device='/dev/ttyS0', baud=115200):
        AsyncDalBase.__init__(self)
        SerialSpheroPort.__init__(
            self,
            loop,
            1,
            Parser,
            Handler,
            device,
            baud
        )

    async def send_command(self, did, cid, target,
                           timeout=None, inputs=[], outputs=[]):
        msg = Message()
        msg.did = did
        msg.cid = cid
        msg.target = target

        if len(outputs) > 0:
            msg.requests_response = True

        for param in inputs:
            msg.pack(param.data_type, param.value)

        def response_handler(msg):
            response_list = []
            for param in sorted(outputs, key=lambda x: x.index):
                response_list.append(msg.unpack(param.data_type))

            return tuple(response_list)

        return await self.handler.send_command(
            msg,
            response_handler=response_handler if len(outputs) > 0 else None,
            timeout=timeout
        )

    async def on_command(self, did, cid, target, handler,
                         timeout=None, outputs=[]):
        async def wrapper(msg):
            response = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response[param.name] = msg.unpack(
                    param.data_type,
                    count=param.size
                )

            await handler(**response)

            return ErrorCode.SUCCESS, bytearray()

        self.handler.add_command_worker(did, cid, target, wrapper)
