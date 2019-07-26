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
    await rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)

    # Listen for IR messages of code 0x01 for the max amount of time
    await rvr.listen_for_robot_to_robot_infrared_message(0x01, 0xffffffff)

    # Send IR msg with code 0x01 at maximum strength from the front, rear, left and right
    while True:
        await rvr.send_robot_to_robot_infrared_message(0x03, 255, 255, 255, 255)
        await asyncio.sleep(0.2)

try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
