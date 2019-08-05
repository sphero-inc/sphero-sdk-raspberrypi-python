import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import ObserverSpheroRvr
from sphero_sdk import LedControlObserver
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups

rvr = ObserverSpheroRvr()

led_controller = LedControlObserver(rvr)


def main():
    """ This program has RVR drive around in different directions using raw motors.

    Note:
        To give RVR time to drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all the statements and exit without the driving ever taking place.
    """

    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Turn off all lights
    led_controller.turn_leds_off()
    time.sleep(0.5)

    # Set right headlight to red
    led_controller.set_led_rgb(RvrLedGroups.headlight_right, 255, 0, 0)
    time.sleep(1)

    # Set left headlight to green
    led_controller.set_led_color(RvrLedGroups.headlight_left, Colors.green)
    time.sleep(1)

    rvr.close()


main()
