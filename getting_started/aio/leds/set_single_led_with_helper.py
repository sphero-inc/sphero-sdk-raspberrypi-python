import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import Colors
from sphero_sdk import LedControlAsync
from sphero_sdk import RvrLedGroups
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object and pass in a SerialAsyncDal object, which in turn takes a reference to the program loop
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)

# Create object that let's us control the LEDs of RVR
led_controller = LedControlAsync(rvr)


async def main():
    """ This program demonstrates how to set a single LED on RVR using the controller LedControlAsync.

    """
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Turn off all lights
    await led_controller.turn_leds_off()
    await asyncio.sleep(0.5)

    # Set right headlight to red
    await led_controller.set_led_rgb(RvrLedGroups.headlight_right, 255, 0, 0)
    await asyncio.sleep(1)

    # Set left headlight to green
    await led_controller.set_led_color(RvrLedGroups.headlight_left, Colors.green)
    await asyncio.sleep(1)


# Run program loop until the main function has completed
loop.run_until_complete(
    main()
)

loop.stop()
loop.close()
