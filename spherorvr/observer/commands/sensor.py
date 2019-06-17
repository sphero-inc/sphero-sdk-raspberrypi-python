from spheroboros.common.commands.sensor import CommandsEnum
from spheroboros.common.devices import DevicesEnum
from spheroboros.common.parameter import Parameter


def set_sensor_streaming_mask(interval, packet_count, data_mask):
    did = DevicesEnum.sensor
    cid = CommandsEnum.set_sensor_streaming_mask
    inputs = [
        Parameter(
            name='interval',
            data_type='uint16_t',
            index=0,
            value=interval,
            size=1
        ),
        Parameter(
            name='packetCount',
            data_type='uint8_t',
            index=1,
            value=packet_count,
            size=1
        ),
        Parameter(
            name='dataMask',
            data_type='uint32_t',
            index=2,
            value=data_mask,
            size=1
        ),
    ]
    return did, cid, inputs


def get_sensor_streaming_mask():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_sensor_streaming_mask
    outputs = [
        Parameter(
            name='interval',
            data_type='uint16_t',
            index=0,
            size=1,
        ),
        Parameter(
            name='packetCount',
            data_type='uint8_t',
            index=1,
            size=1,
        ),
        Parameter(
            name='dataMask',
            data_type='uint32_t',
            index=2,
            size=1,
        ),
    ]
    return did, cid, outputs


def on_sensor_streaming_data_notify():
    did = DevicesEnum.sensor
    cid = CommandsEnum.sensor_streaming_data_notify
    outputs = [
        Parameter(
            name='sensorData',
            data_type='float',
            index=0,
            size=255
        ),
    ]
    return did, cid, outputs


def get_encoder_counts():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_encoder_counts
    outputs = [
        Parameter(
            name='encoderCounts',
            data_type='int16_t',
            index=0,
            size=2,
        ),
    ]
    return did, cid, outputs


def get_euler_angles():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_euler_angles
    outputs = [
        Parameter(
            name='pitch',
            data_type='float',
            index=0,
            size=1,
        ),
        Parameter(
            name='roll',
            data_type='float',
            index=1,
            size=1,
        ),
        Parameter(
            name='extendedRoll',
            data_type='float',
            index=2,
            size=1,
        ),
        Parameter(
            name='yaw',
            data_type='float',
            index=3,
            size=1,
        ),
    ]
    return did, cid, outputs


def get_gyro_degrees_per_second():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_gyro_degrees_per_second
    outputs = [
        Parameter(
            name='pitch',
            data_type='float',
            index=0,
            size=1,
        ),
        Parameter(
            name='roll',
            data_type='float',
            index=1,
            size=1,
        ),
        Parameter(
            name='yaw',
            data_type='float',
            index=2,
            size=1,
        ),
    ]
    return did, cid, outputs


def set_extended_sensor_streaming_mask(data_mask):
    did = DevicesEnum.sensor
    cid = CommandsEnum.set_extended_sensor_streaming_mask
    inputs = [
        Parameter(
            name='dataMask',
            data_type='uint32_t',
            index=0,
            value=data_mask,
            size=1
        ),
    ]


