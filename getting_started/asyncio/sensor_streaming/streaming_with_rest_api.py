import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010
    )
)


async def battery_state_handler(response):
    print('battery state response', response)


async def sensor_stream_handler(response):
    print('sensor stream response', response)


async def main():
    """
    This program has RVR drive around in different directions using the function raw_motors.

    Note:
        To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would
        go on and execute all the statements and exit without the driving ever taking place.
    """
    await rvr.wake()

    response = await rvr.get_main_application_version(target=1)
    print('version response', response)

    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)
    await rvr.on_battery_voltage_state_change_notify(battery_state_handler)

    await rvr.enable_color_detection(is_enabled=True)
    await rvr.sensor_control.add_sensor_data_handler(sensor_stream_handler)
    await rvr.sensor_control.enable('ColorDetection', 'Velocity', 'IMU')


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        loop.run_until_complete(
            rvr.close()
        )

        if loop.is_running():
            loop.close()
