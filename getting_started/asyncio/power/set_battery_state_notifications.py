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


async def battery_voltage_state_change_handler(battery_voltage_state):
    print('Battery voltage state: ', battery_voltage_state)


async def main():
    """ This program demonstrates how to enable battery state change notifications.
    """

    await rvr.wake()

    # give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.on_battery_voltage_state_change_notify(handler=battery_voltage_state_change_handler)
    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    # remove infinite loop if you'd like to operate RVR by other means and monitor battery notifications
    while True:
        print('Waiting for battery notification...')
        await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.stop()

        loop.close()
