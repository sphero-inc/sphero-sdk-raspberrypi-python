import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

import asyncio

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))


async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

    To try this out, write a script for your other robot that a) broadcasts on the corresponding
    channel that RVR is set to listen to [in this case channel 0] and b) listens on the channel which
    RVR sends messages on [in this case channel 3]
    """

    await rvr.wake()

    enabled = True
    await rvr.enable_robot_infrared_message_notify(enabled)

    # Register handler to be called when message is received
    await rvr.on_robot_to_robot_infrared_message_received_notify(on_ir_message_received)

    # Send infrared message with code 3 at maximum strength from the front, rear, left and right sensor respectively
    infrared_code = 3
    strength = 64
    while True:
        await rvr.send_infrared_message(infrared_code, strength, strength, strength, strength)
        print("message sent with code {}".format(infrared_code))
        await asyncio.sleep(0.2)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
