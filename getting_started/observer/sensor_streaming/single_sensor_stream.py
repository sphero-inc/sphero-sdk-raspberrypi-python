import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_sensor_streaming_data(response):
    print(response)


def get_single_sensor_stream():
    """This program enables a single sensor stream that will be printed to the console.

    """
    try:
        # Wake up RVR
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Add a callback to receive sensor stream data
        rvr.sensor_control.add_sensor_data_handler(on_sensor_streaming_data)

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
        rvr.sensor_control.enable("Accelerometer")

        # Allow this program to run until a keyboard interrupt is detected
        while True:
            time.sleep(1)
            # raise Exception("whoops")
    except KeyboardInterrupt:
        print("Program terminated with keyboard interrupt.")
    finally:
        # Properly shuts down the RVR serial port.
        rvr.close()


if __name__ == "__main__":
    get_single_sensor_stream()
