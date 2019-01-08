#! /usr/bin/env python3

from spher_io import SpheroRvr
import asyncio

rvr = SpheroRvr()
loop = asyncio.get_event_loop()


async def do_stuff_with_rvr():
    major, minor, build = await rvr.get_main_app()
    print('{}.{}.{}'.format(major, minor, build))

loop.run_until_complete(do_stuff_with_rvr())

loop.run_until_complete(rvr.session.close())
