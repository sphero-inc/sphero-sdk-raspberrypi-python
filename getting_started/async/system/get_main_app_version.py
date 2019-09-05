import sys
import os
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


async def get_main_app_version():
    """This program demonstrates how to obtain the firmware version for a specific processor.

    """

    response = await rvr.get_main_application_version(target=1, timeout=5)
    print ('response contents:', response)
    major, minor, revision = response['major'], response['minor'], response['revision']
    print('{} {}.{}.{}'.format("Nordic", major, minor, revision))

    response = await rvr.get_main_application_version(target=2, timeout=5)
    print('response contents:', response)
    major, minor, revision = response['major'], response['minor'], response['revision']
    print('{} {}.{}.{}'.format("ST", major, minor, revision))


loop.run_until_complete(
    asyncio.gather(
        get_main_app_version()
    )
)

loop.stop()
loop.close()
