import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

from sphero_sdk import LedControlAsync
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import Colors

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
    """ This program demonstrates how to set the all the LEDs of RVR using the helper function
    defined in LedControlAsync.

    """
    await rvr.wake()

    await leds_helper.turn_leds_off()
    await asyncio.sleep(0.25)

    # Set all LEDs to color of specified color
    await leds_helper.set_all_leds_color(Colors.yellow)
    await asyncio.sleep(1)

    # Set all LEDs to color of RGB value (255, 0, 255)
    await leds_helper.set_all_leds_rgb(255, 0, 255)
    await asyncio.sleep(1)

# Run event loop until the main function has completed
loop.run_until_complete(
        main()
    )

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
