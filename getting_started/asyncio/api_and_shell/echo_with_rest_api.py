import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal
from sphero_sdk import SpheroRvrTargets


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        domain='0.0.0.0',  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and has RVR returns
        the same data. Echo can be used to check to see if RVR is connected.  RVR does not need to be awake
        for this operation. In order to test it, a node.js server must be running on the raspberry-pi connected
        to RVR.  This code is meant to be executed from a separate computer.
    """

    echo_response = await rvr.echo(
        data=[0, 1, 2],
        target=SpheroRvrTargets.primary.value
    )
    print('Echo response 1: ', echo_response)

    echo_response = await rvr.echo(
        data=[4, 5, 6],
        target=SpheroRvrTargets.secondary.value
    )
    print('Echo response 2: ', echo_response)

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
