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


def get_bootloader_version():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_bootloader_version
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


def get_board_revision():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_board_revision
    outputs = [
        Parameter(
            name='revision',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_mac_address():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_mac_address
    outputs = [
        Parameter(
            name='macAddress',
            data_type='std::string',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_nordic_temperature():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_nordic_temperature
    outputs = [
        Parameter(
            name='temperature',
            data_type='int32_t',
            index=0,
            size=2,
        ),
    ]
    return did, cid, outputs


def get_stats_id():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_stats_id
    outputs = [
        Parameter(
            name='statsId',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_processor_name():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_processor_name
    outputs = [
        Parameter(
            name='name',
            data_type='std::string',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_boot_reason():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_boot_reason
    outputs = [
        Parameter(
            name='reason',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_last_error_info():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_last_error_info
    outputs = [
        Parameter(
            name='fileName',
            data_type='uint8_t',
            index=0,
            size=32,
        ),
        Parameter(
            name='lineNumber',
            data_type='uint16_t',
            index=1,
            size=1,
        ),
        Parameter(
            name='data',
            data_type='uint8_t',
            index=2,
            size=12,
        ),
    ]
    return did, cid, outputs


def get_manufacturing_date():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_manufacturing_date
    outputs = [
        Parameter(
            name='year',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='month',
            data_type='uint8_t',
            index=1,
            size=1,
        ),
        Parameter(
            name='day',
            data_type='uint8_t',
            index=2,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_sku():
    did = DevicesEnum.system_info
    cid = CommandsEnum.get_sku
    outputs = [
        Parameter(
            name='sku',
            data_type='std::string',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs
