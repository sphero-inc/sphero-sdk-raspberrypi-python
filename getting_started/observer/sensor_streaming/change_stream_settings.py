import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrStreamingServices


rvr = SpheroRvrObserver()


def imu_handler(imu_data):
    print('IMU data response: ', imu_data)


def ambient_light_handler(ambient_light_data):
    print('Ambient data response:', ambient_light_data)


def velocity_handler(velocity_data):
    print('Velocity data response:', velocity_data)


def main():
    """ This program demonstrates how to update sensor streaming parameters at runtime.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        print('----------', 'Enabling IMU at 100 ms', '----------')

        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.imu,
            handler=imu_handler
        )
        rvr.sensor_control.start(interval=100)

        # Delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Updating interval to 1000 ms', '----------')

        rvr.sensor_control.stop()
        rvr.sensor_control.start(interval=1000)

        # Delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Adding ambient light and velocity sensor streams', '----------')

        rvr.sensor_control.stop()
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.ambient_light,
            handler=ambient_light_handler
        )
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.velocity,
            handler=velocity_handler
        )
        rvr.sensor_control.start(interval=1000)

        # Delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Disabling IMU sensor stream and updating interval to 100 ms', '----------')

        rvr.sensor_control.stop()
        rvr.sensor_control.remove_sensor_data_handler(service=RvrStreamingServices.imu)
        rvr.sensor_control.start(interval=100)

        # Delay to allow RVR to stream sensor data
        time.sleep(5)

        print('----------', 'Clearing all services', '----------')

        rvr.sensor_control.clear()

        # Delay to allow RVR to stream sensor data
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        if len(rvr.sensor_control.enabled_sensors) > 0:
            rvr.sensor_control.clear()

        # Delay to allow RVR issue command before closing
        time.sleep(.5)

        rvr.close()


if __name__ == '__main__':
    main()
