import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import Colors
from sphero_sdk import LedControlAsync
from sphero_sdk import RvrLedGroups
from sphero_sdk import RestfulAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",  # RVR's prefix is RV
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)

# Create object that let's us control the LEDs of RVR
led_controller = LedControlAsync(rvr)


async def main():
    """ This program demonstrates how to set multiple LEDs on RVR using the controller LedControlAsync.

    """
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Turn off all lights
    await led_controller.turn_leds_off()
    await asyncio.sleep(0.5)

    # Set headlights to colors green and blue respectively using Colors enumeration
    await led_controller.set_multiple_leds_color(
        [RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], [Colors.green, Colors.blue])
    await asyncio.sleep(1)

    # Set headlights to colors green and blue respectively using RGB list
    await led_controller.set_multiple_leds_colors(
        [RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], [255, 0, 0, 0, 255, 0])
    await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        loop.run_until_complete(
            rvr.close()
        )

        if loop.is_running():
            loop.close()
