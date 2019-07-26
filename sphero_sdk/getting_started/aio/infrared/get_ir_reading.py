import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio
import time
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(dal=SerialAsyncDal(loop=loop))

async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))

async def main():
    """ This program does... TODO

    """
    await rvr.wake()

    while True:
        reading = await rvr.get_bot_to_bot_infrared_readings()
        print(reading)

try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
