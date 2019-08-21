import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

import asyncio

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredCodes
from sphero_sdk import InfraredControlAsync

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

infrared_controller = InfraredControlAsync(rvr)


async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))


async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

       To try this out, write a script for your other robot that a) broadcasts on any channel and b) listens on the
       channel which RVR sends messages on [in this case channel 0, 1, 2, and 3]
    """
    await rvr.wake()

    await infrared_controller.listen_for_infrared_message(on_ir_message_received)

    codes = [InfraredCodes.zero, InfraredCodes.one, InfraredCodes.two, InfraredCodes.three]
    while True:
        await infrared_controller.send_infrared_messages(codes, strength=64)
        print("message sent with codes {}".format([code.value for code in codes]))
        await asyncio.sleep(0.5)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
