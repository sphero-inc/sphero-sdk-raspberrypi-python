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
    await rvr.enable_color_detection(is_enabled=True)

    # Register a handler to be called when a color detection notification is received
    await rvr.sensor_control.add_sensor_data_handler(on_color_detected)

    # Enable the color detection sensor stream
    await rvr.sensor_control.enable("ColorDetection")


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.run_until_complete(rvr.close())

loop.close()
