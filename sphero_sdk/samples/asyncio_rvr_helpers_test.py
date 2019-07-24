import asyncio
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RvrLedGroups
from sphero_sdk import RgbColors
from sphero_sdk import IrCodes
from sphero_sdk import AsyncLedsHelper
from sphero_sdk import AsyncIrHelper
from sphero_sdk import AsyncDriveHelper
from sphero_sdk import RawMotorModes

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def test_leds():
    leds_helper = AsyncLedsHelper(rvr)

    print('rvr wake')
    await rvr.wake()

    major,minor,revision = await rvr.get_main_application_version(target=1)
    print('target 1','{}.{}.{}'.format(major,minor,revision))

    major, minor, revision = await rvr.get_main_application_version(target=2)
    print('target 2', '{}.{}.{}'.format(major, minor, revision))

    print ("Setting all lights red")
    await leds_helper.set_all_lights_enum(RgbColors.red)
    await asyncio.sleep(2)
    print("Setting all lights green")
    await leds_helper.set_all_lights_enum(RgbColors.green)
    await asyncio.sleep(2)
    print("Setting all lights blue")
    await leds_helper.set_all_lights_enum(RgbColors.blue)
    await asyncio.sleep(2)
    print("Setting all lights white")
    await leds_helper.set_all_lights_enum(RgbColors.white)
    await asyncio.sleep(2)
    print("Setting all lights yellow")
    await leds_helper.set_all_lights_enum(RgbColors.yellow)
    await asyncio.sleep(2)
    print("Setting all lights purple")
    await leds_helper.set_all_lights_enum(RgbColors.purple)
    await asyncio.sleep(2)
    print("Setting all lights orange")
    await leds_helper.set_all_lights_enum(RgbColors.orange)
    await asyncio.sleep(2)
    print("Setting all lights pink")
    await leds_helper.set_all_lights_enum(RgbColors.pink)
    await asyncio.sleep(2)
    print("Setting all lights black")
    await leds_helper.set_all_lights_enum(RgbColors.black)
    await asyncio.sleep(2)

    print("Setting all lights 128, 255, 64")
    await leds_helper.set_all_lights_rgb(128, 255, 64)
    await asyncio.sleep(2)
    print("Setting all lights 64, 128, 255")
    await leds_helper.set_all_lights_rgb(64, 128, 255)
    await asyncio.sleep(2)
    print("Setting all lights 255, 64, 128")
    await leds_helper.set_all_lights_rgb(255, 64, 128)
    await asyncio.sleep(2)

    print("Setting multiple lights rear_1 purple, door_1 yellow")
    await leds_helper.set_multiple_lights_enum([RvrLedGroups.rear_1, RvrLedGroups.door_1], [RgbColors.purple, RgbColors.yellow])
    await asyncio.sleep(2)
    print("Setting multiple lights rear_2 (0, 255, 0), door_2 (0, 255, 0)")
    await leds_helper.set_multiple_lights_rgb([RvrLedGroups.rear_2, RvrLedGroups.door_2], [0, 255, 0, 0, 255, 0])
    await asyncio.sleep(2)



async def handle_ir_message(infraredCode):
    print('received ir code', infraredCode)


async def test_ir():
    ir_helper = AsyncIrHelper(rvr)

    print('listening for messages on channel 0 and 3')
    await ir_helper.listen_for_infrared_message(channels=[IrCodes.zero,IrCodes.three], handler=handle_ir_message)

    print('sending ir message 1')
    await ir_helper.send_infrared_message(messages=[IrCodes.one], strength=64)
    asyncio.sleep(2)

    print('sending ir message 2')
    await ir_helper.send_infrared_message(messages=[IrCodes.two], strength=64)
    asyncio.sleep(2)


async def test_drive():
    drive_helper = AsyncDriveHelper(rvr)

    await drive_helper.drive_forward_seconds(speed=128, heading=0, time_to_drive=2)
    await drive_helper.drive_backward_seconds(speed=128, heading=0, time_to_drive=2)

    await drive_helper.drive_raw_motors(RawMotorModes.forward, 128, RawMotorModes.reverse, 128)
    await asyncio.sleep(2)
    await drive_helper.stop_raw_motors()


async def main():
    await test_leds()
    await test_ir()
    await test_drive()

loop.run_until_complete(main())
loop.close()