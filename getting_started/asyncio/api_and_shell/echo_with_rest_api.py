import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal
from sphero_sdk.common.log_level import LogLevel

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",  # RVR's prefix is RV
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    ),
    log_level=LogLevel.Debug_Verbose
)


async def main():
    """
    This program demonstrates how to use the echo command, which sends data to RVR and has RVR returns
    the same data. Echo can be used to check to see if RVR is connected and awake.  In order to test it,
    a node.js server must be running on the raspberry-pi connected to RVR.  This code is meant to be
    executed from a separate computer.

    """
    response = await rvr.echo([1], target=2)
    print(response)

    await asyncio.sleep(1)

    response = await rvr.echo([2], target=2)
    print(response)

    await asyncio.sleep(1)


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
