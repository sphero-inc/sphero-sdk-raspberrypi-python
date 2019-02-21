# Sphero Python Client Library

This package provides two ways with interacting with the Sphero API Service

## Simple: Blocking (uses requests)
The first is a simpler, blocking style that uses requests library
```python
#!/usr/bin/env python3

from spheroboros import SpheroRvr

rvr = SpheroRvr()

major, minor, build = rvr.get_main_app()

print('{}.{}.{}'.format(major, minor, build))
```

## Slightly More Complex: Coroutines (uses asyncio + aiohttp)
Do A bunch of stuff in coroutines!
```python
#! /usr/bin/env python3

from spheroboros import AsyncSpheroRvr
import asyncio

rvr = AsyncSpheroRvr()
loop = asyncio.get_event_loop()


async def do_stuff_with_rvr():
    major, minor, build = await rvr.get_main_app()
    print('{}.{}.{}'.format(major, minor, build))


async def do_other_stuff_with_rvr():
    await set_led_with_8_bit_bitmask()


loop.run_until_complete(
    asyncio.gather(
        do_stuff_with_rvr(),
        do_other_stuff_with_rvr()
    )
)

loop.run_until_complete(rvr.session.close())
```
