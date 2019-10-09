import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups


rvr = SpheroRvrObserver()


def main():
    """ This program demonstrates how to set multiple LEDs on RVR using the LED control helper.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.led_control.turn_leds_off()

        # Delay to show LEDs change
        time.sleep(1)

        rvr.led_control.set_multiple_leds_with_enums(
            leds=[
                RvrLedGroups.headlight_left,
                RvrLedGroups.headlight_right
            ],
            colors=[
                Colors.green,
                Colors.blue
            ]
        )

        # Delay to show LEDs change
        time.sleep(1)

        rvr.led_control.set_multiple_leds_with_rgb(
            leds=[
                RvrLedGroups.headlight_left,
                RvrLedGroups.headlight_right
            ],
            colors=[
                255, 0, 0,
                0, 255, 0
            ]
        )

        # Delay to show LEDs change
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
