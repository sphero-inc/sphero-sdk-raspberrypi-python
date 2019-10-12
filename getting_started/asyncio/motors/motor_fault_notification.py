import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RawMotorModesEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def motor_fault_handler(response):
    print('Motor fault response:', response)


async def main():
    """ In the rare event that a motor fault occurs while operating RVR, this program demonstrates how to register
        a handler for a motor fault notification.  In order to receive a motor fault notification, RVR's motors
        must be in use.
    """

    await rvr.wake()

    await rvr.enable_motor_fault_notify(is_enabled=True)

    await rvr.on_motor_fault_notify(handler=motor_fault_handler)

    # Give RVR time to wake up
    await asyncio.sleep(1)

    await rvr.raw_motors(
        left_mode=RawMotorModesEnum.forward.value,
        left_speed=128,  # Valid speed values are 0-255
        right_mode=RawMotorModesEnum.forward.value,
        right_speed=128  # Valid speed values are 0-255
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

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
