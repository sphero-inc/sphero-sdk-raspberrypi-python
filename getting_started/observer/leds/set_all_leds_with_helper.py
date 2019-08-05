import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import ObserverSpheroRvr
from sphero_sdk import LedControlObserver
from sphero_sdk import Colors


rvr = ObserverSpheroRvr()

led_controller = LedControlObserver(rvr)


def main():
     """ This program demonstrates how to set the all the LEDs of RVR using the helper function
    defined in LedControlObserver.

    """

    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Turn off all lights
    led_controller.turn_leds_off()
    time.sleep(0.5)

    # Set all lights to yellow using Colors enumeration
    led_controller.set_all_leds_color(Colors.yellow)
    time.sleep(1)

    # Turn off all lights
    led_controller.turn_leds_off()
    time.sleep(0.5)

    # Set all lights to yellow using RGB values
    led_controller.set_all_leds_rgb(255, 144, 0)
    time.sleep(1)

    rvr.close()


main()
