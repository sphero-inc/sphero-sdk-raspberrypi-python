#!/usr/bin/env python3

from port.uart_sphero_port import UARTSpheroPort
from parser.sphero_parser_base import SpheroParserBase
from handler.sphero_handler_base import SpheroHandlerBase
import asyncio


fut = asyncio.Future()


class Parser(SpheroParserBase):
    def __init__(self, message_handler, error_handler):
        SpheroParserBase.__init__(self, message_handler, error_handler)
        self.buf = bytearray()

    def feed(self, data):
        self.buf += data
        if '\n' in self.buf.decode():
            self.buf.clear()
            fut.set_result("Done!")
        return []

class Handler(SpheroHandlerBase):
    def __init__(self, port):
        SpheroHandlerBase.__init__(self, port)

    async def message_handler(msg):
        pass

    async def error_handler(msg):
        pass


async def send_test(port):
    class Message:
        def __init__(self, val):
            self.val = val

        def serialise(self):
            return self.val.encode()

    msg = Message("Hello Sphero!\r\n")
    port.send(msg)


async def future_timeout():
    try:
        await asyncio.wait_for(fut, timeout=5)
    except asyncio.TimeoutError:
        pass


def test_uart_sphero_port():
    loop = asyncio.get_event_loop()
    port = UARTSpheroPort(
            loop,
            1,
            Parser,
            Handler,
            '/dev/ttyS0',
            baud=115200)

    asyncio.ensure_future(send_test(port))

    try:
        loop.run_until_complete(future_timeout())
    except KeyboardInterrupt:
        loop.close()

    port.close()

    assert fut.cancelled() is not True
    assert fut.result() == "Done!"
