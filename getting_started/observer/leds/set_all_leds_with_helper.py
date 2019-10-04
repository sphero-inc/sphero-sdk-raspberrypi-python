import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors


rvr = SpheroRvrObserver()


def main():
    """ This program demonstrates how to set the all the LEDs of RVR using the LED control helper.
    """

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.led_control.turn_leds_off()

    # delay to show LEDs change
    time.sleep(1)

    rvr.led_control.set_all_leds_color(color=Colors.yellow)

    # delay to show LEDs change
    time.sleep(1)

    rvr.led_control.turn_leds_off()

    # delay to show LEDs change
    time.sleep(1)

    rvr.led_control.set_all_leds_rgb(red=255, green=144, blue=0)

    # delay to show LEDs change
    time.sleep(1)

    rvr.close()


if __name__ == '__main__':
    main()
