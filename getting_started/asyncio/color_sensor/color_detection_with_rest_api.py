import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RestfulAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=RestfulAsyncDal(
        prefix="RV",  # RVR's prefix is RV
        domain="10.211.2.21",  # Add your raspberry-pi's IP address here
        port=2010  # The port opened by the npm server is always 2010
    )
)



async def on_color_detected(response):
    print('Response data for color detected:',response)


async def main():
    """ This program uses the color sensor on RVR (located on the down side of RVR, facing the floor) to report colors detected.
        To exit program, press <CTRL-C>

    """
    # Wake up RVR
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(1)

    # This enables the color sensor on RVR
    await rvr.enable_color_detection(is_enabled=True)

    # Register a handler to be called when a color detection notification is received
    await rvr.sensor_control.add_sensor_data_handler(on_color_detected)

    # Enable the color detection sensor stream
    await rvr.sensor_control.enable("ColorDetection")


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
