import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SpheroRvrTargets
from sphero_sdk import RestfulAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        domain='0.0.0.0',  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def main():
    """ This program demonstrates how to obtain the firmware version for a specific processor.  RVR does
        not need to be awake for this operation. In order to test it, a node.js server must be running on the
        raspberry-pi connected to RVR. This code is meant to be executed from a separate computer.
    """

    nordic_main_application_version = await rvr.get_main_application_version(target=SpheroRvrTargets.primary.value)
    print('Nordic main application version (target 1): ', nordic_main_application_version)

    st_main_application_version = await rvr.get_main_application_version(target=SpheroRvrTargets.secondary.value)
    print('ST main application version (target 2): ', st_main_application_version)

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
