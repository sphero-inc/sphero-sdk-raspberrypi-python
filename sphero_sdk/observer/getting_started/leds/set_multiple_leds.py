import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups

rvr = ObserverSpheroRvr()

def main():
    """ This program demonstrates how to set multiple LEDs on RVR with one function call
            to set_all_leds_with_32_bit_mask.

    """
    rvr.wake()

    # Turn off all lights
    rvr.set_all_leds_with_32_bit_mask(
        RvrLedGroups.all_lights.value, [color for _ in range(10) for color in Colors.off.value]
    )

    time.sleep(1)

    # Set front and rear power buttons to blue
    led_group_bitmask = RvrLedGroups.power_button_front.value | RvrLedGroups.power_button_rear.value # 0x1c0000
    rvr.set_all_leds_with_32_bit_mask(
        led_group_bitmask, [0, 0, 255, 255, 0,0]
    )


main()
