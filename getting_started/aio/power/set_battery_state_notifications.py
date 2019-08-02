import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


def on_battery_voltage_state_change(state):
    print("Battery voltage state changed; new state: ", state)


async def main():
    """ This program demonstrates how to enable battery state change notifications and how to set up
        a handler for such notifications.

    """
    await rvr.wake()

    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    await rvr.on_battery_voltage_state_change_notify(on_battery_voltage_state_change)


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
