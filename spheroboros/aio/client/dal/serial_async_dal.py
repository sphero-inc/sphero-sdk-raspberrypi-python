#! /usr/bin/env python3

from spheroboros.aio.common.dal.async_dal_base import AsyncDalBase
from spheroboros.aio.server import SerialSpheroPort,\
                                   Parser,\
                                   Handler,\
                                   Message,\
                                   ErrorCode


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
                           timeout=None, inputs=None, outputs=None):
        msg = Message()
        msg.did = did
        msg.cid = cid
        msg.target = target

        for param in inputs:
            msg.pack(param.data_type, param.value, param.size)

        def response_handler(msg):
            response_list = []
            for param in sorted(outputs, key=lambda x: x.index):
                response_list.append(msg.unpack(param.data_type, param.size))

            return ErrorCode.SUCCESS, tuple(response_list)

        return await self.handler.send_command(
            msg,
            response_handler,
            timeout
        )

    async def on_command(self, did, cid, target, handler,
                         timeout=None, outputs=None):
        async def wrapper(msg):
            response = {}
            for param in sorted(outputs, key=lambda x: x.index):
                response[param.name] = msg.unpack(param.data_type)

            await handler(**response)

            return ErrorCode.SUCCESS, bytearray()

        self.handler.add_command_worker(did, cid, target, wrapper)
