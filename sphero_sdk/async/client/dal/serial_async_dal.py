#! /usr/bin/env python3

from sphero_sdk.async.client.dal.async_dal_base import AsyncDalBase
from sphero_sdk.async.server import SerialSpheroPort, Parser, Handler
from sphero_sdk.common.protocol import Message, ErrorCode


class SerialAsyncDal(AsyncDalBase, SerialSpheroPort):
    """
    """

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

    async def send_command(self, did, cid, target, timeout=None, inputs=[], outputs=[]):
        """Creates a Message object using the provided parameters and creates response handler that
        if a response is requested.

        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            target (uint8): 1 - Nordic; 2 - ST
            timeout (uint8): Time in seconds to wait for a response, if one is requested. Otherwise, ignored.
            inputs (list(Parameter)): Inputs for command that is being sent
            outputs (list(Parameter)): Expected outputs for command that is being sent

        Returns:
            The result of the response_handler, or None if a response_handler
            was not provided
        """

        msg = Message()
        msg.did = did
        msg.cid = cid
        msg.target = target
        msg.is_activity = True

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

    async def on_command(self, did, cid, target, handler, timeout=None, outputs=[]):
        """Creates a wrapper to unpack response data and invoke the provided handler.
        Calls handler.add_command_worker() using parameters and wrapper() as inputs

        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            target (uint8): 1 - Nordic; 2 - ST
            timeout (uint8): Timeout in seconds
            outputs (list): Expected outputs for command that is being sent

        Returns:


        """
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
