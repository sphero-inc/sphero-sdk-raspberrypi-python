import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredCodes


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def infrared_message_received_handler(infrared_message):
    print('Infrared message response: ', infrared_message)


async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.infrared_control.listen_for_infrared_message(handler=infrared_message_received_handler)

    codes = [
        InfraredCodes.zero,
        InfraredCodes.one,
        InfraredCodes.two,
        InfraredCodes.three
    ]

    while True:
        await rvr.infrared_control.send_infrared_messages(
            messages=codes,
            strength=64
        )

        print('Infrared message sent with codes: {0}'.format([code.value for code in codes]))

        await asyncio.sleep(2)


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            asyncio.gather(
                rvr.stop_robot_to_robot_infrared_broadcasting(),
                rvr.close()
            )
        )

    finally:
        if loop.is_running():
            loop.close()