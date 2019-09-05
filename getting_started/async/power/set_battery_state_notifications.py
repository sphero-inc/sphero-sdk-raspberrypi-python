import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
import time

from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def on_battery_voltage_state_change(response):
    print('response contents:', response)
    state = response['state']
    print("Battery voltage state changed; new state: ", state)


async def main():
    """ This program demonstrates how to enable battery state change notifications and how to set up
        a handler for such notifications.

    """
    await rvr.wake()

    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    await rvr.on_battery_voltage_state_change_notify(on_battery_voltage_state_change)

    # Uncomment this infinite loop if you'd like to operate RVR by other means and monitor battery notifications.
    while True:
       print('waiting for battery notification....')
       await asyncio.sleep(5)


try:
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )
except KeyboardInterrupt:
    print("Program aborted with keyboard interrupt.")
    loop.stop()

time.sleep(1)
loop.close()
