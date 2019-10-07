import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def sensor_data_handler(sensor_data):
    print('Sensor data response: ', sensor_data)


async def main():
    """ This program demonstrates how to enable multiple sensors to stream.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.sensor_control.add_sensor_data_handler(sensor_data_handler)

    # TODO: is there a constant or enum available for these?
    # Enable a single sensor. Supported sensors are:
    # 'ColorDetection'
    # 'AmbientLight'
    # 'Quaternion'
    # 'IMU'
    # 'Accelerometer'
    # 'Gyroscope'
    # 'Locator'
    # 'Velocity'
    # 'Speed'
    # 'CoreTime'

    await rvr.sensor_control.enable(
        'IMU',
        'ColorDetection',
        'Accelerometer',
        'AmbientLight'
    )

    while True:
        # delay to allow RVR to stream sensor data
        await asyncio.sleep(1)


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
