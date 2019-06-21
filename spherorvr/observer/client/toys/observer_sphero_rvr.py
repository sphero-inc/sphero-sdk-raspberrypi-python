import logging.config
from spherorvr.config import logging_config
from spherorvr.config import LogLevel
from spherorvr.observer.observer_base import Observer
from spherorvr.observer.dal.rvr_dal import RvrDal
from spherorvr.observer.dal.rvr_parser import RvrParser
from spherorvr.observer.dal.rvr_port import RvrSerialPort
from spherorvr.observer.events.rvr_event_dispatcher import RvrEventDispatcher
from spherorvr.observer.commands import api_and_shell
from spherorvr.observer.commands import system_info
from spherorvr.observer.commands import power
from spherorvr.observer.commands import drive
from spherorvr.observer.commands import sensor
from spherorvr.observer.commands import connection
from spherorvr.observer.commands import io

class SpheroRvr(Observer):

    def __init__(self, log_level = LogLevel.Silent):
        logging.config.dictConfig(logging_config.get_dict(log_level))
        Observer.__init__(self)
        dispatcher = RvrEventDispatcher()
        parser = RvrParser(dispatcher)
        port = RvrSerialPort(parser)
        self.__dal = RvrDal(port)

    def close(self):
        self.__dal.close()
    
    def echo(self, data, target, callback, timeout=None):
        did, \
        cid, \
        inputs, \
        outputs = api_and_shell.echo(data)
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, inputs=inputs, outputs=outputs)

    def get_api_protocol_version(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = api_and_shell.get_api_protocol_version()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_supported_dids(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = api_and_shell.get_supported_dids()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_supported_cids(self, did, target, callback, timeout=None):
        did, \
        cid, \
        outputs = api_and_shell.get_supported_cids(did)
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_main_application_version(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_main_application_version()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_bootloader_version(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_bootloader_version()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_board_revision(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_board_revision()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_mac_address(self, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_mac_address()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def get_nordic_temperature(self, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_nordic_temperature()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def get_stats_id(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_stats_id()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_processor_name(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_processor_name()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_boot_reason(self, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_boot_reason()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def get_last_error_info(self, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_last_error_info()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def get_manufacturing_date(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_manufacturing_date()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def get_sku(self, target, callback, timeout=None):
        did, \
        cid, \
        outputs = system_info.get_sku()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)

    def enter_deep_sleep(self, seconds_until_deep_sleep, timeout=None):
        did, \
        cid, \
        inputs = power.enter_deep_sleep(seconds_until_deep_sleep)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, inputs=inputs)

    def enter_soft_sleep(self, timeout=None):
        did, \
        cid = power.enter_soft_sleep()
        self.__dal.send_command(did, cid, target=1, timeout=timeout)

    def wake(self, timeout=None):
        did, \
        cid = power.wake()
        self.__dal.send_command(did, cid, target=1, timeout=timeout)

    def get_battery_percentage(self, callback, timeout=None):
        did, \
        cid, \
        outputs = power.get_battery_percentage()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def get_battery_voltage_state(self, callback, timeout=None):
        did, \
        cid, \
        outputs = power.get_battery_voltage_state()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, outputs=outputs)

    def on_will_sleep_notify(self, callback):
        did, \
        cid = power.on_will_sleep_notify()
        self._register_callback(did, cid, callback)

    def on_did_sleep_notify(self, callback):
        did, \
        cid = power.on_did_sleep_notify()
        self._register_callback(did, cid, callback)

    def enable_battery_voltage_state_change_notify(self, is_enabled, timeout=None):
        did, \
        cid, \
        inputs = power.enable_battery_voltage_state_change_notify(is_enabled)
        self.__dal.send_command(did, cid, target=1, timeout=timeout, inputs=inputs)

    def on_battery_voltage_state_change_notify(self, callback):
        did, \
        cid, \
        outputs = power.on_battery_voltage_state_change_notify()
        self._register_callback(did, cid, callback, outputs)

    def raw_motors(self, left_mode, left_speed, right_mode, right_speed, timeout=None):
        did, \
        cid, \
        inputs = drive.raw_motors(left_mode, left_speed, right_mode, right_speed)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, inputs=inputs)

    def reset_yaw(self, timeout=None):
        did, \
        cid = drive.reset_yaw()
        self.__dal.send_command(did, cid, target=2, timeout=timeout)

    def drive_with_heading(self, speed, heading, flags, timeout=None):
        did, \
        cid, \
        inputs = drive.drive_with_heading(speed, heading, flags)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, inputs=inputs)

    def set_sensor_streaming_mask(self, interval, packet_count, data_mask, timeout=None):
        did, \
        cid, \
        inputs = sensor.set_sensor_streaming_mask(interval, packet_count, data_mask)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, inputs=inputs)

    def get_sensor_streaming_mask(self, callback, timeout=None):
        did, \
        cid, \
        outputs = sensor.get_sensor_streaming_mask()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, outputs=outputs)

    def on_sensor_streaming_data_notify(self, callback):
        did, \
        cid, \
        outputs = sensor.on_sensor_streaming_data_notify()
        self._register_callback(did, cid, callback, outputs)

    def get_encoder_counts(self, callback, timeout=None):
        did, \
        cid, \
        outputs = sensor.get_encoder_counts()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, outputs=outputs)

    def get_euler_angles(self, callback, timeout=None):
        did, \
        cid, \
        outputs = sensor.get_euler_angles()
        self._register_callback(did, cid, callback, outputs)
        self.__dal.send_command(did, cid, target=2, timeout=timeout, outputs=outputs)


    '''def get_gyro_degrees_per_second(self, timeout=None):
        sensor.get_gyro_degrees_per_second(self, target=2, timeout=timeout)

    def set_extended_sensor_streaming_mask(self, data_mask, timeout=None):
        sensor.set_extended_sensor_streaming_mask(self, data_mask, target=2, timeout=timeout)

    def get_extended_sensor_streaming_mask(self, timeout=None):
        sensor.get_extended_sensor_streaming_mask(self, target=2, timeout=timeout)

    def enable_gyro_max_notify(self, is_enabled, timeout=None):
        sensor.enable_gyro_max_notify(self, is_enabled, target=2, timeout=timeout)

    def on_gyro_max_notify(self, handler=None, timeout=None):
        return asyncio.ensure_future(
            sensor.on_gyro_max_notify(self, target=2, handler=handler, timeout=timeout)
        )

    def configure_collision_detection(self, method, x_threshold, x_speed, y_threshold, y_speed, dead_time, timeout=None):
        sensor.configure_collision_detection(self, method, x_threshold, x_speed, y_threshold, y_speed, dead_time, target=2, timeout=timeout)

    def on_collision_detected_notify(self, handler=None, timeout=None):
        return asyncio.ensure_future(
            sensor.on_collision_detected_notify(self, target=2, handler=handler, timeout=timeout)
        )

    def get_bot_to_bot_infrared_readings(self, timeout=None):
        sensor.get_bot_to_bot_infrared_readings(self, target=2, timeout=timeout)

    def start_robot_to_robot_infrared_broadcasting(self, far_code, near_code, timeout=None):
        sensor.start_robot_to_robot_infrared_broadcasting(self, far_code, near_code, target=2, timeout=timeout)

    def stop_robot_to_robot_infrared_broadcasting(self, timeout=None):
        sensor.stop_robot_to_robot_infrared_broadcasting(self, target=2, timeout=timeout)

    def send_robot_to_robot_infrared_message(self, infrared_code, front_left_strength, front_right_strength, back_right_strength, back_left_strength, timeout=None):
        sensor.send_robot_to_robot_infrared_message(self, infrared_code, front_left_strength, front_right_strength, back_right_strength, back_left_strength, target=2, timeout=timeout)

    def listen_for_robot_to_robot_infrared_message(self, infrared_code, listen_duration, timeout=None):
        sensor.listen_for_robot_to_robot_infrared_message(self, infrared_code, listen_duration, target=2, timeout=timeout)

    def on_robot_to_robot_infrared_message_received_notify(self, handler=None, timeout=None):
        return asyncio.ensure_future(
            sensor.on_robot_to_robot_infrared_message_received_notify(self, target=2, handler=handler, timeout=timeout)
        )

    def get_ambient_light_sensor_value(self, timeout=None):
        sensor.get_ambient_light_sensor_value(self, target=1, timeout=timeout)

    def enable_color_detection_notification(self, enable, interval, minimum_confidence_threshold, timeout=None):
        sensor.enable_color_detection_notification(self, enable, interval, minimum_confidence_threshold, target=1, timeout=timeout)

    def on_color_detection_notify(self, handler=None, timeout=None):
        return asyncio.ensure_future(
            sensor.on_color_detection_notify(self, target=1, handler=handler, timeout=timeout)
        )

    def get_current_detected_color_reading(self, timeout=None):
        sensor.get_current_detected_color_reading(self, target=1, timeout=timeout)

    def enable_color_detection(self, enable, timeout=None):
        sensor.enable_color_detection(self, enable, target=1, timeout=timeout)'''

