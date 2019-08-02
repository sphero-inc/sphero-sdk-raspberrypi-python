# TODO: understand how to use get_bot_to_bot_infrared_readings() and demonstrate
import time

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))


async def main():
    """ This program does... TODO

    """
    await
    rvr.wake()

    while True:
        reading = await
        rvr.get_bot_to_bot_infrared_readings()
        print(reading)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
