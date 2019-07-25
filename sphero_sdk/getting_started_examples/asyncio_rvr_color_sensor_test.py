import asyncio
import time

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(dal=SerialAsyncDal(loop=loop))


async def on_color_detected(red, green, blue, confidence, colorClassification):
    print('Detected: ', red, green, blue, confidence, colorClassification)


async def main():
    await rvr.wake()
    await rvr.on_color_detection_notify(handler=on_color_detected)
    await rvr.enable_color_detection(enable=True)
    await rvr.enable_color_detection_notification(enable=True, interval=100, minimum_confidence_threshold=0)


try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
