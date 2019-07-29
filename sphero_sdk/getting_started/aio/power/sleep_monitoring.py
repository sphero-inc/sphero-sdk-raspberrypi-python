import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal = SerialAsyncDal(
        loop
    )
)


def on_about_to_enter_soft_sleep():
    print("RVR is about to enter soft sleep...")
    # Here we could issue a command to RVR, e.g. wake() such that the sleep timer is reset
    # and RVR does not go to sleep

def on_entered_soft_sleep():
    print("RVR entered soft sleep...")



async def main():
    """ This program demonstrates how to register handlers for a) the event received 10 seconds
        before RVR will enter soft sleep unless some new command is issued and b) the event received
        when RVR does enter soft sleep.

        Note that these notifications are received without the need to enable them on the robot.

    """
    await rvr.wake()

    await rvr.on_will_sleep_notify(on_about_to_enter_soft_sleep)

    await rvr.on_did_sleep_notify(on_entered_soft_sleep)

    # Sleep for 5 minutes such that we see the aforementioned events have time to occur
    await asyncio.sleep(300)


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