def get_extended_sensor_streaming_mask():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_extended_sensor_streaming_mask
    outputs = [
        Parameter(
            name='dataMask',
            data_type='uint32_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def enable_gyro_max_notify(is_enabled):
    did = DevicesEnum.sensor
    cid = CommandsEnum.enable_gyro_max_notify
    inputs = [
        Parameter(
            name='isEnabled',
            data_type='bool',
            index=0,
            value=is_enabled,
            size=1
        ),
    ]
    return did, cid, inputs


def on_gyro_max_notify():
    did = DevicesEnum.sensor
    cid = CommandsEnum.gyro_max_notify
    outputs = [
        Parameter(
            name='flags',
            data_type='uint8_t',
            index=0,
            size=1
        ),
    ]
    return did, cid, outputs


def configure_collision_detection(method, x_threshold, x_speed, y_threshold, y_speed, dead_time):
    did = DevicesEnum.sensor
    cid = CommandsEnum.configure_collision_detection
    inputs = [
        Parameter(
            name='method',
            data_type='uint8_t',
            index=0,
            value=method,
            size=1
        ),
        Parameter(
            name='xThreshold',
            data_type='uint8_t',
            index=1,
            value=x_threshold,
            size=1
        ),
        Parameter(
            name='xSpeed',
            data_type='uint8_t',
            index=2,
            value=x_speed,
            size=1
        ),
        Parameter(
            name='yThreshold',
            data_type='uint8_t',
            index=3,
            value=y_threshold,
            size=1
        ),
        Parameter(
            name='ySpeed',
            data_type='uint8_t',
            index=4,
            value=y_speed,
            size=1
        ),
        Parameter(
            name='deadTime',
            data_type='uint8_t',
            index=5,
            value=dead_time,
            size=1
        ),
    ]
    return did, cid, inputs


def on_collision_detected_notify():
    did = DevicesEnum.sensor
    cid = CommandsEnum.collision_detected_notify
    outputs = [
        Parameter(
            name='accelerationX',
            data_type='uint16_t',
            index=0,
            size=1
        ),
        Parameter(
            name='accelerationY',
            data_type='uint16_t',
            index=1,
            size=1
        ),
        Parameter(
            name='accelerationZ',
            data_type='uint16_t',
            index=2,
            size=1
        ),
        Parameter(
            name='axis',
            data_type='uint8_t',
            index=3,
            size=1
        ),
        Parameter(
            name='powerX',
            data_type='uint16_t',
            index=4,
            size=1
        ),
        Parameter(
            name='powerY',
            data_type='uint16_t',
            index=5,
            size=1
        ),
        Parameter(
            name='speed',
            data_type='uint8_t',
            index=6,
            size=1
        ),
        Parameter(
            name='time',
            data_type='uint32_t',
            index=7,
            size=1
        ),
    ]
    return did, cid, outputs


def get_bot_to_bot_infrared_readings():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_bot_to_bot_infrared_readings
    outputs = [
        Parameter(
            name='sensorData',
            data_type='uint32_t',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def start_robot_to_robot_infrared_broadcasting(far_code, near_code):
    did = DevicesEnum.sensor
    cid = CommandsEnum.start_robot_to_robot_infrared_broadcasting
    inputs = [
        Parameter(
            name='farCode',
            data_type='uint8_t',
            index=0,
            value=far_code,
            size=1
        ),
        Parameter(
            name='nearCode',
            data_type='uint8_t',
            index=1,
            value=near_code,
            size=1
        ),
    ]
    return did, cid, inputs


def stop_robot_to_robot_infrared_broadcasting():
    did = DevicesEnum.sensor
    cid = CommandsEnum.stop_robot_to_robot_infrared_broadcasting
    return did, cid


def send_robot_to_robot_infrared_message(infrared_code, front_left_strength, front_right_strength, back_right_strength, back_left_strength):
    did = DevicesEnum.sensor
    cid = CommandsEnum.send_robot_to_robot_infrared_message
    inputs = [
        Parameter(
            name='infraredCode',
            data_type='uint8_t',
            index=0,
            value=infrared_code,
            size=1
        ),
        Parameter(
            name='frontLeftStrength',
            data_type='uint8_t',
            index=1,
            value=front_left_strength,
            size=1
        ),
        Parameter(
            name='frontRightStrength',
            data_type='uint8_t',
            index=2,
            value=front_right_strength,
            size=1
        ),
        Parameter(
            name='backRightStrength',
            data_type='uint8_t',
            index=3,
            value=back_right_strength,
            size=1
        ),
        Parameter(
            name='backLeftStrength',
            data_type='uint8_t',
            index=4,
            value=back_left_strength,
            size=1
        ),
    ]
    return did, cid, inputs


def listen_for_robot_to_robot_infrared_message(infrared_code, listen_duration):
    did = DevicesEnum.sensor
    cid = CommandsEnum.listen_for_robot_to_robot_infrared_message
    inputs = [
        Parameter(
            name='infraredCode',
            data_type='uint8_t',
            index=0,
            value=infrared_code,
            size=1
        ),
        Parameter(
            name='listenDuration',
            data_type='uint32_t',
            index=1,
            value=listen_duration,
            size=1
        ),
    ]
    return did, cid, inputs


def on_robot_to_robot_infrared_message_received_notify():
    did = DevicesEnum.sensor
    cid = CommandsEnum.robot_to_robot_infrared_message_received_notify
    outputs = [
        Parameter(
            name='infraredCode',
            data_type='uint8_t',
            index=0,
            size=1
        ),
    ]
    return did, cid, outputs


def get_ambient_light_sensor_value():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_ambient_light_sensor_value
    outputs = [
        Parameter(
            name='ambientLightWhiteChannelValue',
            data_type='float',
            index=0,
            size=1,
        ),
    ]
    return did, cid, outputs


def enable_color_detection_notification(enable, interval, minimum_confidence_threshold):
    did = DevicesEnum.sensor
    cid = CommandsEnum.enable_color_detection_notification
    inputs = [
        Parameter(
            name='enable',
            data_type='bool',
            index=0,
            value=enable,
            size=1
        ),
        Parameter(
            name='interval',
            data_type='uint16_t',
            index=1,
            value=interval,
            size=1
        ),
        Parameter(
            name='minimumConfidenceThreshold',
            data_type='uint8_t',
            index=2,
            value=minimum_confidence_threshold,
            size=1
        ),
    ]
    return did, cid, inputs


def on_color_detection_notify():
    did = DevicesEnum.sensor
    cid = CommandsEnum.color_detection_notify
    outputs = [
        Parameter(
            name='red',
            data_type='uint8_t',
            index=0,
            size=1
        ),
        Parameter(
            name='green',
            data_type='uint8_t',
            index=1,
            size=1
        ),
        Parameter(
            name='blue',
            data_type='uint8_t',
            index=2,
            size=1
        ),
        Parameter(
            name='confidence',
            data_type='uint8_t',
            index=3,
            size=1
        ),
        Parameter(
            name='colorClassification',
            data_type='uint8_t',
            index=4,
            size=1
        ),
    ]
    return did, cid, outputs


def get_current_detected_color_reading():
    did = DevicesEnum.sensor
    cid = CommandsEnum.get_current_detected_color_reading
    return did, cid


def enable_color_detection(enable):
    did = DevicesEnum.sensor
    cid = CommandsEnum.enable_color_detection
    inputs = [
        Parameter(
            name='enable',
            data_type='bool',
            index=0,
            value=enable,
            size=1
        ),
    ]
    return did, cid, inputs
