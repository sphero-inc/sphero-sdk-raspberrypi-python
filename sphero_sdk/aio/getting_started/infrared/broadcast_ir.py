import asyncio
import time
import sys
sys.path.append('/home/pi/raspberry-pi-python')

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(dal=SerialAsyncDal(loop=loop))

async def main():
    """
    Place your BOLT or other robot that has a support for infrared following. Make sure to set your other robot
    to follow the channels specified below. Upon running this program RVR should drive forward and the other robot
    follow it.
    Returns:

    """
    await rvr.wake()

    await rvr.start_robot_to_robot_infrared_broadcasting(0x01, 0x02)

    await rvr.raw_motors(1, 128, 1, 128)
    await asyncio.sleep(1)

    await rvr.stop_robot_to_robot_infrared_broadcasting()

try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
