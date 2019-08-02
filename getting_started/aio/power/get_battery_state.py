import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates how to retrieve the battery state of RVR and print it to the console.

    """
    await rvr.wake()

    battery_percentage = await rvr.get_battery_percentage()

    battery_voltage_state = await rvr.get_battery_voltage_state()

    print("Current battery percentage: ", battery_percentage[0], "%")

    state_info = {0: "unknown", 1: "OK", 2: "low", 3: "critical"}
    print("Voltage states: ", state_info)
    print("Current voltage state: ", battery_voltage_state[0])


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
