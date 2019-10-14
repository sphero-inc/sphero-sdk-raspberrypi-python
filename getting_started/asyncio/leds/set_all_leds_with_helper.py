import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import Colors
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates how to set the all the LEDs of RVR using the LED control helper.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.led_control.turn_leds_off()

    # Delay to show LEDs change
    await asyncio.sleep(1)

    await rvr.led_control.set_all_leds_color(color=Colors.yellow)

    # Delay to show LEDs change
    await asyncio.sleep(1)

    await rvr.led_control.turn_leds_off()

    # Delay to show LEDs change
    await asyncio.sleep(1)

    await rvr.led_control.set_all_leds_rgb(red=255, green=144, blue=0)

    # Delay to show LEDs change
    await asyncio.sleep(1)

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
