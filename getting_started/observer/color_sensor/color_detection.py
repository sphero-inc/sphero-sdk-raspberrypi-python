import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_color_detected(response):
    print('Response data for color detected:',response)


def main():
    """ This program uses the color sensor on RVR (located on the down side of RVR, facing the floor) to report colors detected.

    """
    try:
        # Wake up RVR
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # This enables the color sensor on RVR
        rvr.enable_color_detection(is_enabled=True)

        # Register a handler to be called when a color detection notification is received
        rvr.sensor_control.add_sensor_data_handler(on_color_detected)

        # Enable the color detection sensor stream
        rvr.sensor_control.enable("ColorDetection")

        # Allow this program to run for 10 seconds
        time.sleep(10)

        # Disable all services
        rvr.sensor_control.disable_all()
    except KeyboardInterrupt:
        print("Program terminated with keyboard interrupt.")
    finally:
        # Properly shuts down the RVR serial port.
        rvr.close()

if __name__ == "__main__":
    main()
