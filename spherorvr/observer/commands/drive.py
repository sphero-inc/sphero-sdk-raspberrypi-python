from spheroboros.common.commands.drive import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def raw_motors(left_mode, left_speed, right_mode, right_speed):
    did = DevicesEnum.drive
    cid = CommandsEnum.raw_motors
    inputs=[
        Parameter(
            name='leftMode',
            data_type='uint8_t',
            index=0,
            value=left_mode,
            size=1
        ),
        Parameter(
            name='leftSpeed',
            data_type='uint8_t',
            index=1,
            value=left_speed,
            size=1
        ),
        Parameter(
            name='rightMode',
            data_type='uint8_t',
            index=2,
            value=right_mode,
            size=1
        ),
        Parameter(
            name='rightSpeed',
            data_type='uint8_t',
            index=3,
            value=right_speed,
            size=1
        ),
    ]
    return did, cid, inputs


def reset_yaw():
    did = DevicesEnum.drive,
    cid = CommandsEnum.reset_yaw
    return did, cid


def drive_with_heading(speed, heading, flags):
    did = DevicesEnum.drive
    cid = CommandsEnum.drive_with_heading
    inputs=[
        Parameter(
            name='speed',
            data_type='uint8_t',
            index=0,
            value=speed,
            size=1
        ),
        Parameter(
            name='heading',
            data_type='int16_t',
            index=1,
            value=heading,
            size=1
        ),
        Parameter(
            name='flags',
            data_type='uint8_t',
            index=2,
            value=flags,
            size=1
        ),
    ]
    return did, cid, inputs
