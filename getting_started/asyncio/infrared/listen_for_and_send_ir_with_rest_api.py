import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

import asyncio

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",  # RVR's prefix is RV
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def on_ir_message_received(response):
    print('Response data for IR message received:',response)


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


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        loop.run_until_complete(
            rvr.close()
        )

        if loop.is_running():
            loop.close()
