import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import InfraredCodes
from sphero_sdk import RawMotorModesEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.infrared_control.start_infrared_broadcasting(
        far_code=InfraredCodes.one,
        near_code=InfraredCodes.zero
    )

    await rvr.raw_motors(
        left_mode=RawMotorModesEnum.forward.value,
        left_speed=64,
        right_mode=RawMotorModesEnum.forward.value,
        right_speed=64
    )

    # delay to allow RVR to drive
    await asyncio.sleep(4)

    await rvr.infrared_control.stop_infrared_broadcasting()

    await rvr.close()


if __name__ == '__main__':
    loop.run_until_complete(
        main()
    )

    if loop.is_running():
        loop.stop()

    loop.close()
