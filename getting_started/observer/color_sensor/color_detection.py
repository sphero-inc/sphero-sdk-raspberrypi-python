import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_color_detected(red, green, blue, confidence, colorClassificationId):
    print('Color detected: ', red, green, blue, confidence, colorClassificationId)


def main():
    """ This program uses the color sensor on RVR (located on the down side of RVR, facing the floor) to report colors detected.

    """
    # Wake up RVR
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # This enables the color sensor on RVR
    rvr.enable_color_detection(is_enabled=True)

    # Register a handler to be called when a color detection notification is received
    rvr.on_color_detection_notify(handler=on_color_detected)

    # Enable the color detection notifications with the given parameters
    rvr.enable_color_detection_notify(is_enabled=True, interval=250, minimum_confidence_threshold=0, timeout=5)

    # Allow this program to run for 10 seconds
    time.sleep(10)
    
    # Properly shuts down the RVR serial port.
    rvr.close()


if __name__ == "__main__":
    main()
