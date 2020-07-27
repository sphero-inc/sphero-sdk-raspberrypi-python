import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrStreamingServices

rvr = SpheroRvrObserver()


def imu_handler(imu_data):
    print('IMU data response: ', imu_data)


def color_detected_handler(color_detected_data):
    print('Color detection data response: ', color_detected_data)


def main():
    """ This program demonstrates how to disable all notifications and active commands.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        print('Initiate streaming IMU and color sensor data...')
        rvr.enable_color_detection(is_enabled=True)
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.imu,
            handler=imu_handler
        )
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.color_detection,
            handler=color_detected_handler
        )
        rvr.sensor_control.start(interval=1000)

        print('Set the control system timeout to 10s and initiate a drive command...')
        rvr.set_custom_control_system_timeout(command_timeout=10000)
        rvr.drive_with_yaw_normalized(
            linear_velocity=32,  # Valid linear_velocity values are in the range [-127..+127]
            yaw_angle=0  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
        )

        # Delay to allow commands to run
        time.sleep(5)

        # Disable notifications and active commands
        rvr.disable_notifications_and_active_commands()
        print('Disabling notifications and active commands...')

        # Delay to allow observation that notifications and active commands have been disabled
        time.sleep(5)

        # Restore the default timeout (2 seconds)
        rvr.restore_default_control_system_timeout()

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()