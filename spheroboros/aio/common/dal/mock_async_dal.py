#! /usr/bin/env python3

import asyncio
import random
import string
from spheroboros.aio.common.dal.async_dal_base import AsyncDalBase


class MockAsyncDal(AsyncDalBase):
    def __init__(self):
        AsyncDalBase.__init__(self)

    async def send_command(self, did, cid, target,
                           timeout=None, inputs=[], outputs=[]):
        response_list = [None]*len(outputs)
        for param in outputs:
            if param.size == 1:
                response_list[param.index] = self.random_value(param.data_type)
            else:
                response_list[param.index] = self.random_list(
                        param.data_type, param.size
                )

        return tuple(response_list) if response_list is not {} else None

    async def on_command(self, did, cid, target, handler,
                         timeout=None, outputs=[]):
        async def coro(timeout):
            await asyncio.sleep(timeout)

        task = asyncio.ensure_future(coro(timeout))

        while not task.done():
            json = {}
            for param in outputs:
                if param.size == 1:
                    json[param.name] = self.random_value(param.data_type)
                else:
                    json[param.name] = self.random_list(
                        param.data_type,
                        param.size
                    )
            try:
                await handler(**json)
            except Exception as e:
                pass

            await asyncio.sleep(timeout)  # Maybe should be configurable

    def random_value(self, data_type):
        if data_type == 'uint8_t':
            return random.randint(0, 255)

        if data_type == 'uint16_t':
            return random.randint(256, 65535)

        if data_type == 'uint32_t':
            return random.randint(65535, 4294967295)

        if data_type == 'uint64_t':
            return random.randint(4294967296, 18446744073709551615)

        if data_type == 'int8_t':
            return random.randint(-128, -1)

        if data_type == 'int16_t':
            return random.randint(-32768, -129)

        if data_type == 'int32_t':
            return random.randint(-2147483648, -32769)

        if data_type == 'int64_t':
            return random.randint(-9223372036854775808, -2147483649)

        if data_type == 'float':
            return random.random()

        if data_type == 'double':
            return random.random()

        if data_type == 'bool':
            return random.choice((True, False))

        if data_type == 'std::string':
            return ''.join(
                random.choice(string.ascii_letters) for x in range(20)
            )

        raise ValueError

    def random_list(self, data_type, size):
        return [self.random_value(data_type) for x in range(size)]
