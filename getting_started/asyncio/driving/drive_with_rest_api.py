import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal
from sphero_sdk import DriveFlagsBitmask


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        domain='0.0.0.0',  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def main():
    """ This program has RVR drive using the Rest API.  In order to test it, a node.js server must be running on the
        raspberry-pi connected to RVR.  This code is meant to be executed from a separate computer.

        Note:
            To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would
            go on and execute all the statements and exit without the driving ever taking place.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    await rvr.drive_with_heading(
        speed=128,  # Valid speed values are 0-255
        heading=0,  # Valid heading values are 0-359
        flags=DriveFlagsBitmask.none.value
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_with_heading(
        speed=128,  # Valid speed values are 0-255
        heading=0,  # Valid heading values are 0-359
        flags=DriveFlagsBitmask.drive_reverse.value
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_with_heading(
        speed=128,  # Valid speed values are 0-255
        heading=90,  # Valid heading values are 0-359
        flags=DriveFlagsBitmask.none.value
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_with_heading(
        speed=128,  # Valid speed values are 0-255
        heading=270,  # Valid heading values are 0-359
        flags=DriveFlagsBitmask.none.value
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_with_heading(
        speed=0,  # Valid heading values are 0-359
        heading=0,  # Valid heading values are 0-359
        flags=DriveFlagsBitmask.none.value
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
