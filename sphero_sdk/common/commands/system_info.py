#!/usr/bin/env python3
# This file is automatically generated!
# Source File:        0x11-system_info.json
# Device ID:          0x11
# Device Name:        system_info
# Timestamp:          07/01/2020 @ 17:22:40.061032 (UTC)

from sphero_sdk.common.enums.system_info_enums import CommandsEnum
from sphero_sdk.common.devices import DevicesEnum
from sphero_sdk.common.parameter import Parameter
from sphero_sdk.common.sequence_number_generator import SequenceNumberGenerator


def get_main_application_version(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_main_application_version,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
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
    }


def get_bootloader_version(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_bootloader_version,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
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
    }


def get_board_revision(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_board_revision,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='revision',
                data_type='uint8_t',
                index=0,
                size=1,
            ),
        ]
    }


def get_mac_address(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_mac_address,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='mac_address',
                data_type='std::string',
                index=0,
                size=1,
            ),
        ]
    }


def get_stats_id(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_stats_id,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='stats_id',
                data_type='uint16_t',
                index=0,
                size=1,
            ),
        ]
    }


def get_processor_name(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_processor_name,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='name',
                data_type='std::string',
                index=0,
                size=1,
            ),
        ]
    }


def get_sku(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_sku,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='sku',
                data_type='std::string',
                index=0,
                size=1,
            ),
        ]
    }


def get_core_up_time_in_milliseconds(target, timeout): 
    return { 
        'did': DevicesEnum.system_info,
        'cid': CommandsEnum.get_core_up_time_in_milliseconds,
        'seq': SequenceNumberGenerator.get_sequence_number(),
        'target': target,
        'timeout': timeout,
        'outputs': [ 
            Parameter( 
                name='up_time',
                data_type='uint64_t',
                index=0,
                size=1,
            ),
        ]
    }
