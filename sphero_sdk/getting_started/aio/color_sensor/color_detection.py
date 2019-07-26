import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio
import time

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchornous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object, and pass in a SerialAsyncDal object, which in turn takes a reference
# to the asynchronous program loop
rvr = AsyncSpheroRvr(
    dal = SerialAsyncDal(
        loop
    )
)

async def on_color_detected(red, green, blue, confidence, colorClassification):
    print('Color detected: ', red, green, blue, confidence, colorClassification)


async def main():
    """ This program enables color detection on RVR, using its built-in sensor located on the
    down side of RVR, facing the floor.

    """
    # Wake up RVR
    await rvr.wake()

    # Decide upon handler to be called upon color detection
    await rvr.on_color_detection_notify(handler=on_color_detected)

    # Enable color detection
    await rvr.enable_color_detection(enable=True)

    # Color detection is reported at 100 ms intervals. Call handler if color is detected with
    # confidence 0 or above
    await rvr.enable_color_detection_notification(enable=True, interval=100, minimum_confidence_threshold=0)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
