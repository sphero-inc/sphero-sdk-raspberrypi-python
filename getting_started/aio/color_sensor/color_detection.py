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


async def on_color_detected(red, green, blue, confidence, colorClassification):
    print('Color detected: ', red, green, blue, confidence, colorClassification)


async def main():
    """ This program uses the color sensor on RVR (located on the down side of RVR, facing the floor) to report colors detected.
        To exit program, press <CTRL-C>

    """
    # Wake up RVR
    await
    rvr.wake()

    # Give RVR time to wake up
    await
    asyncio.sleep(2)

    # Register handler to be called when message is received
    await
    rvr.on_color_detection_notify(handler=on_color_detected)

    await
    rvr.enable_color_detection(enable=True)

    # Color detection is reported at 100 ms intervals. Handler is called only if color is detected with
    # confidence level  0 or above
    await
    rvr.enable_color_detection_notification(enable=True, interval=100, minimum_confidence_threshold=0)


try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
