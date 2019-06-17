from spheroboros.common.commands.api_and_shell import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def echo(data):
    did = DevicesEnum.api_and_shell
    cid = CommandsEnum.echo
    inputs=[
        Parameter(
            name='data',
            data_type='uint8_t',
            index=0,
            value=data,
            size=16
        ),
    ],
    outputs=[
        Parameter(
            name='data',
            data_type='uint8_t',
            index=0,
            size=16,
        ),
    ]
    return did, cid, inputs, outputs


def get_api_protocol_version():
    did = DevicesEnum.api_and_shell
    cid = CommandsEnum.get_api_protocol_version
    outputs=[
        Parameter(
            name='majorVersion',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='minorVersion',
            data_type='uint8_t',
            index=1,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_supported_dids():
    did = DevicesEnum.api_and_shell
    cid = CommandsEnum.get_supported_dids
    outputs=[
        Parameter(
            name='dids',
            data_type='uint8_t',
            index=0,
            size=9999,
        ),
    ]
    return did, cid, outputs


def get_supported_cids(input_did):
    did = DevicesEnum.api_and_shell
    cid = CommandsEnum.get_supported_cids
    inputs=[
        Parameter(
            name='did',
            data_type='uint8_t',
            index=0,
            value=input_did,
            size=1
        ),
    ],
    outputs=[
        Parameter(
            name='cids',
            data_type='uint8_t',
            index=0,
            size=9999,
        ),
    ]
    return did, cid, inputs, outputs
