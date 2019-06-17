from spheroboros.common.commands.io import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def set_all_leds_with_32_bit_mask(led_group, led_brightness_values):
    did = DevicesEnum.io
    cid = CommandsEnum.set_all_leds_with_32_bit_mask
    inputs = [
        Parameter(
            name='ledGroup',
            data_type='uint32_t',
            index=0,
            value=led_group,
            size=1
        ),
        Parameter(
            name='ledBrightnessValues',
            data_type='uint8_t',
            index=1,
            value=led_brightness_values,
            size=32
        ),
    ]
    return did, cid, inputs


def enable_usb_connection_notification(enable):
    did = DevicesEnum.io
    cid = CommandsEnum.enable_usb_connection_notification
    inputs = [
        Parameter(
            name='enable',
            data_type='bool',
            index=0,
            value=enable,
            size=1
        ),
    ]
    return did, cid, inputs


def on_usb_connection_status_notify():
    did = DevicesEnum.io
    cid = CommandsEnum.usb_connection_status_notify,
    outputs=[
        Parameter(
            name='usbConnectionStatus',
            data_type='uint8_t',
            index=0,
            size=1
        ),
    ]
    return did, cid, outputs


def get_usb_connection_status():
    did = DevicesEnum.io
    cid = CommandsEnum.get_usb_connection_status
    outputs=[
        Parameter(
            name='usbConnectionStatus',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs
