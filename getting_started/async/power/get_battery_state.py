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


async def main():
    """ This program demonstrates how to retrieve the battery state of RVR and print it to the console.

    """
    await rvr.wake()

    response = await rvr.get_battery_percentage()
    print('response contents:', response)
    percentage = response['percentage']

    response = await rvr.get_battery_voltage_state()
    print('response contents:', response)
    state = response['state']

    print("Current battery percentage: {}%".format(percentage))

    state_info = {0: "unknown", 1: "OK", 2: "low", 3: "critical"}
    print("Voltage states: ", state_info)
    print("Current voltage state: {}".format(state))


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
