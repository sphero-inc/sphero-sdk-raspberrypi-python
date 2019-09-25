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
    """This program demonstrates how to update sensor streaming parameters at runtime.

    """
    # Wake up RVR
    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)
    print("----------", "Enabling IMU at 100 ms", "----------")

    # Add a callback to receive sensor stream data
    await rvr.sensor_control.add_sensor_data_handler(on_sensor_streaming_data)

    # Set a slow streaming interval (every 500 ms)
    rvr.sensor_control.streaming_interval = 100

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
    await rvr.sensor_control.enable("IMU")

    # Pause this function for 5 seconds
    await asyncio.sleep(5)
    print("----------", "Updating interval to 1000 ms", "----------")

    # Update the streaming interval to 100ms
    rvr.sensor_control.streaming_interval = 1000

    # Sleep for 5 seconds before calling next function
    await asyncio.sleep(5)
    print("----------", "Adding color detection and velocity sensor streams", "----------")

    # Add 2 more services
    await rvr.sensor_control.enable("AmbientLight", "Velocity")

    # Sleep for another 5 seconds
    await asyncio.sleep(5)
    print("----------", "Disabling IMU sensor stream and updating interval to 100", "----------")

    # Disable IMU service
    await rvr.sensor_control.disable("IMU")

    # Sleep for another 5 seconds
    await asyncio.sleep(5)
    print("----------", "Disabling all services", "----------")

    # Disable all services
    await rvr.sensor_control.disable_all()

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
