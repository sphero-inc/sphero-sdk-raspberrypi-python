import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def will_sleep_handler():
    print('RVR is about to sleep...')

    # here we could issue a command to RVR, e.g. wake() such that the sleep timer is reset


async def did_sleep_handler():
    print('RVR is asleep...')


async def main():
    """ This program demonstrates how to register handlers for a) the event received 10 seconds
        before RVR will sleep unless some new command is issued and b) the event received
        when RVR does go to sleep.

        Note that these notifications are received without the need to enable them on the robot.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.on_will_sleep_notify(handler=will_sleep_handler)
    await rvr.on_did_sleep_notify(handler=did_sleep_handler)

    # sleep for 310 seconds such that we see the aforementioned events have time to occur
    await asyncio.sleep(310)

    await rvr.close()


if __name__ == '__main__':
    loop.run_until_complete(
        main()
    )

    if loop.is_running():
        loop.stop()

    loop.close()
