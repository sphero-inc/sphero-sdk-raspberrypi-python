import os
import sys
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


async def infrared_message_received_handler(infrared_message):
    print('Infrared message response: ', infrared_message)


async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.on_robot_to_robot_infrared_message_received_notify(handler=infrared_message_received_handler)

    await rvr.enable_robot_infrared_message_notify(is_enabled=True)

    infrared_code = 3
    strength = 64

    while True:
        await rvr.send_infrared_message(
            infrared_code=infrared_code,
            front_strength=strength,
            left_strength=strength,
            right_strength=strength,
            rear_strength=strength
        )

        print('Infrared message sent with code: {0}'.format(infrared_code))

        await asyncio.sleep(2)


if __name__ == '__main__':
    try:
        asyncio.ensure_future(
            main()
        )
        loop.run_forever()

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

