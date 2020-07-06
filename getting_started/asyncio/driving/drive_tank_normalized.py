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
    """ This program has RVR drive around in different directions using the function drive_tank_normalized.
        This function commands a normalized linear velocity target for each tread.  Velocity targets
        are normalized in the range [-127..127]
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    # drive forward, 50% speed
    await rvr.drive_tank_normalized(
        left_velocity=64,  # Valid velocity values are [-127..127]
        right_velocity=64  # Valid velocity values are [-127..127]
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # drive reverse, 50% speed
    await rvr.drive_tank_normalized(
        left_velocity=-64,  # Valid velocity values are [-127..127]
        right_velocity=-64  # Valid velocity values are [-127..127]
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # Spin in place slowly
    await rvr.drive_tank_normalized(
        left_velocity=5,  # Valid velocity values are [-127..127]
        right_velocity=-5 # Valid velocity values are [-127..127]
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    # Spin in place quickly
    await rvr.drive_tank_normalized(
        left_velocity=-127,  # Valid velocity values are [-127..127]
        right_velocity=127  # Valid velocity values are [-127..127]
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    await rvr.drive_tank_normalized(
        left_velocity=0,  # Valid velocity values are [-127..127]
        right_velocity=0  # Valid velocity values are [-127..127]
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
