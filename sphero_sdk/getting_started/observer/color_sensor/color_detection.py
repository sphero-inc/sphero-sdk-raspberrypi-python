import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def on_color_detected(red, green, blue, confidence, colorClassification):
    print('Color detected: ', red, green, blue, confidence, colorClassification)


def main():
    """ This program enables color detection on RVR, using its built-in sensor located on the
        down side of RVR, facing the floor.

    """
    # Wake up RVR
    rvr.wake()
    
    # Decide upon handler to be called upon color detection
    rvr.on_color_detection_notify(handler=on_color_detected)

    # Enable color detection
    rvr.enable_color_detection(enable=True)

    # Color detection is reported at 100 ms intervals. Call handler if color is detected with
    # confidence 0 or above
    rvr.enable_color_detection_notification(enable=True, interval=100, minimum_confidence_threshold=0)

    time.sleep(5)

    rvr.close()

main()