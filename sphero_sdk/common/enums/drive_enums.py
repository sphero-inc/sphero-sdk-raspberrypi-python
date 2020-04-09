#!/usr/bin/env python3
# This file is automatically generated!
# Source File:        0x16-driving.json
# Device ID:          0x16
# Device Name:        drive
# Timestamp:          04/09/2020 @ 21:22:32.681519 (UTC)

from enum import IntEnum


__all__ = ['LinearVelocitySlewMethodsEnum',
           'RawMotorModesEnum',
           'MotorIndexesEnum',
           'DriveFlagsBitmask',
           'XyPositionDriveFlagsBitmask',
           'RcDriveFlagsBitmask']


class CommandsEnum(IntEnum): 
    raw_motors = 0x01
    reset_yaw = 0x06
    drive_with_heading = 0x07
    set_custom_control_system_timeout = 0x22
    enable_motor_stall_notify = 0x25
    motor_stall_notify = 0x26
    enable_motor_fault_notify = 0x27
    motor_fault_notify = 0x28
    get_motor_fault_state = 0x29
    drive_tank_si_units = 0x32
    drive_tank_normalized = 0x33
    drive_rc_si_units = 0x34
    drive_rc_normalized = 0x35
    drive_with_yaw_si = 0x36
    drive_with_yaw_normalized = 0x37
    drive_to_position_si = 0x38
    drive_to_position_normalized = 0x39
    xy_position_drive_result_notify = 0x3A
    set_drive_target_slew_parameters = 0x3C
    get_drive_target_slew_parameters = 0x3D
    stop_active_controller_custom_decel = 0x3E
    active_controller_stopped_notify = 0x3F
    restore_default_drive_target_slew_parameters = 0x40
    get_stop_controller_state = 0x41
    stop_active_controller = 0x42


class LinearVelocitySlewMethodsEnum(IntEnum):
    constant = 0
    proportional = 1


class RawMotorModesEnum(IntEnum):
    off = 0
    forward = 1
    reverse = 2


class MotorIndexesEnum(IntEnum):
    left_motor_index = 0
    right_motor_index = 1


class DriveFlagsBitmask(IntEnum):
    none = 0
    drive_reverse = 1
    boost = 2
    fast_turn = 4
    left_direction = 8
    right_direction = 16
    enable_drift = 32


class XyPositionDriveFlagsBitmask(IntEnum):
    none = 0
    force_reverse = 1
    auto_reverse = 2


class RcDriveFlagsBitmask(IntEnum):
    none = 0
    slew_linear_velocity = 1
