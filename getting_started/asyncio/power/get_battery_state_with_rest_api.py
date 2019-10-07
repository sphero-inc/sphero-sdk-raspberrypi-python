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


async def main():
    """
    This program demonstrates how to retrieve the battery state of RVR and print it to the console.
    Echo can be used to check to see if RVR is connected and awake.  In order to test it, a node.js
    server must be running on the raspberry-pi connected to RVR.  This code is meant to be executed
    from a separate computer.

    """
    await rvr.wake()

    response = await rvr.get_battery_percentage()
    print('Response data for battery percentage:', response)

    response = await rvr.get_battery_voltage_state()
    print('Response data for voltage state:', response)

    state_info = {0: "unknown", 1: "OK", 2: "low", 3: "critical"}
    print("Voltage states: ", state_info)


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
