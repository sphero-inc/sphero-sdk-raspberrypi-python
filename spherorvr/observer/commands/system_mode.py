from spheroboros.common.commands.system_mode import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def enable_play_mode_change_notify():
    did = DevicesEnum.system_mode
    cid = CommandsEnum.enable_play_mode_change_notify
    outputs=[
        Parameter(
            name='identifier',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]


def set_play_mode(identifier):
    did = DevicesEnum.system_mode
    cid = CommandsEnum.set_play_mode
    inputs=[
        Parameter(
            name='identifier',
            data_type='uint16_t',
            index=0,
            value=identifier,
            size=1
        ),
    ]


def get_play_mode():
    did = DevicesEnum.system_mode
    cid = CommandsEnum.get_play_mode
    outputs=[
        Parameter(
            name='identifier',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
    ]
