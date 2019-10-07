import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def sensor_data_handler(sensor_data):
    print('Sensor data response: ', sensor_data)


def main():
    """ This program demonstrates how to update sensor streaming parameters at runtime.
    """

    try:
        rvr.wake()

        # give RVR time to wake up
        time.sleep(2)

        print('----------', 'Enabling IMU at 100 ms', '----------')

        rvr.sensor_control.add_sensor_data_handler(sensor_data_handler)

        rvr.sensor_control.streaming_interval = 100

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

        rvr.sensor_control.enable('IMU')

        # delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Updating interval to 1000 ms', '----------')

        rvr.sensor_control.streaming_interval = 1000

        # delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Adding ambient light and velocity sensor streams', '----------')

        rvr.sensor_control.enable(
            'AmbientLight',
            'Velocity'
        )

        # delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Disabling IMU sensor stream and updating interval to 100 ms', '----------')

        rvr.sensor_control.disable('IMU')

        # delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Disabling all services', '----------')

        rvr.sensor_control.disable_all()

        # delay to allow RVR to stream sensor data
        time.sleep(5)

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
