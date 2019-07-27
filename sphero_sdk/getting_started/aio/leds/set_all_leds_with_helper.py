import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

from sphero_sdk import LedControlAsync
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import Colors


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
    """ This program demonstrates how to set the all the LEDs of RVR using the helper function
    defined in LedControlAsync.

    """
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Turn off all lights
    await led_controller.turn_leds_off()
    await asyncio.sleep(0.5)

    # Set all lights to yellow using Colors enumeration
    await led_controller.set_all_leds_color(Colors.yellow)
    await asyncio.sleep(1)

    # Turn off all lights
    await led_controller.turn_leds_off()
    await asyncio.sleep(0.5)

    # Set all lights to yellow using RGB values
    await led_controller.set_all_leds_rgb(255, 144, 0)
    await asyncio.sleep(1)

# Run program loop until the main function has completed
loop.run_until_complete(
        main()
    )

loop.stop()
loop.close()
