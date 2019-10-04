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


async def main():
    """ This program demonstrates how to retrieve the battery state of RVR.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    battery_percentage = await rvr.get_battery_percentage()
    print('Battery percentage: ', battery_percentage)

    battery_voltage_state = await rvr.get_battery_voltage_state()
    print('Voltage state: ', battery_voltage_state)

    state_info = {
        0: 'Unknown',
        1: 'OK',
        2: 'Low',
        3: 'Critical'
    }   # TODO: are these autogen'd and can they be referenced instead?
    print('Voltage states: ', state_info)

    await rvr.close()


if __name__ == '__main__':
    loop.run_until_complete(
        main()
    )

    if loop.is_running():
        loop.stop()

    loop.close()
