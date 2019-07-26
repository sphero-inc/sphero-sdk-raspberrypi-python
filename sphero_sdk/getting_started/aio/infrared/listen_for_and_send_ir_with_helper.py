import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio
import time
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredControlAsync


loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop=loop
    )
)

infrared_helper = InfraredControlAsync(rvr)

async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))

async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

       To try this out, write a script for your other robot that a) broadcasts on the corresponding
       channel that RVR is set to listen to [in this case channel 0] and b) listens on the channel which
       RVR sends messages on [in this case channel 3]
    """
    await rvr.wake()

    await infrared_helper.listen_for_infrared_message(on_ir_message_received)

    while True:
        await infrared_helper.send_infrared_message([InfraredCodes.alpha, InfraredCodes.bravo, InfraredCodes.charlie, InfraredCodes.delta], strength=64)
        asyncio.sleep(0.2)

try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
