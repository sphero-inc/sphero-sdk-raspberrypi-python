import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def sensor_data_handler(sensor_data):
    print('Sensor data response: ', sensor_data)


def main():
    """ This program demonstrates how to use the color sensor on RVR (located on the down side of RVR, facing the floor)
        to report colors detected.
    """

    try:
        rvr.wake()

        # give RVR time to wake up
        time.sleep(2)

        rvr.enable_color_detection(is_enabled=True)
        rvr.sensor_control.add_sensor_data_handler(handler=sensor_data_handler)
        rvr.sensor_control.enable('ColorDetection')     # TODO: is there a constant available for this?

        # allow this program to run for 10 seconds
        time.sleep(10)

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
