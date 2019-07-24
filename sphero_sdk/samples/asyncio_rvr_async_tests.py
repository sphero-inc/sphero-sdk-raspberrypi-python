import sys
sys.path.append('/home/pi/raspberry-pi')

import asyncio
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def handle_will_sleep():
    print("RVR will sleep")


async def handle_did_sleep():
    print("RVR did sleep")
    loop.stop()


async def handle_battery_voltage_state(state):
    print("battery voltage state: {}".format(state))


async def handle_usb_connection_status(usbConnectionStatus):
    print("handle usb connection status: {}".format(usbConnectionStatus))


async def main():
    print("target 1 wake")
    await rvr.wake()

    print("target 2 getting main app version")
    major, minor, revision = await rvr.get_main_application_version(target=2)
    print("{}.{}.{}".format(major, minor, revision))

    # SLEEP NOTIFY (known not to work for ST versions 2.2.402  and 4.1.411
    '''print("target 1 on will sleep notify")
    await rvr.on_will_sleep_notify(handler=handle_will_sleep)

    print("target 1 on did sleep notify")
    await rvr.on_did_sleep_notify(handler=handle_did_sleep)'''

    # BATTERY VOLTAGE NOTIFY

    print("target 1 on battery voltage state change notify")
    await rvr.on_battery_voltage_state_change_notify(handler=handle_battery_voltage_state)

    print("target 1 enable battery voltage state change notify ")
    await rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    # USB STATUS NOTIFY (not working)
    print("target 2 on usb connection notify")
    await rvr.on_usb_connection_status_notify(handler=handle_usb_connection_status)

    print("target 2 enable usb conneciton notification")
    await rvr.enable_usb_connection_notification(enable=True)

asyncio.ensure_future(main())
loop.run_forever()
loop.close()
