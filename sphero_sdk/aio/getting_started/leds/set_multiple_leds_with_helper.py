import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

from sphero_sdk import LedControlAsync
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups


# Get a reference to the asynchornous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object, and pass in a SerialAsyncDal object, which in turn takes a reference
# to the asynchronous program loop
rvr = AsyncSpheroRvr(
    dal = SerialAsyncDal(
        loop
    )
)

# Create object that let's us control the LEDs of RVR
leds_helper = LedControlAsync(rvr)


async def main():
    """ This program demonstrates how to set multiple LEDs on RVR using the helper function
        defined in LedControlAsync.

    """
    await rvr.wake()

    await leds_helper.turn_leds_off()
    await asyncio.sleep(0.25)

    # Set multiple LEDs with colors enum
    await leds_helper.set_multiple_leds_color([RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], [Colors.green, Colors.blue])
    await asyncio.sleep(1)

    # Set multiple LEDs to color with RGB values
    rgb_values = [255, 0, 0, 0, 255, 0] # red and green
    await leds_helper.set_multiple_leds_colors([RvrLedGroups.headlight_left, RvrLedGroups.headlight_right], rgb_values)
    await asyncio.sleep(1)


# Run event loop until the main function has completed
loop.run_until_complete(
        main()
    )

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
