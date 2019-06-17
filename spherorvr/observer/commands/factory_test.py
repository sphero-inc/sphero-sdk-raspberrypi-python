from spheroboros.common.commands.factory_test import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def set_test_fixture_result(test_id, fixture_id, results):
    did = DevicesEnum.factory_test
    cid = CommandsEnum.set_test_fixture_result
    inputs = [
        Parameter(
            name='test_id',
            data_type='uint16_t',
            index=0,
            value=test_id,
            size=1
        ),
        Parameter(
            name='fixture_id',
            data_type='uint16_t',
            index=1,
            value=fixture_id,
            size=1
        ),
        Parameter(
            name='results',
            data_type='uint32_t',
            index=2,
            value=results,
            size=1
        ),
    ]
    return did, cid, inputs


def get_test_fixture_result(test_id):
    did = DevicesEnum.factory_test
    cid = CommandsEnum.get_test_fixture_result
    inputs = [
        Parameter(
            name='test_id',
            data_type='uint16_t',
            index=0,
            value=test_id,
            size=1
        ),
    ],
    outputs = [
        Parameter(
            name='fixture_id',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='results',
            data_type='uint32_t',
            index=1,
            size=1,
        ),
    ]
    return did, cid, inputs, outputs


def get_factory_mode_challenge():
    did = DevicesEnum.factory_test
    cid = CommandsEnum.get_factory_mode_challenge
    outputs = [
        Parameter(
            name='security_challenge',
            data_type='uint32_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def enter_factory_mode(security_response):
    did = DevicesEnum.factory_test
    cid = CommandsEnum.enter_factory_mode
    inputs = [
        Parameter(
            name='security_response',
            data_type='uint32_t',
            index=0,
            value=security_response,
            size=1
        ),
    ]
    return did, cid, inputs


def exit_factory_mode():    
    did = DevicesEnum.factory_test
    cid = CommandsEnum.exit_factory_mode
    return did, cid


def get_chassis_id():    
    did = DevicesEnum.factory_test
    cid = CommandsEnum.get_chassis_id
    outputs = [
        Parameter(
            name='identifier',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def enable_extended_life_test(is_enabled):
    did = DevicesEnum.factory_test
    cid = CommandsEnum.enable_extended_life_test
    inputs = [
        Parameter(
            name='is_enabled',
            data_type='bool',
            index=0,
            value=is_enabled,
            size=1
        ),
    ]
    return did, cid, inputs


def get_factory_mode_status():
    did = DevicesEnum.factory_test
    cid = CommandsEnum.get_factory_mode_status
    outputs = [
        Parameter(
            name='factory_status',
            data_type='bool',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs
