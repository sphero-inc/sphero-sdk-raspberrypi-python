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


async def main():
    """ This program demonstrates how to get motor thermal protection status, in the event RVR's motors have already
        been stopped to prevent overheating.  This can be used to check if the motors are no longer in a thermal
        protection state. RVR does not need to be awake in order to run this operation.
    """

    response = await rvr.get_motor_thermal_protection_status()
    print('Thermal protection status response', response)

    # Delay to allow the callback to be invoked
    await asyncio.sleep(2)

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
