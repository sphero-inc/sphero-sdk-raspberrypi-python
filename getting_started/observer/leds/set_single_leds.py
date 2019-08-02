import time

from sphero_sdk import Colors
from sphero_sdk import ObserverSpheroRvr
from sphero_sdk import RvrLedGroups

rvr = ObserverSpheroRvr()


def main():
    """ This program demonstrates how to set a single LED on RVR with one function call to set_all_leds_with_32_bit_mask.

    """
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Turn off all lights
    rvr.set_all_leds_with_32_bit_mask(
        RvrLedGroups.all_lights.value, [color for _ in range(10) for color in Colors.off.value]
    )

    time.sleep(1)

    # Set right headlight to red
    led_group_bitmask = RvrLedGroups.headlight_right.value  # 0xe00

    rvr.set_all_leds_with_32_bit_mask(
        led_group_bitmask, [255, 0, 0]
    )

    time.sleep(1)

    # Set left headlight to green
    led_group_bitmask = RvrLedGroups.headlight_left.value  # 0x1c0

    rvr.set_all_leds_with_32_bit_mask(
        led_group_bitmask, [0, 255, 0]
    )

    time.sleep(1)

    rvr.close()


main()
