import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal
from sphero_sdk import RvrStreamingServices


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        domain='0.0.0.0',  # Add your raspberry-pi's IP address here
        port=2010
    )
)


async def imu_handler(imu_data):
    print('IMU data response: ', imu_data)


async def ambient_light_handler(ambient_light_data):
    print('Ambient data response:', ambient_light_data)


async def velocity_handler(velocity_data):
    print('Velocity data response:', velocity_data)


async def main():
    """ This program has RVR drive around in different directions using the function raw_motors.

        Note:
            To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would
            go on and execute all the statements and exit without the driving ever taking place.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    print('----------', 'Enabling IMU at 100 ms', '----------')

    await rvr.sensor_control.add_sensor_data_handler(
        service=RvrStreamingServices.imu,
        handler=imu_handler
    )
    await rvr.sensor_control.start(interval=100)

    # Delay to allow RVR to stream sensor data
    await asyncio.sleep(5)

    print('----------', 'Updating interval to 1000 ms', '----------')

    await rvr.sensor_control.stop()
    await rvr.sensor_control.start(interval=1000)

    # Delay to allow RVR to stream sensor data
    await asyncio.sleep(5)

    print('----------', 'Adding ambient light and velocity sensor streams', '----------')

    await rvr.sensor_control.stop()
    await rvr.sensor_control.add_sensor_data_handler(
        service=RvrStreamingServices.ambient_light,
        handler=ambient_light_handler
    )
    await rvr.sensor_control.add_sensor_data_handler(
        service=RvrStreamingServices.velocity,
        handler=velocity_handler
    )
    await rvr.sensor_control.start(interval=1000)

    # Delay to allow RVR to stream sensor data
    await asyncio.sleep(5)

    print('----------', 'Disabling IMU sensor stream and updating interval to 100 ms', '----------')

    await rvr.sensor_control.stop()
    await rvr.sensor_control.remove_sensor_data_handler(service=RvrStreamingServices.imu)
    await rvr.sensor_control.start(interval=100)

    # Delay to allow RVR to stream sensor data
    await asyncio.sleep(5)

    print('----------', 'Clearing all services', '----------')

    await rvr.sensor_control.clear()

    # Delay to allow RVR to stream sensor data
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
            asyncio.gather(
                rvr.sensor_control.clear(),
                rvr.close()
            )
        )

    finally:
        if loop.is_running():
            loop.close()
