import asyncio
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def sensor_data_handler(sensor_data):
    print('Sensor data response: ', sensor_data)


async def main():
    """ This program demonstrates how to use the color sensor on RVR (located on the down side of RVR, facing the floor)
        to report colors detected. To exit program, press <CTRL-C>
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.enable_color_detection(is_enabled=True)
    await rvr.sensor_control.add_sensor_data_handler(handler=sensor_data_handler)
    await rvr.sensor_control.enable('ColorDetection')       # TODO: is there a constant available for this?


if __name__ == '__main__':
    try:
        asyncio.ensure_future(
            main()
        )

        loop.run_forever()

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.stop()

        loop.close()
