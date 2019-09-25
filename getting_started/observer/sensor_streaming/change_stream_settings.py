import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_sensor_streaming_data(response):
    print(response)


def run_sample_sequence():
    """This program demonstrates how to update sensor streaming parameters at runtime.

    """
    try:
        # Wake up RVR
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)
        print("----------", "Enabling IMU at 100 ms", "----------")

        # Add a callback to receive sensor stream data
        rvr.sensor_control.add_sensor_data_handler(on_sensor_streaming_data)

        # Set a slow streaming interval (every 500 ms)
        rvr.sensor_control.streaming_interval = 100

        # Enable a single sensor. Supported sensors are:
        # "ColorDetection"
        # "AmbientLight"
        # "Quaternion"
        # "IMU"
        # "Accelerometer"
        # "Gyroscope"
        # "Locator"
        # "Velocity"
        # "Speed"
        # "CoreTime"
        rvr.sensor_control.enable("IMU")

        # Pause this function for 5 seconds
        time.sleep(5)
        print("----------", "Updating interval to 1000 ms", "----------")

        # Update the streaming interval to 100ms
        rvr.sensor_control.streaming_interval = 1000

        # Sleep for 5 seconds before calling next function
        time.sleep(5)
        print("----------", "Adding color detection and velocity sensor streams", "----------")

        # Add 2 more services
        rvr.sensor_control.enable("AmbientLight", "Velocity")

        # Sleep for another 5 seconds
        time.sleep(5)
        print("----------", "Disabling IMU sensor stream and updating interval to 100", "----------")

        # Disable IMU service
        rvr.sensor_control.disable("IMU")

        # Sleep for another 5 seconds
        time.sleep(5)
        print("----------", "Disabling all services", "----------")

        # Disable all services
        rvr.sensor_control.disable_all()

    except KeyboardInterrupt:
        print("Program terminated with keyboard interrupt.")
    finally:
        # Properly shuts down the RVR serial port.
        rvr.close()


if __name__ == "__main__":
    run_sample_sequence()
