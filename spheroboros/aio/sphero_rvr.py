#! /usr/bin/env python3

from . import system_info
import aiohttp


class SpheroRvr:
    def __init__(self, *, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.session = aiohttp.ClientSession()

    async def get_main_app(self):
        return await system_info.get_main_app(self)
