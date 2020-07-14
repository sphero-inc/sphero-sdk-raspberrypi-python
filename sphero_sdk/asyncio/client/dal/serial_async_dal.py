#! /usr/bin/env python3

import logging
from sphero_sdk.common.client.dal.sphero_dal_base import SpheroDalBase
from sphero_sdk.asyncio.server import SerialSpheroPort, Parser, Handler
from sphero_sdk.common.protocol import Message, ErrorCode

logger = logging.getLogger(__name__)


class SerialAsyncDal(SpheroDalBase, SerialSpheroPort):
    """
    """

    def __init__(self, loop=None, port_id='/dev/ttyS0', baud=115200):
        SpheroDalBase.__init__(self)
        SerialSpheroPort.__init__(
            self,
            loop,
            1,
            Parser,
            Handler,
            port_id,
            baud
        )

    async def close(self):
        SerialSpheroPort.close(self)

    async def send_command(self, did, cid, seq, target, timeout=None, inputs=[], outputs=[]):
        """Creates a Message object using the provided parameters and creates response handler that
        if a response is requested.

        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            seq (uint8): Sequence Number
            target (uint8): 1 - Nordic; 2 - ST
            timeout (uint8): Time in seconds to wait for a response, if one is requested. Otherwise, ignored.
            inputs (list(Parameter)): Inputs for command that is being sent
            outputs (list(Parameter)): Expected outputs for command that is being sent

        Returns:
            The result of the response_handler, or None if a response_handler
            was not provided
        """

        message = Message()
        message.did = did
        message.cid = cid
        message.seq = seq
        message.target = target
        message.is_activity = True
        message.requests_response = len(outputs) > 0 or self.request_error_responses_only

        # Messages that already request a response due to expected outputs don't need this
        # extra flag. They will automatically respond with errors if any are generated.
        # This flag is meant only for commands with no expected output.
        message.requests_error_response = self.request_error_responses_only if len(outputs) == 0 else False

        for param in inputs:
            message.pack(param.data_type, param.value)

        logger.debug('Message created: %s', message)

        def response_handler(message):
            response_dictionary = {}
            if len(outputs) > 0:
                for param in sorted(outputs, key=lambda x: x.index):
                    response_dictionary[param.name] = message.unpack(
                        param.data_type,
                        count=param.size
                    )

            debug_str = 'Response_handler invoked for DID: 0x{:2x} CID: 0x{:2x}.'.format(did, cid)
            return_str = 'Returning: %s'.format(response_dictionary) if len(outputs) > 0 else None
            logger.debug('{} {}'.format(debug_str, return_str))

            return response_dictionary

        return await self.handler.send_command(
            message,
            response_handler=response_handler if message.requests_response else None,
            timeout=timeout
        )

    async def on_command(self, did, cid, target, handler, timeout=None, outputs=[]):
        """Creates a wrapper to unpack response data and invoke the provided handler.
        Calls handler.add_command_worker() using parameters and wrapper() as inputs

        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            target (uint8): 1 - Nordic; 2 - ST
            handler (function): Callback function
            timeout (uint8): Timeout in seconds
            outputs (list): Expected outputs for command that is being sent

        """
        async def wrapper(msg):
            if len(outputs) > 0:
                response_dictionary = {}
                for param in sorted(outputs, key=lambda x: x.index):
                    response_dictionary[param.name] = msg.unpack(
                        param.data_type,
                        count=param.size
                    )

                logger.debug('Command response wrapper invoked, returning: {}'.format(response_dictionary))
                await handler(response_dictionary)
            else:
                logger.debug('No outputs expected, invoking callback.')
                await handler()

            return ErrorCode.success, bytearray()

        logger.debug('Command worker added for DID:{} CID:{} Target:{}'.format(did, cid, target))

        self.handler.add_command_worker(did, cid, target, wrapper)