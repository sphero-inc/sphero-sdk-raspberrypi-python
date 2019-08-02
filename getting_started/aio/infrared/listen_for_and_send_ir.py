# NOTE: when rvr.listen_for_robot_to_robot_infrared_message is called, all channels are listen at regardless of
# infrared code passed
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
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

    To try this out, write a script for your other robot that a) broadcasts on the corresponding
    channel that RVR is set to listen to [in this case channel 0] and b) listens on the channel which
    RVR sends messages on [in this case channel 3]
    """

    await
    rvr.wake()

    # Register handler to be called when message is received
    await
    rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)

    # Listen for messages at channel 0 for the maximum amount of time possible
    # Note: The channel is given as a bit mask
    # In this case, we want to listen to channel 0, so the first bit is set to 1
    infrared_code = 0x01
    listen_duration = 0xffffffff
    await
    rvr.listen_for_robot_to_robot_infrared_message(infrared_code, listen_duration)

    # Send infrared message with code 3 at maximum strength from the front, rear, left and right sensor respectively
    infrared_code = 3
    strength = 64
    while True:
        await
        rvr.send_robot_to_robot_infrared_message(infrared_code, strength, strength, strength, strength)
        await
        asyncio.sleep(0.2)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
