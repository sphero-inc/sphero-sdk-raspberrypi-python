import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
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

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.on_will_sleep_notify(handler=will_sleep_handler)
    await rvr.on_did_sleep_notify(handler=did_sleep_handler)

    # The asyncio loop will run forever to give the aforementioned events time to occur


if __name__ == '__main__':
    try:
        asyncio.ensure_future(
            main()
        )
        loop.run_forever()

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
