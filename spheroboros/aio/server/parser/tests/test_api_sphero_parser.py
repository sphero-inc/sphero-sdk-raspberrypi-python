#!/usr/bin/env python3

import asyncio
from parser.api_sphero_parser import Parser
from protocol.api_sphero_message import Message


def test_api_sphero_parser():
    loop = asyncio.get_event_loop()
    fut = asyncio.Future()

    message = Message()
    message.requests_response = True
    message.target = 10
    message.source = 20
    message.did = 30
    message.cid = 40
    message.seq = 50

    message.pack_bytes(bytearray.fromhex('ABCDEF'))

    async def message_handler(msg):
        print("Received Message: {}".format(msg))
        assert msg.requests_response
        assert msg.has_target
        assert msg.has_source
        assert msg.did == 30
        assert msg.cid == 40
        assert msg.seq == 50
        assert msg.unpack_uint8() == 0xAB
        assert msg.unpack_uint8() == 0xCD
        assert msg.unpack_uint8() == 0xEF
        fut.set_result('SUCCESS')

    async def error_handler(buf):
        print("Bad Message: {}".format(buf))
        fut.set_exception('FAILURE')

    async def future_timeout(future):
        try:
            await asyncio.wait_for(future, timeout=1)
        except asyncio.TimeoutError:
            pass

    parser = Parser(message_handler, error_handler)
    buf = message.serialise()
    print("Feed Message: {}".format(buf.hex()))
    new_msg = Message.from_buffer(buf)
    print("Deserialise Message: {}".format(new_msg))
    parser.feed(message.serialise())
    loop.run_until_complete(future_timeout(fut))
    assert fut.result() == 'SUCCESS'
