import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RvrStreamingServices


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def imu_handler(imu_data):
    print('IMU data response: ', imu_data)


async def color_detected_handler(color_detected_data):
    print('Color detection data response: ', color_detected_data)


async def main():
    """ This program demonstrates how to disable all notifications and active commands.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    print('Initiate streaming IMU and color sensor data...')
    await rvr.enable_color_detection(is_enabled=True)
    await rvr.sensor_control.add_sensor_data_handler(
        service=RvrStreamingServices.imu,
        handler=imu_handler
    )
    await rvr.sensor_control.add_sensor_data_handler(
        service=RvrStreamingServices.color_detection,
        handler=color_detected_handler
    )
    await rvr.sensor_control.start(interval=1000)

    print('Set the control system timeout to 10s and initiate a drive command...')
    await rvr.set_custom_control_system_timeout(command_timeout=10000)
    await rvr.drive_with_yaw_normalized(
        linear_velocity=32,  # Valid linear_velocity values are in the range [-127..+127]
        yaw_angle=0  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
    )

    # Delay to allow commands to run 
    await asyncio.sleep(5)

    # Disable notifications and active commands 
    await rvr.disable_notifications_and_active_commands()
    print('Disabling notifications and active commands...')

    # Delay to allow observation that notifications and active commands have been disabled 
    await asyncio.sleep(5)

    # Restore the default timeout (2 seconds)
    await rvr.restore_default_control_system_timeout()

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
                rvr.disable_notifications_and_active_commands(),
                # Restore the default timeout (2 seconds)
                rvr.restore_default_control_system_timeout(),
                rvr.close()
            )
        )

    finally:
        if loop.is_running():
            loop.close()
