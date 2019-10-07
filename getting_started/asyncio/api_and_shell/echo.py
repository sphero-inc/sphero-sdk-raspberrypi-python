import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrTargets


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and RVR returns
        the same data. Echo can be used to check to see if RVR is connected and awake.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    echo_response = await rvr.echo(
        data=[0, 2, 4, 8, 16, 32, 64, 128, 255],
        target=SpheroRvrTargets.primary.value
    )
    print('Echo response: ', echo_response)

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
