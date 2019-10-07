import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",  # RVR's prefix is RV
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def main():
    """
    This program has RVR drive using the Rest API.  In order to test it, a node.js server must be running on the
    raspberry-pi connected to RVR.  This code is meant to be executed from a separate computer.

    Note:
        To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would
        go on and execute all the statements and exit without the driving ever taking place.
    """
    await rvr.wake()

    await rvr.reset_yaw()

    # drive forward
    await rvr.drive_with_heading(speed=128, heading=0, flags=0)

    await asyncio.sleep(3)

    # drive reverse
    await rvr.drive_with_heading(speed=128, heading=0, flags=1)

    await asyncio.sleep(3)


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
