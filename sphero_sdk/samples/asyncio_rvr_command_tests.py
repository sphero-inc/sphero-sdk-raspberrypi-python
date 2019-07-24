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

test_target = 1


async def main():
    global rvr
    global test_target

    print("target 1 wake")
    await rvr.wake()
    await asyncio.sleep(1)

    test_target = 1
    print("echo target {}".format(test_target))
    data = await rvr.echo(data=1, target=test_target)
    print("target {} echo data {}".format(test_target, data))
    await asyncio.sleep(1)

    test_target = 2
    print("echo target {}".format(test_target))
    data = await rvr.echo(data=11, target=test_target)
    print("target {} echo data {}".format(test_target, data))
    await asyncio.sleep(1)

    # ISSUE - length of dids is 1
    test_target = 1
    print("get supported dids for target {}".format(test_target))
    dids = await rvr.get_supported_dids(test_target)
    print(len(dids))
    await asyncio.sleep(1)

    # ISSUE - length of dids is 1
    test_target = 2
    print("get supported dids for target {}".format(test_target))
    dids = await rvr.get_supported_dids(test_target)
    print(len(dids))
    await asyncio.sleep(1)

    test_target = 1
    print("get main application version target {}".format(test_target))
    major, minor, revision = await rvr.get_main_application_version(target=test_target)
    print("{}.{}.{}".format(major, minor, revision))
    await asyncio.sleep(1)

    test_target = 2
    print("get main application version target {}".format(test_target))
    major, minor, revision = await rvr.get_main_application_version(target=test_target)
    print("{}.{}.{}".format(major, minor, revision))
    await asyncio.sleep(1)

    test_target = 1
    print("target {} get bootloader version".format(test_target))
    major, minor, revision = await rvr.get_bootloader_version(target=test_target)
    print("{}.{}.{}".format(major, minor, revision))
    await asyncio.sleep(1)

    test_target = 2
    print("target {} get bootloader version".format(test_target))
    major, minor, revision = await rvr.get_bootloader_version(target=test_target)
    print("{}.{}.{}".format(major, minor, revision))
    await asyncio.sleep(1)

    test_target = 1
    print("target {} get board revision".format(test_target))
    revision = await rvr.get_board_revision(target=test_target)
    print("{}".format(revision))
    await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/aio/server/handler/api_sphero_handler.py", line 172, in response_handler_wrapper
    raise Exception(msg.err.name)
    Exception: BAD_CID
    '''
    # test_target = 2
    # print("target {} get board revision".format(test_target))
    # revision = await rvr.get_board_revision(target=test_target)
    # print("{}".format(revision))
    # await asyncio.sleep(1)

    # ERROR
    '''
    appending bytes: bytearray(b'\x8d!\x01\x11\x06\xff\x00dec954aed0f6\x03\xd8')
    parsing packet complete: RESPONSE 255: DID: 17 CID: 6 Payload: 646563393534616564306636 ERR: 0
    File "/home/pi/raspberry-pi/spheroboros/aio/server/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # print("target {} get mac address".format(test_target))
    # macAddress = await rvr.get_mac_address()
    # print("{}".format(macAddress))
    # await asyncio.sleep(5)

    print("target {} get nordic temperature".format(test_target))
    temperature = await rvr.get_nordic_temperature()
    print("{}".format(temperature))
    await asyncio.sleep(1)

    test_target = 1
    print("target {} get stats id".format(test_target))
    statsId = await rvr.get_stats_id(target=test_target)
    print("{}".format(statsId))
    await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/aio/server/handler/api_sphero_handler.py", line 172, in response_handler_wrapper
    raise Exception(msg.err.name)
    Exception: BAD_CID
    '''
    # test_target = 2
    # print("target {} get stats id".format(test_target))
    # statsId = await rvr.get_stats_id(target=test_target)
    # print("{}".format(statsId))
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/spheroboros/aio/server/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # test_target = 1
    # print("target {} get processor name".format(test_target))
    # name = await rvr.get_processor_name(target=test_target)
    # print("{}".format(name))
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/spheroboros/aio/server/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # test_target = 2
    # print("target {} get processor name".format(test_target))
    # await rvr.get_processor_name(target=test_target, handler=handle_processor_name)
    # await asyncio.sleep(1)

    print("target 1 get boot reason")
    reason = await rvr.get_boot_reason()
    print("{}".format(reason))
    await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/aio/server/handler/api_sphero_handler.py", line 172, in response_handler_wrapper 
    raise Exception(msg.err.name)
    Exception: FAILED
    '''
    # print("target 1 get last error info")
    # fileName, lineNumber, data = await rvr.get_last_error_info()
    # print("fileName = {}, lineNumber = {}, data = {}".format(fileName, lineNumber, data))
    # await asyncio.sleep(1)

    '''test_target = 1
    print("target {} get manufacturing date".format(test_target))
    year, month, day = await rvr.get_manufacturing_date(target=test_target)
    print("{}/{}/{}".format(year, month, day))
    await asyncio.sleep(1)'''

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/aio/server/handler/api_sphero_handler.py", line 172, in response_handler_wrapper
    raise Exception(msg.err.name)
    Exception: BAD_CID
    '''
    # test_target = 2
    # print("target {} get manufacturing date".format(test_target))
    # year, month, day = await rvr.get_manufacturing_date(target=test_target)
    # print("{}/{}/{}".format(year, month, day))
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/common/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # test_target = 1
    # print("target {} get sku".format(test_target))
    # sku = await rvr.get_sku(target=test_target)
    # print("{}".format(sku))
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/sphero_sdk/common/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # test_target = 2
    # print("target {} get sku".format(test_target))
    # await rvr.get_sku(target=test_target)
    # await asyncio.sleep(1)

    print("target 1 get battery percentage")
    percentage = await rvr.get_battery_percentage()
    print("{}".format(percentage))
    await asyncio.sleep(1)

    print("target 1 get battery voltage state")
    state = await rvr.get_battery_voltage_state()
    print("{}".format(state))
    await asyncio.sleep(1)

    # test_target = 1
    # print("target {} set bluetooth device name to \"cat\"".format(test_target))
    # await rvr.set_bluetooth_device_name(name='cat', target=test_target)
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/spheroboros/aio/server/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # print("target {} get bluetooth device name".format(test_target))
    # name = await rvr.get_bluetooth_device_name(target=test_target)
    # print("{}".format(name))
    # await asyncio.sleep(1)

    # test_target = 2
    # print("target {} set bluetooth device name \"dog\"".format(test_target))
    # await rvr.set_bluetooth_device_name(name='dog', target=test_target)
    # await asyncio.sleep(1)

    # ERROR
    '''
    File "/home/pi/raspberry-pi/spheroboros/aio/server/protocol/api_sphero_message.py", line 282, in unpack
    unpacker = Unpack.string
    AttributeError: type object 'Unpack' has no attribute 'string'
    '''
    # print("target {} get bluetooth device name".format(test_target))
    # await rvr.get_bluetooth_device_name(handler=handle_bluetooth_device_name, target=test_target)
    # await asyncio.sleep(1)

    print("target 2 raw motors")
    await rvr.raw_motors(1, 128, 1, 128)
    await asyncio.sleep(2)
    await rvr.raw_motors(0, 0, 0, 0)
    await asyncio.sleep(1)

    print("target 2 reset yaw")
    await rvr.reset_yaw()

    print("target 2 drive with heading...")
    await rvr.drive_with_heading(128, 0, 0)
    await asyncio.sleep(2)

    print("target 1 set all leds red with 32-bit mask")
    rgb_values = [255, 0, 0]
    led_values = [color for i in range(10) for color in rgb_values]
    await rvr.set_all_leds_with_32_bit_mask(led_group=0x3FFFFFFF, led_brightness_values=led_values)
    await asyncio.sleep(2)

    print("target 1 set all leds green with 32-bit mask")
    rgb_values = [0, 255, 0]
    led_values = [color for i in range(10) for color in rgb_values]
    await rvr.set_all_leds_with_32_bit_mask(led_group=0x3FFFFFFF, led_brightness_values=led_values)
    await asyncio.sleep(2)

    print("target 1 set all leds blue with 32-bit mask")
    rgb_values = [0, 0, 255]
    led_values = [color for i in range(10) for color in rgb_values]
    await rvr.set_all_leds_with_32_bit_mask(led_group=0x3FFFFFFF, led_brightness_values=led_values)
    await asyncio.sleep(2)

    print("target 2 get usb connection status")
    usbConnectionStatus = await rvr.get_usb_connection_status()
    print("{}".format(usbConnectionStatus))
    await asyncio.sleep(1)

    print("target 1 enter soft sleep")
    await rvr.enter_soft_sleep()
    await asyncio.sleep(1)

    print("All Done")

loop.run_until_complete(
    main()
)
