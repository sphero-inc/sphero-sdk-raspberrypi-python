# TODO: upon testing, BOLT gives no response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import InfraredCodes
from sphero_sdk import InfraredControlAsync
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)

infrared_controller = InfraredControlAsync(rvr)


async def main():
    """ This program has another robot capable of infrared communication, e.g. BOLT, follow RVR.

        To try this out, write a script for your other robot that has it follow on the corresponding channel
        that RVR broadcasts on [in this case channel 0 and 1].
        Place your other robot behind RVR and run its script.
        Upon running this program RVR drives forward and the other robot follows it.
    """
    await rvr.wake()

    # Broadcast on channels 0, 1, 2, and 3. We specify the channels with the InfraredCodes enumeration
    await infrared_controller.start_infrared_broadcasting([InfraredCodes.alpha, InfraredCodes.charlie],
                                                    [InfraredCodes.bravo, InfraredCodes.delta])

    await rvr.raw_motors(1, 64, 1, 64)
    await asyncio.sleep(3)

    await infrared_controller.stop_infrared_broadcasting()


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
