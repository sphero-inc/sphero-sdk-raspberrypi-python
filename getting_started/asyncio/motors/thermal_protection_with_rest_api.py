import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal
from sphero_sdk import RawMotorModesEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        domain='0.0.0.0',  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)


async def thermal_protection_handler(response):
    print('Motor thermal protection response:', response)


async def main():
    """ This program demonstrates how to register a handler for a motor thermal protection notification, in the event
        RVR's motors are at risk of overheating.  In order to receive the notification, RVR's motors must be heavy use
        for an extended period.  In order to test it, a node.js server must be running on the raspberry-pi connected
        to RVR.  This code is meant to be executed from a separate computer.
    """

    await rvr.wake()

    await rvr.enable_motor_thermal_protection_status_notify(is_enabled=True)

    await rvr.on_motor_thermal_protection_status_notify(handler=thermal_protection_handler)

    # Give RVR time to wake up
    await asyncio.sleep(1)

    print('Press CTRL+C to stop this program anytime.')

    # Allow RVR to drive infinitely
    while True:
        await rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,
            left_speed=255,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.reverse.value,
            right_speed=255  # Valid speed values are 0-255
        )

        await asyncio.sleep(1)


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
