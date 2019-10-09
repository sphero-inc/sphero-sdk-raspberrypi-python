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


async def main():
    """ This program has RVR drive with how to drive RVR using the drive control helper.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.drive_control.reset_heading()

    await rvr.drive_control.drive_forward_seconds(
        speed=64,
        heading=0,  # Valid heading values are 0-359
        time_to_drive=1
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_control.drive_backward_seconds(
        speed=64,
        heading=0,  # Valid heading values are 0-359
        time_to_drive=1
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.drive_control.turn_left_degrees(
        heading=0,  # Valid heading values are 0-359
        amount=90
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
