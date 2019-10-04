import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def sensor_data_handler(sensor_data):
    print('Sensor data response: ', sensor_data)


def main():
    """ This program demonstrates how to enable a single sensor to stream.
    """

    try:
        rvr.wake()

        # give RVR time to wake up
        time.sleep(2)

        rvr.sensor_control.add_sensor_data_handler(sensor_data_handler)

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

        rvr.sensor_control.enable('Accelerometer')

        while True:
            # delay to allow RVR to stream sensor data
            time.sleep(1)

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
