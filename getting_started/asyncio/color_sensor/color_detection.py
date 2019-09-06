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


async def on_color_detected(response):
    print('Response data for color detected:',response)


async def main():
    """ This program uses the color sensor on RVR (located on the down side of RVR, facing the floor) to report colors detected.
        To exit program, press <CTRL-C>

    """
    # Wake up RVR
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(1)

    # This enables the color sensor on RVR
    await rvr.enable_color_detection(is_enabled=False)

    # Register a handler to be called when a color detection notification is received
    await rvr.on_color_detection_notify(handler=on_color_detected)

    # Enable the color detection notifications with the given parameters
    await rvr.enable_color_detection_notify(is_enabled=True, interval=250, minimum_confidence_threshold=0, timeout=5)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
