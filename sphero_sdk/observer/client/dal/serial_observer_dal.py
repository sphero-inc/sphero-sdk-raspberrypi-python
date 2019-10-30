#! /usr/bin/env python3

import logging
from sphero_sdk import ObserverParser
from sphero_sdk import SerialObserverPort
from sphero_sdk import EventDispatcher
from sphero_sdk.common.client.dal.sphero_dal_base import SpheroDalBase
from sphero_sdk.common.protocol import Message


logger = logging.getLogger(__name__)


class SerialObserverDal(SpheroDalBase):
    __slots__ = ['_port']

    def __init__(self, port_id='/dev/ttyS0', baud=115200):
        SpheroDalBase.__init__(self)
        dispatcher = EventDispatcher()
        parser = ObserverParser(dispatcher)
        self._port = SerialObserverPort(parser, port_id, baud)

    def send_command(self, did, cid, seq, target, timeout=None, inputs=[], outputs=[]):
        """Creates a Message object using the provided parameters and sends it to the serial port.

        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            seq (uint8): Sequence Number
            target (uint8): 1 - Nordic; 2 - ST
            timeout (uint8): Time in seconds to wait for a response, if one is requested. Otherwise, ignored.
            inputs (list(Parameter)): Inputs for command that is being sent
            outputs (list(Parameter)): Expected outputs for command that is being sent

        """

        # TODO: implement timeout logic, which should remove any registered callbacks if timeout occurs.
        message = Message()
        message.did = did
        message.cid = cid
        message.seq = seq
        message.target = target
        message.is_activity = True

        if seq is not None:
            message.seq = seq

        if len(outputs) > 0:
            message.requests_response = True

        for param in inputs:
            message.pack(param.data_type, param.value)

        logger.info('Sending message: %s', message)

        self._port.send(message)

    def close(self):
        """Closes the serial port, and joins the read/write thread.

        """
        self._port.close()

    def on_command(self, did, cid, target, handler=None, timeout=None, outputs=None):
        """In the observer version of the serial DAL, asyncs coming from the robot only require a registered
        callback to be dispatched back to the user.  Asyncs are enabled through a call to send_command, and
        the handler is registered with a subclass of EventDispatcher outside of the DAL.  Therefore, this method
        is not used.

        """
        pass
