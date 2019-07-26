# NOTE: when rvr.listen_for_robot_to_robot_infrared_message is called, all channels are listen at
# The infrared code passed in as first argument has no effect
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
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

    To try this out, write a script for your other robot that a) broadcasts on the corresponding
    channel that RVR is set to listen to [in this case channel 0] and b) listens on the channel which
    RVR sends messages on [in this case channel 3]
    """
    await rvr.wake()

    # Register handler to be called when message is received
    await rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)

    # Note: The IR code is passed in as a bit mask
    # In this case, we want to listen to message 0, so the first bit is set
    # If you want to listen to message 6, set infrared_code to 0x01000000
    infrared_code = 0x01
    await rvr.listen_for_robot_to_robot_infrared_message(infrared_code, 0xffffffff)

    # Send IR msg with code 0x01 at maximum strength from the front, rear, left and right
    # The IR code is given directly, i.e. is a number between 0 - 7
    while True:
        await rvr.send_robot_to_robot_infrared_message(0x3, 64, 64, 64, 64)
        await asyncio.sleep(0.2)

try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
