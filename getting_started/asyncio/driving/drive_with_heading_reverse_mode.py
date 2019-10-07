import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import DriveFlagsBitmask


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program has RVR drive around in different directions using the function drive_with_heading.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    await rvr.drive_with_heading(
        speed=128,
        heading=90,
        flags=DriveFlagsBitmask.drive_reverse.value
    )

    # delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_with_heading(
        speed=0,
        heading=0,
        flags=DriveFlagsBitmask.none.value
    )

    # delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        loop.run_until_complete(
            rvr.close()
        )

        if loop.is_running():
            loop.close()
