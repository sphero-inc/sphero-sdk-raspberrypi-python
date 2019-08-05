import sys

import asyncio
import sphero_sdk 

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal = SerialAsyncDal(
        loop
    )
)

async def deep_sleep_rvr():
    print("entering deep sleep")
    await rvr.enter_deep_sleep(2)

async def soft_sleep_rvr():
    print("entering soft sleep")
    await rvr.enter_soft_sleep()

async def wake_up_rvr():
    print("wake up!")
    await rvr.wake()

if sys.argv[1] == '1':
    func = wake_up_rvr
elif sys.argv[1] == '2':
    func = soft_sleep_rvr
elif sys.argv[1] == '3':
    func = deep_sleep_rvr
else:
    raise KeyError

loop.run_until_complete(
    asyncio.gather(
      func()
    )
)

loop.stop()
loop.close()
