from spheroboros.common.commands.power import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


async def enter_deep_sleep(self, seconds_until_deep_sleep):
    did = DevicesEnum.power
    cid = CommandsEnum.enter_deep_sleep
    inputs=[
        Parameter(
            name='secondsUntilDeepSleep',
            data_type='uint8_t',
            index=0,
            value=seconds_until_deep_sleep,
            size=1
        ),
    ]
    return did, cid, inputs


async def enter_soft_sleep():
    did = DevicesEnum.power
    cid = CommandsEnum.enter_soft_sleep
    return did, cid


async def wake():
    did = DevicesEnum.power
    cid = CommandsEnum.wake
    return did, cid


async def get_battery_percentage():
    did = DevicesEnum.power
    cid = CommandsEnum.get_battery_percentage
    outputs=[
        Parameter(
            name='percentage',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


async def get_battery_voltage_state():
    did = DevicesEnum.power
    cid = CommandsEnum.get_battery_voltage_state
    outputs=[
        Parameter(
            name='state',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


async def on_will_sleep_notify():
    did = DevicesEnum.power
    cid = CommandsEnum.will_sleep_notify,
    return did, cid


async def on_did_sleep_notify():
    did = DevicesEnum.power
    cid = CommandsEnum.did_sleep_notify,
    return did, cid
    


async def enable_battery_voltage_state_change_notify(is_enabled):
    did = DevicesEnum.power
    cid = CommandsEnum.enable_battery_voltage_state_change_notify
    inputs=[
        Parameter(
            name='isEnabled',
            data_type='bool',
            index=0,
            value=is_enabled,
            size=1
        ),
    ]
    return did, cid, inputs


async def on_battery_voltage_state_change_notify():
    did = DevicesEnum.power
    cid = CommandsEnum.battery_voltage_state_change_notify,
    outputs=[
        Parameter(
            name='state',
            data_type='uint8_t',
            index=0,
            size=1
        ),
    ]
    return did, cid, outputs
