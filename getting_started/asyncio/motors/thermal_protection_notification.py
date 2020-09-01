import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import TemperatureSensorsEnum

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

async def thermal_protection_handler(response):
    print('Motor thermal protection response:', response)


async def main():
    """ This program demonstrates how to register a handler for a motor thermal protection notification, in the event
        RVR's motors are at risk of overheating.  In order to receive the notification, RVR's motors must be heavily
        used for an extended period.

        For visibility into the motor temperatures, they are printed to the console every minute.
    """

    printing_loop_counter=9;

    await rvr.wake()

    await rvr.enable_motor_thermal_protection_status_notify(is_enabled=True)

    await rvr.on_motor_thermal_protection_status_notify(handler=thermal_protection_handler)

    # Give RVR time to wake up
    await asyncio.sleep(1)

    print('Press CTRL+C to stop this program anytime.')

    # Allow RVR to drive infinitely
    while True:
        await rvr.drive_tank_normalized(
            left_velocity=127, # Valid linear velocity values are [-127..127]
            right_velocity=-127 # Valid linear velocity values are [-127..127]
        )

        await asyncio.sleep(1)

        printing_loop_counter += 1
        if(++printing_loop_counter>=10):
            # It's been 1 minute.  Zero the counter
            printing_loop_counter = 0

            # Query the temperature
            response = await rvr.get_temperature(
                id0=TemperatureSensorsEnum.left_motor_temperature.value,
                id1=TemperatureSensorsEnum.right_motor_temperature.value
            )

            # 2 Decimal places are displayed only to make changes more visible.
            # Motor thermal modeling is not actually that precise in practice.
            print("L={0:.2f}C, R={1:.2f}C".format(response["temp0"], response["temp1"]))



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
