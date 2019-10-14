import os
import sys
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


async def battery_voltage_state_change_handler(battery_voltage_state):
    print('Battery voltage state: ', battery_voltage_state)


async def main():
    """ This program demonstrates how to enable battery state change notifications.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.on_battery_voltage_state_change_notify(handler=battery_voltage_state_change_handler)
    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    print('Waiting for battery notification...')

    # The asyncio loop will run forever to give the aforementioned events time to occur


if __name__ == '__main__':
    try:
        asyncio.ensure_future(
            main()
        )
        loop.run_forever()

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
