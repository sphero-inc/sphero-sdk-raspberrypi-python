from spheroboros.common.commands.firmware import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def jump_to_bootloader():
    did = DevicesEnum.firmware
    cid = CommandsEnum.jump_to_bootloader
    return did, cid


def get_current_application_id():
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_current_application_id
    outputs = [
        Parameter(
            name='application_id',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_all_updatable_targets():
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_all_updatable_targets
    return did, cid


def on_updatable_targets_notify():
    did = DevicesEnum.firmware
    cid = CommandsEnum.updatable_targets_notify
    outputs = [
        Parameter(
            name='id_type_array',
            data_type='tuple',
            index=0,
            size=255
        ),
    ]
    return did, cid, outputs


def get_versions_for_all_updatable_processors():
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_versions_for_all_updatable_processors
    return did, cid


def on_version_for_all_updatable_processors_notify():
    did = DevicesEnum.firmware
    cid = CommandsEnum.version_for_all_updatable_processors_notify
    outputs = [
        Parameter(
            name='version_info_array',
            data_type='tuple',
            index=0,
            size=255
        ),
    ]
    return did, cid, outputs


def set_pending_update_targets(target_ids):
    did = DevicesEnum.firmware
    cid = CommandsEnum.set_pending_update_targets
    inputs = [
        Parameter(
            name='target_ids',
            data_type='uint8_t',
            index=0,
            value=target_ids,
            size=255
        ),
    ]
    outputs = [
        Parameter(
            name='reset_strategy',
            data_type='uint8_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, inputs, outputs


def get_pending_update_targets():
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_pending_update_targets
    outputs = [
        Parameter(
            name='target_ids',
            data_type='uint8_t',
            index=0,
            size=255,
        ),
    ]
    return did, cid, outputs


def reset_with_parameters(reset_strategy):
    did = DevicesEnum.firmware
    cid = CommandsEnum.reset_with_parameters
    inputs = [
        Parameter(
            name='reset_strategy',
            data_type='uint8_t',
            index=0,
            value=reset_strategy,
            size=1
        ),
    ]
    return did, cid, inputs


def prepare_for_update(processor_id, offset, per_device_keys):
    did = DevicesEnum.firmware
    cid = CommandsEnum.prepare_for_update
    inputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            value=processor_id,
            size=1
        ),
        Parameter(
            name='offset',
            data_type='uint32_t',
            index=1,
            value=offset,
            size=1
        ),
        Parameter(
            name='per_device_keys',
            data_type='uint32_t',
            index=2,
            value=per_device_keys,
            size=4
        ),
    ]
    outputs = [
        Parameter(
            name='chunk_size',
            data_type='uint32_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='fifo_depth',
            data_type='uint8_t',
            index=1,
            size=1,
        ),
    ]
    return did, cid, inputs, outputs


def get_update_settings(processor_id):
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_update_settings
    inputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            value=processor_id,
            size=1
        ),
    ]
    outputs = [
        Parameter(
            name='chunk_size',
            data_type='uint32_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='fifo_depth',
            data_type='uint8_t',
            index=1,
            size=1,
        ),
    ]
    return did, cid, inputs, outputs


def on_ready_for_update_notify():
    did = DevicesEnum.firmware
    cid = CommandsEnum.ready_for_update_notify
    outputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            size=1
        ),
        Parameter(
            name='success',
            data_type='bool',
            index=1,
            size=1
        ),
    ]
    return did, cid, outputs


def on_chunk_write_complete_notify():
    did = DevicesEnum.firmware
    cid = CommandsEnum.chunk_write_complete_notify
    outputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            size=1
        ),
        Parameter(
            name='success',
            data_type='bool',
            index=1,
            size=1
        ),
    ]
    return did, cid, outputs


def on_get_chunk_write_completion_state():
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_chunk_write_completion_state
    return did, cid


def complete_update(processor_id):
    did = DevicesEnum.firmware
    cid = CommandsEnum.complete_update
    inputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            value=processor_id,
            size=1
        ),
    ]
    return did, cid, inputs


def on_update_completion_result_notify():
    did = DevicesEnum.firmware
    cid = CommandsEnum.update_completion_result_notify
    outputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            size=1
        ),
        Parameter(
            name='success',
            data_type='bool',
            index=1,
            size=1
        ),
    ]
    return did, cid, outputs


def get_update_completion_result(processor_id):
    did = DevicesEnum.firmware
    cid = CommandsEnum.get_update_completion_result
    inputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            value=processor_id,
            size=1
        ),
    ]
    return did, cid, inputs


def here_is_variable_sized_chunk(processor_id, chunk_index, chunk_data):
    did = DevicesEnum.firmware
    cid = CommandsEnum.here_is_variable_sized_chunk
    inputs = [
        Parameter(
            name='processor_id',
            data_type='uint8_t',
            index=0,
            value=processor_id,
            size=1
        ),
        Parameter(
            name='chunk_index',
            data_type='uint16_t',
            index=1,
            value=chunk_index,
            size=1
        ),
        Parameter(
            name='chunk_data',
            data_type='uint8_t',
            index=2,
            value=chunk_data,
            size=65535
        ),
    ]
    return did, cid, inputs


def clear_pending_update_targets(processor_ids):
    did = DevicesEnum.firmware
    cid = CommandsEnum.clear_pending_update_targets
    inputs = [
        Parameter(
            name='processor_ids',
            data_type='uint8_t',
            index=0,
            value=processor_ids,
            size=255
        ),
    ]
    return did, cid, inputs
