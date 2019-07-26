import asyncio
import time
import sys
sys.path.append('/home/pi/raspberry-pi-python')

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(dal=SerialAsyncDal(loop=loop))

async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))

async def main():
    """
    This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    RVR listens for messages and performs the action as defined by on_ir_message_received when a message is
    received.
    At the same time, RVR sends out IR messages of code 0x03 continuously.
    """
    await rvr.wake()

    # Register handler to be called when message is received
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
