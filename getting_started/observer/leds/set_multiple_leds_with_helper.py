import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import LedControlObserver
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups

rvr = SpheroRvrObserver()

led_controller = LedControlObserver(rvr)


def main():
    """ This program demonstrates how to set multiple LEDs on RVR using the controller LedControlObserver.

    """

    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Turn off all lights
    led_controller.turn_leds_off()
    time.sleep(0.5)

    # Set headlights to colors green and blue respectively using Colors enumeration
    led_controller.set_multiple_leds_color(
        [RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], [Colors.green, Colors.blue])
    time.sleep(1)

    # Set headlights to colors green and blue respectively using RGB list
    led_controller.set_multiple_leds_colors(
        [RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], [255, 0, 0, 0, 255, 0])
    time.sleep(1)

    rvr.close()


main()
