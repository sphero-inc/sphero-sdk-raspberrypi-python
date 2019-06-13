from spheroboros.common.commands.system_info import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def get_main_application_version():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_main_application_version
    outputs = [
        Parameter(
            name='major',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='minor',
            data_type='uint16_t',
            index=1,
            size=1,
        ),
        Parameter(
            name='revision',
            data_type='uint16_t',
            index=2,
            size=1,
        ),
    ]
    return did, cid, outputs

