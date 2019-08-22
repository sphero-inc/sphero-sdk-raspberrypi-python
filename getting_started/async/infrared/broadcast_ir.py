import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

import asyncio

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredCodes

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """
    This program has another robot capable of infrared communication, e.g. BOLT, follow RVR.

    To try this out, write a script for your other robot that has it follow on the corresponding channel
    that RVR broadcasts on [in this case channel 0 and 1].
    Place your other robot behind RVR and run its script.
    Upon running this program RVR drives forward and the other robot follows it.
    """
    await rvr.wake()
    await asyncio.sleep(2)

    # Broadcast on channels 0 and 1. We specify the channels with the InfraredCodes enumeration
    far_code = InfraredCodes.zero
    near_code = InfraredCodes.one
    await rvr.start_robot_to_robot_infrared_broadcasting(far_code.value, near_code.value)

    # drive RVR forward for 4 seconds (one command times out after 2 seconds)
    for i in range(2):
        await rvr.raw_motors(1, 64, 1, 64)
        await asyncio.sleep(2)

    # Stops IR broadcasting
    await rvr.stop_robot_to_robot_infrared_broadcasting()


loop.run_until_complete(
    main()
)
