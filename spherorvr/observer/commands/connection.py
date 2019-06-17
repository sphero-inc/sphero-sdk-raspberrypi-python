from spheroboros.common.commands.connection import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def set_bluetooth_device_name(name):
    did = DevicesEnum.connection
    cid = CommandsEnum.set_bluetooth_device_name
    inputs=[
        Parameter(
            name='name',
            data_type='std::string',
            index=0,
            value=name,
            size=1
        ),
    ]
    return did, cid, inputs


def get_bluetooth_device_name():
    did = DevicesEnum.connection
    cid = CommandsEnum.get_bluetooth_device_name
    outputs=[
        Parameter(
            name='name',
            data_type='std::string',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs
