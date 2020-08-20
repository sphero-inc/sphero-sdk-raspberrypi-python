import logging
from .sensor_stream_attribute import SensorStreamAttribute
from .sensor_stream_service import SensorStreamService
from .sensor_stream_slot import SensorStreamSlot
from sphero_sdk import SpheroRvrTargets
from sphero_sdk.common.enums.sensor_enums import StreamingDataSizesEnum
from sphero_sdk.common.enums.number_bounds_enums import UintBounds

logger = logging.getLogger(__name__)


class SensorStreamingControl:
    # TODO: there are mixed styles of constants in sphero_sdk. we need to pick one and update
    slot_token_1 = 0x01
    slot_token_2 = 0x02
    slot_token_3 = 0x03
    slot_token_4 = 0x04
    valid_success_status = 0x00
    min_streaming_interval = 33

    def __init__(self, rvr):
        self._rvr = rvr
        self._sensor_handlers = {}
        self.__nordic_service_slots_by_token = {}
        self.__st_service_slots_by_token = {}
        self.__streaming_services_by_name = {}
        self.__enabled_sensors = []
        self.__streaming_interval = 0
        self.__init_service_slots()
        self.__init_services()

    @property
    def supported_sensors(self):
        """Returns a list of supported sensors for RVR

        """
        return self.__streaming_services_by_name.keys()

    @property
    def enabled_sensors(self):
        """Returns a list of currently enabled sensors

        """
        return self.__enabled_sensors.copy()

    @property
    def streaming_interval(self):
        """Returns the current sensor streaming interval

        """
        return self.__streaming_interval

    def add_sensor_data_handler(self, service, handler):
        """Adds a callback function for the service specified.  Handler must define only one parameter to contain
        sensor data as a dictionary.  Changes take effect once streaming is started.  If already streaming, stop()
        must be called first.

        Args:
            service (str):  Name of the sensor streaming service.
            handler (function): Function to receive sensor stream callbacks

        Examples:
            $ def imu_handler(self, imu_data):
                  pitch = imu_data['Pitch']
                  roll = imu_data['Roll']
                  yaw = imu_data['Yaw']

            $ def accel_handler(self, accel_data):
                  x = accel_data['X']
                  y = accel_data['Y']
                  z = accel_data['Z']

            $ rvr.sensor_control.add_sensor_data_handler('IMU', imu_handler)
            $ rvr.sensor_control.add_sensor_data_handler('Accelerometer', accel_handler)
            $ rvr.sensor_control.start(interval=100)
        """

        if service in self._sensor_handlers.keys():
            logger.warning('Handler already registered for service \'{}\'.'.format(service))
            return

        self._sensor_handlers[service] = handler
        logger.info('Adding {} service handler'.format(service))

    def remove_sensor_data_handler(self, service):
        """Removes a callback for the service specified, which consequently also removes the service
        from RVR's streaming data configuration.  Changes take effect once streaming is started.  If
        already streaming, stop() must be called first.

        Args:
            service (str):  Name of the sensor streaming service.

        """

        if service not in self._sensor_handlers.keys():
            logger.warning('Handler not registered for service \'{}\'.'.format(service))
            return

        self._sensor_handlers.pop(service)
        logger.info('Removed {} service handler'.format(service))

    def start(self, interval):
        """Starts the specified sensors streams by name at the configured streaming interval

        Args:
            interval (uint16): Rate of data streaming in milliseconds

        """

        if len(self.__enabled_sensors) > 0:
            logger.error('Streaming services already started, call stop() first!')
            return

        if interval < self.min_streaming_interval:
            raise ValueError('Cannot set streaming interval lower than {}} milliseconds!'.format(self.min_streaming_interval))

        has_change = False
        service_names = self._sensor_handlers.keys()

        for sensor_name in service_names:
            if sensor_name in self.__enabled_sensors:
                continue

            self.__enabled_sensors.append(sensor_name)
            has_change = True

        if not has_change:
            logger.error('Attempted to start sensor streaming, but no sensors enabled!')
            return

        self.__streaming_interval = interval
        self.__add_service_handlers()
        self.__configure_services()
        self.__start_services()

    def stop(self):
        """Disables the specified sensors streams by name

        """
        if len(self.__enabled_sensors) == 0:
            logger.info('No enabled sensors to stop.')
            return

        self.__stop_and_clear_services()
        self.__enabled_sensors.clear()

    def clear(self):
        """Disables all sensor streams

        """
        if len(self.__enabled_sensors) == 0:
            logger.info('No enabled sensors to disable.')
            return

        logger.info('Disabling all streaming services.')

        self._sensor_handlers.clear()
        self.__stop_and_clear_services()
        self.__enabled_sensors.clear()
        self.__reset_services(SpheroRvrTargets.primary.value)
        self.__reset_services(SpheroRvrTargets.secondary.value)

    def _configure_streaming_service(self, token_id, configuration, processor):
        raise NotImplementedError('Missing implementation, subclasses should implement this!')

    def _add_streaming_service_data_notify_handler(self, processor):
        raise NotImplementedError('Missing implementation, subclasses should implement this!')

    def _start_streaming_service(self, interval, processor):
        raise NotImplementedError('Missing implementation, subclasses should implement this!')

    def _stop_streaming_service(self, processor):
        raise NotImplementedError('Missing implementation, subclasses should implement this!')

    def _stop_and_clear_streaming_service(self, processor):
        raise NotImplementedError('Missing implementation, subclasses should implement this!')

    def _process_streaming_response(self, processor, response):
        response_token_uint8 = response['token']
        raw_sensor_data = response['sensor_data']
        raw_start_index = 0
        status_flag = response_token_uint8 & 0xF0  # Check the upper nibble for flag value: 0x0 = OK, 0x1 = Invalid Data
        token_id = response_token_uint8 & 0x0F # Check the lower nibble for token id
        is_valid = status_flag == self.valid_success_status

        logger.debug(
            'Token: {}, Processor: {} Status: {}, Sensor Data: {}'.format(
                token_id,
                processor,
                status_flag,
                '[{}]'.format(', '.join('0x{:02x}'.format(x) for x in raw_sensor_data))
            )
        )

        processor_service_slots = self.__get_processor_service_slots(processor)
        service_slot = processor_service_slots[token_id]

        if service_slot is None:
            logger.error('Retrieved null streaming service slot for processor {}, token {}.'.format(processor, token_id))
            return

        if len(service_slot.enabled_streaming_services_by_id) == 0:
            logger.error('Attempting to process streaming data before services in slot are enabled! Clearing services.')
            self.__stop_and_clear_services()
            return

        streaming_services_by_id = service_slot.enabled_streaming_services_by_id
        service_ids = streaming_services_by_id.keys()
        parsed_service_data = {}
        for id in service_ids:
            streaming_service = streaming_services_by_id[id]

            if streaming_service is None:
                logger.error('Retrieved null streaming service for service id {}'.format(id))

            # calculate how many bytes to copy from raw data array for the current service
            slice_length = len(streaming_service.attributes) * streaming_service.byte_count
            raw_end_index = raw_start_index + slice_length

            # slice from raw data
            sensor_data_bytes = raw_sensor_data[raw_start_index: raw_end_index]

            # end index becomes new start index
            raw_start_index = raw_end_index

            # get attribute value dictionary
            attribute_dictionary = streaming_service.parse_attribute_bytes_to_floats(sensor_data_bytes)

            # merge is_valid flag and attribute values into one dictionary for current streaming service
            sensor_data_dictionary = {'is_valid': is_valid, **attribute_dictionary}

            # add entry into parsed service data dictionary being returned to the user
            parsed_service_data[streaming_service.name] = sensor_data_dictionary

        if len(parsed_service_data) == 0:
            raise Exception('Parsed empty sensor data for processor {}, token {}'.format(processor, token_id))

        return parsed_service_data

    def __add_service_handlers(self):
        self._add_streaming_service_data_notify_handler(SpheroRvrTargets.primary.value)
        self._add_streaming_service_data_notify_handler(SpheroRvrTargets.secondary.value)

    def __configure_services(self):
        self.__configure_services_for_processor(SpheroRvrTargets.primary.value)
        self.__configure_services_for_processor(SpheroRvrTargets.secondary.value)

    def __configure_services_for_processor(self, processor):
        # step 1: reset existing streaming service configurations in each slot
        self.__reset_services(processor)

        # step 2: enable streaming services in each slot
        for enabled_sensor_name in self.__enabled_sensors:
            if enabled_sensor_name not in self.__streaming_services_by_name.keys():
                continue

            streaming_service_slots = self.__streaming_services_by_name[enabled_sensor_name]

            if streaming_service_slots is None or len(streaming_service_slots) == 0:
                continue

            for service_slot in streaming_service_slots:
                if service_slot.processor != processor:
                    continue
                service_slot.enable_streaming_service(enabled_sensor_name)

        # step 3: generate streaming service configurations for each slot and send command
        streaming_service_slots_by_token = self.__get_processor_service_slots(processor)

        service_enabled = False
        for token in streaming_service_slots_by_token.keys():
            service_slot = streaming_service_slots_by_token[token]

            if service_slot is None:
                logger.error('Retrieved null service slot!')
                continue

            if not service_slot.has_enabled_streaming_services:
                logger.info('Slot has no enabled services')
                continue

            service_enabled = True
            configuration = service_slot.streaming_services_configuration
            self._configure_streaming_service(token, configuration, processor)

        # step 4: start streaming services
        if not service_enabled:
            logger.info('No services enabled during configuration.')
            return

    def __start_services(self):
        self._start_streaming_service(self.__streaming_interval, SpheroRvrTargets.primary.value)
        self._start_streaming_service(self.__streaming_interval, SpheroRvrTargets.secondary.value)

    def __stop_services(self):
        self._stop_streaming_service(SpheroRvrTargets.primary.value)
        self._stop_streaming_service(SpheroRvrTargets.secondary.value)

    def __stop_and_clear_services(self):
        self._stop_and_clear_streaming_service(SpheroRvrTargets.primary.value)
        self._stop_and_clear_streaming_service(SpheroRvrTargets.secondary.value)

    def __reset_services(self, processor):
        for streaming_service_name in self.__streaming_services_by_name.keys():
            service_slots = self.__streaming_services_by_name[streaming_service_name]

            if service_slots is None:
                continue

            for i in range(len(service_slots)):
                service_slot = service_slots[i]

                if service_slot.processor != processor:
                    continue

                service_slot.disable_all_streaming_services()

    def __init_services(self):
        """
        streaming service configuration for RVR:
        | Id     | Processor          | Token | Service            | Attributes                 |
        | ------ | ------------- -----| ----- | ------------------ | -------------------------- |
        | 0x0003 | Nordic (1)         | 1     | ColorDetection     | R, G, B, Index, Confidence |
        | 0x000A | Nordic (1)         | 2     | AmbientLight       | Light                      |
        -----------------------------------------------------------------------------------------
        | 0x0000 | ST (2)             | 1     | Quaternion         | W, X, Y, Z                 |
        | 0x0001 | ST (2)             | 1     | IMU                | Pitch, Roll, Yaw           |
        | 0x0002 | ST (2)             | 1     | Accelerometer      | X, Y, Z                    |
        | 0x0004 | ST (2)             | 1     | Gyroscope          | X, Y, Z                    |
        | 0x0006 | ST (2)             | 2     | Locator            | X, Y                       |
        | 0x0007 | ST (2)             | 2     | Velocity           | X, Y                       |
        | 0x0008 | ST (2)             | 2     | Speed              | Speed                      |
        | 0x000B | ST (2)             | 2     | Encoders           | Left, Right                |
        -----------------------------------------------------------------------------------------
        | 0x0009 | Nordic (1), ST (2) | 3     | CoreTime           | TimeUpper, TimeLower       |
        -----------------------------------------------------------------------------------------
        """

        # Quaternion
        attributes = [
            SensorStreamAttribute('W', -1.0, 1.0),
            SensorStreamAttribute('X', -1.0, 1.0),
            SensorStreamAttribute('Y', -1.0, 1.0),
            SensorStreamAttribute('Z', -1.0, 1.0)
        ]
        streaming_service = SensorStreamService(
            0x0000,
            'Quaternion',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_1)

        # IMU
        attributes = [
            SensorStreamAttribute('Pitch', -180.0, 180.0),
            SensorStreamAttribute('Roll', -90.0, 90.0),
            SensorStreamAttribute('Yaw', -180.0, 180.0)
        ]
        streaming_service = SensorStreamService(
            0x0001,
            'IMU',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_1)

        # Accelerometer
        attributes = [
            SensorStreamAttribute('X', -16.0, 16.0),
            SensorStreamAttribute('Y', -16.0, 16.0),
            SensorStreamAttribute('Z', -16.0, 16.0)
        ]
        streaming_service = SensorStreamService(
            0x0002,
            'Accelerometer',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_1)

        # Color detection
        attributes = [
            SensorStreamAttribute('R', 0, 255),
            SensorStreamAttribute('G', 0, 255),
            SensorStreamAttribute('B', 0, 255),
            SensorStreamAttribute('Index', 0, 255),
            SensorStreamAttribute('Confidence', 0.0, 1.0)
        ]
        streaming_service = SensorStreamService(
            0x0003,
            'ColorDetection',
            StreamingDataSizesEnum.eight_bit,
            attributes,
            [SpheroRvrTargets.primary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_1)

        # Gyroscope
        attributes = [
            SensorStreamAttribute('X', -2000.0, 2000.0),
            SensorStreamAttribute('Y', -2000.0, 2000.0),
            SensorStreamAttribute('Z', -2000.0, 2000.0)
        ]
        streaming_service = SensorStreamService(
            0x0004,
            'Gyroscope',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_1)

        # Locator
        attributes = [
            SensorStreamAttribute('X', -16000.0, 16000.0),
            SensorStreamAttribute('Y', -16000.0, 16000.0)
        ]
        streaming_service = SensorStreamService(
            0x0006,
            'Locator',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_2)

        # Velocity
        attributes = [
            SensorStreamAttribute('X', -5.0, 5.0),
            SensorStreamAttribute('Y', -5.0, 5.0)
        ]
        streaming_service = SensorStreamService(
            0x0007,
            'Velocity',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_2)

        # Speed
        attributes = [
            SensorStreamAttribute('Speed', 0.0, 5.0),
        ]
        streaming_service = SensorStreamService(
            0x0008,
            'Speed',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_2)

        # Core Time
        attributes = [
            SensorStreamAttribute('TimeUpper', 0, UintBounds.uint_32_max),
            SensorStreamAttribute('TimeLower', 0, UintBounds.uint_32_max)
        ]
        streaming_service = SensorStreamService(
            0x0009,
            'CoreTime',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.primary.value, SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_3)

        # Ambient Light
        attributes = [
            SensorStreamAttribute('Light', 0.0, 120000.0),
        ]
        streaming_service = SensorStreamService(
            0x000A,
            'AmbientLight',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.primary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_2)

        # Encoder ticks
        attributes = [
            SensorStreamAttribute('LeftTicks', 0, UintBounds.uint_32_max),
            SensorStreamAttribute('RightTicks', 0, UintBounds.uint_32_max)
        ]
        streaming_service = SensorStreamService(
            0x000B,
            'Encoders',
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [SpheroRvrTargets.secondary.value]
        )
        self.__add_service_to_slot(streaming_service, self.slot_token_2)

    def __add_service_to_slot(self, streaming_service, token):
        slots = []

        for processor in streaming_service.processors:
            processor_service_slots = self.__get_processor_service_slots(processor)
            service_slot = processor_service_slots[token]

            if service_slot is None:
                logger.log('Retrieved null service slot for token {} and processor {}'.format(token, processor))
                continue

            service_slot.add_streaming_service(streaming_service)
            slots.append(service_slot)

        self.__streaming_services_by_name[streaming_service.name] = slots

    def __init_service_slots(self):
        self.__nordic_service_slots_by_token.clear()
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.slot_token_1, SpheroRvrTargets.primary.value)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.slot_token_2, SpheroRvrTargets.primary.value)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.slot_token_3, SpheroRvrTargets.primary.value)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.slot_token_4, SpheroRvrTargets.primary.value)

        self.__st_service_slots_by_token.clear()
        self.__init_service_slot(self.__st_service_slots_by_token, self.slot_token_1, SpheroRvrTargets.secondary.value)
        self.__init_service_slot(self.__st_service_slots_by_token, self.slot_token_2, SpheroRvrTargets.secondary.value)
        self.__init_service_slot(self.__st_service_slots_by_token, self.slot_token_3, SpheroRvrTargets.secondary.value)
        self.__init_service_slot(self.__st_service_slots_by_token, self.slot_token_4, SpheroRvrTargets.secondary.value)

    def __get_processor_service_slots(self, processor):
        return self.__nordic_service_slots_by_token \
            if processor == SpheroRvrTargets.primary.value \
            else self.__st_service_slots_by_token

    def __init_service_slot(self, processor_service_slots_by_token, token, processor):
        service_slot = SensorStreamSlot(token, processor)
        processor_service_slots_by_token[token] = service_slot

