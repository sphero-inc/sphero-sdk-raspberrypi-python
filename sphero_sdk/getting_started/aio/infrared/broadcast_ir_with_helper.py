import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio
import time
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredControlAsync
from sphero_sdk import InfraredCodes


loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop=loop
    )
)

infrared_helper = InfraredControlAsync(rvr)

async def main():
    """ This program has another robot capable of infrared communication, e.g. BOLT, follow RVR.

        To try this out, write a script for your other robot that has it follow on the corresponding channel
        that RVR broadcasts on [in this case channel 0 and 1].
        Place your other robot behind RVR and run its script.
        Upon running this program RVR drives forward and the other robot follows it.
    """
    await rvr.wake()

    # Broadcast on channels 0, 1, 2, and 3. Here, we specify the channels with the enumeration InfraredCodes
    await infrared_helper.start_infrared_broadcasting([InfraredCodes.alpha, InfraredCodes.charlie], [InfraredCodes.bravo, InfraredCodes.delta])

    await rvr.raw_motors(1, 64, 1, 64)
    await asyncio.sleep(1)

    await infrared_helper.stop_infrared_broadcasting()

try:
    asyncio.ensure_future(main())
    loop.run_forever()

except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
