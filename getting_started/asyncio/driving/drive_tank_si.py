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
    """ This program has RVR drive around in different directions using the function drive_tank_si.
        This function commands a floating point linear velocity target for each tread in meters per second.
        Achievable velocity targets are in the range of [-1.555..1.555]
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    # drive forward, 50% speed
    await rvr.drive_tank_si_units(
        left_velocity=0.75,  # Valid velocity values are [-1.555..1.555]
        right_velocity=0.75
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # drive reverse, ~50% speed
    await rvr.drive_tank_si_units(
        left_velocity=-0.75,
        right_velocity=-0.75
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # Spin in place slowly
    await rvr.drive_tank_si_units(
        left_velocity=0.1,
        right_velocity=-0.1
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    # Spin in place quickly
    await rvr.drive_tank_si_units(
        left_velocity=-1.5,
        right_velocity=1.5
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    await rvr.drive_tank_si_units(
        left_velocity=0,
        right_velocity=0
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
