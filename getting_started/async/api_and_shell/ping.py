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


async def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and has RVR returns
        the same data. Echo can be used to check to see if RVR is connected and awake.

    """
    await rvr.wake()

    response = await rvr.echo([0,2,4,8,16,32,64,128,255], target=1)
    print("Response contents: ",response)
    data = response['data']
    print("echo data:{}".format(data))


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
