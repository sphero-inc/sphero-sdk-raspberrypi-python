import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

async def on_sensor_streaming_data(response):
    print(response)

async def get_single_sensor_stream():
    """This program enables a single sensor stream that will be printed to the console.

    """
    # Wake up RVR
    await rvr.wake()
    
    # Add a callback to receive sensor stream data
    await rvr.sensor_control.add_sensor_data_handler(on_sensor_streaming_data)
    
    # Enable a single sensor. Supported sensors are:
    # "ColorDetection"
    # "AmbientLight"
    # "Quaternion"
    # "IMU"
    # "Accelerometer"
    # "Gyroscope"
    # "Locator"
    # "Velocity"
    # "Speed"
    # "CoreTime"
    await rvr.sensor_control.enable("Accelerometer")

    # Allow this program to run until a keyboard interrupt is detected
    while True:
        await asyncio.sleep(1)

async def close_rvr():
    await rvr.close()

try:
    loop.run_until_complete(
        get_single_sensor_stream()
    )
except KeyboardInterrupt:
    print("Program terminated with keyboard interrupt.")

    # Need to make sure we close rvr properly to terminate all streams.
    loop.run_until_complete(
       rvr.close()
    )
finally:
    # stop the loop
    loop.close()
