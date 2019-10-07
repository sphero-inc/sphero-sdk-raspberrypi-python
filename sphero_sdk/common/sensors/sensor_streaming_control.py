import logging
from .sensor_stream_attribute import SensorStreamAttribute
from .sensor_stream_service import SensorStreamService
from .sensor_stream_slot import SensorStreamSlot
from sphero_sdk.common.processors import Processors
from sphero_sdk.common.enums.sensor_enums import StreamingServiceStatesEnum
from sphero_sdk.common.enums.sensor_enums import StreamingDataSizesEnum

logger = logging.getLogger(__name__)


class SensorStreamingControl:
    # TODO: there are mixed styles of constants in sphero_sdk. we need to pick one and update
    SLOT_TOKEN_1 = 0x01
    SLOT_TOKEN_2 = 0x02
    SLOT_TOKEN_3 = 0x03
    SLOT_TOKEN_4 = 0x04
    VALID_SUCCESS_STATUS = 0x00
    MIN_STREAMING_INTERVAL = 33
    DEFAULT_STREAMING_INTERVAL = 250

    def __init__(self, rvr):
        self._rvr = rvr
        self._handlers = []
        self.__nordic_service_slots_by_token = {}
        self.__st_service_slots_by_token = {}
        self.__streaming_services_by_name = {}
        self.__enabled_sensors = []
        self.__nordic_service_state = StreamingServiceStatesEnum.Stop
        self.__st_service_state = StreamingServiceStatesEnum.Stop
        self.__streaming_interval = self.DEFAULT_STREAMING_INTERVAL

        self.__init_service_slots()
        self.__init_services()

        self.__clear_services()
        self.__add_service_handlers()

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

    @streaming_interval.setter
    def streaming_interval(self, interval_ms):
        """Sets the sensor streaming interval
        Args:
            interval_ms (uint16): Rate in milliseconds

        """
        if len(self.__enabled_sensors) > 0:
            self.__stop_services()

        if interval_ms < self.MIN_STREAMING_INTERVAL:
            logger.error("Streaming interval of {} is less than supported minimum!".format(interval_ms))
            return

        logger.info("Streaming interval set to {}".format(interval_ms))

        self.__streaming_interval = interval_ms

        self.__start_services()

    def add_sensor_data_handler(self, handler):
        """Adds a callback function to invoke when sensor streaming data is available.  Handler must define only
        one parameter to contain sensor data as a dictionary.

        Args:
            handler: Function to receive sensor stream callbacks

        Examples:
            $ def sensor_stream_handler(self, response):
                  imu_data = response["IMU"]
                  pitch = imu_data["Pitch"]
                  roll = imu_data["Roll"]
                  yaw = imu_data["Yaw"]

                  accel_data = response["Accelerometer"]
                  x = accel_data["X"]
                  y = accel_data["Y"]
                  z = accel_data["Z"]

        """
        if handler in self._handlers:
            logger.warning('{} already registered.'.format(handler))
            return

        self._handlers.append(handler)

    def enable(self, *sensor_names):
        """Starts the specified sensors streams by name at the configured streaming interval

        Args:
            *sensor_names (list(str)): List of sensors names

        Examples:
            To enable one sensor:
            $ enable("Quaternion")

            To enable multiple sensors:
            $ enable("Quaternion", "IMU", "Accelerometer")

        """
        if len(self.__enabled_sensors) > 0:
            self.__stop_services()
            self.__clear_services()

        logger.info("Enabling streaming services: {}".format(sensor_names))

        has_change = False
        for sensor_name in sensor_names:
            if sensor_name in self.__enabled_sensors:
                continue

            self.__enabled_sensors.append(sensor_name)
            has_change = True

        if not has_change:
            logger.info("No new sensors enabled.")
            return

        self.__configure_services(Processors.NORDIC_TARGET)
        self.__configure_services(Processors.ST_TARGET)

    def disable(self, *sensor_names):
        """Disables the specified sensors streams by name

        Args:
            *sensor_names (list(str)): List of sensors names

        Examples:
            To disable one sensor:
            $ disable("Quaternion")

            To disable multiple sensors:
            $ disable("Quaternion", "IMU", "Accelerometer")

        """
        if len(self.__enabled_sensors) > 0:
            self.__stop_services()
            self.__clear_services()

        logger.info("Disabling streaming services: {}".format(sensor_names))

        has_change = False
        for sensor_name in sensor_names:
            if sensor_name not in self.__enabled_sensors:
                continue

            self.__enabled_sensors.remove(sensor_name)
            has_change = True

        if not has_change:
            logger.info("No sensors disabled.")
            return

        self.__configure_services(Processors.NORDIC_TARGET)
        self.__configure_services(Processors.ST_TARGET)

    def disable_all(self):
        """Disables all sensor streams

        """
        if len(self.__enabled_sensors) == 0:
            logger.info('No enabled sensors to disable.')
            return

        logger.info("Disabling all streaming services.")

        self.__stop_services()
        self.__clear_services()
        self.__enabled_sensors.clear()
        self.__reset_services(Processors.NORDIC_TARGET)
        self.__reset_services(Processors.ST_TARGET)

    def _configure_streaming_service(self, token_id, configuration, processor):
        raise NotImplementedError("Missing implementation, subclasses should implement this!")

    def _add_streaming_service_data_notify_handler(self, processor):
        raise NotImplementedError("Missing implementation, subclasses should implement this!")

    def _start_streaming_service(self, interval, processor):
        raise NotImplementedError("Missing implementation, subclasses should implement this!")

    def _stop_streaming_service(self, processor):
        raise NotImplementedError("Missing implementation, subclasses should implement this!")

    def _clear_streaming_service(self, processor):
        raise NotImplementedError("Missing implementation, subclasses should implement this!")

    def _process_streaming_data(self, response, processor):
        response_token_uint8 = response['token']
        raw_sensor_data = response['sensorData']
        raw_start_index = 0
        status_flag = response_token_uint8 & 0xF0  # Check the upper nibble for flag value: 0x0 = OK, 0x1 = Invalid Data
        token_id = response_token_uint8 & 0x0F # Check the lower nibble for token id
        is_valid = status_flag == self.VALID_SUCCESS_STATUS

        logger.debug(
            'Processor: {}, Status: {}, Token: {}, Sensor Data: {}'.format(
                processor,
                status_flag,
                token_id,
                '[{}]'.format(', '.join('0x{:02x}'.format(x) for x in raw_sensor_data))
            )
        )

        processor_service_slots = self.__get_processor_service_slots(processor)
        service_slot = processor_service_slots[token_id]

        if service_slot is None:
            logger.error("Retrieved null streaming service slot for processor {}, token {}.".format(processor, token_id))
            return

        if len(service_slot.enabled_streaming_services_by_id) == 0:
            logger.error("Attempting to process streaming data before services in slot are enabled! Clearing services.")
            self.__clear_services()
            return

        streaming_services_by_id = service_slot.enabled_streaming_services_by_id
        service_ids = streaming_services_by_id.keys()
        parsed_service_data = {}
        for id in service_ids:
            streaming_service = streaming_services_by_id[id]

            if streaming_service is None:
                logger.error("Retrieved null streaming service for service id {}".format(id))

            # calculate how many bytes to copy from raw data array for the current service
            slice_length = len(streaming_service.attributes) * streaming_service.data_byte_count
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
            parsed_service_data[streaming_service.service_name] = sensor_data_dictionary

        if len(parsed_service_data) == 0:
            raise Exception("Parsed empty sensor data for processor {}, token {}".format(processor, token_id))

        return parsed_service_data

    def __add_service_handlers(self):
        self._add_streaming_service_data_notify_handler(Processors.NORDIC_TARGET)
        self._add_streaming_service_data_notify_handler(Processors.ST_TARGET)

    def __configure_services(self, processor):
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
            logger.info("No services enabled during configuration.")
            return

        self._start_streaming_service(self.__streaming_interval, processor)

    def __start_services(self):
        self._start_streaming_service(self.__streaming_interval, Processors.NORDIC_TARGET)
        self._start_streaming_service(self.__streaming_interval, Processors.ST_TARGET)

    def __stop_services(self):
        self._stop_streaming_service(Processors.NORDIC_TARGET)
        self._stop_streaming_service(Processors.ST_TARGET)

    def __clear_services(self):
        self._clear_streaming_service(Processors.NORDIC_TARGET)
        self._clear_streaming_service(Processors.ST_TARGET)

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
        -----------------------------------------------------------------------------------------
        | 0x0009 | Nordic (1), ST (2) | 3     | CoreTime           | TimeUpper, TimeLower       |
        -----------------------------------------------------------------------------------------
        """

        # Quaternion
        attributes = [
            SensorStreamAttribute("W", -1.0, 1.0),
            SensorStreamAttribute("X", -1.0, 1.0),
            SensorStreamAttribute("Y", -1.0, 1.0),
            SensorStreamAttribute("Z", -1.0, 1.0)
        ]
        streaming_service = SensorStreamService(
            0x0000,
            "Quaternion",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_1)

        # IMU
        attributes = [
            SensorStreamAttribute("Pitch", -180.0, 180.0),
            SensorStreamAttribute("Roll", -90.0, 90.0),
            SensorStreamAttribute("Yaw", -180.0, 180.0)
        ]
        streaming_service = SensorStreamService(
            0x0001,
            "IMU",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_1)

        # Accelerometer
        attributes = [
            SensorStreamAttribute("X", -16.0, 16.0),
            SensorStreamAttribute("Y", -16.0, 16.0),
            SensorStreamAttribute("Z", -16.0, 16.0)
        ]
        streaming_service = SensorStreamService(
            0x0002,
            "Accelerometer",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_1)

        # Color detection
        attributes = [
            SensorStreamAttribute("R", 0, 255),
            SensorStreamAttribute("G", 0, 255),
            SensorStreamAttribute("B", 0, 255),
            SensorStreamAttribute("Index", 0, 255),
            SensorStreamAttribute("Confidence", 0.0, 1.0)
        ]
        streaming_service = SensorStreamService(
            0x0003,
            "ColorDetection",
            StreamingDataSizesEnum.eight_bit,
            attributes,
            [Processors.NORDIC_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_1)

        # Gyroscope
        attributes = [
            SensorStreamAttribute("X", -2000.0, 2000.0),
            SensorStreamAttribute("Y", -2000.0, 2000.0),
            SensorStreamAttribute("Z", -2000.0, 2000.0)
        ]
        streaming_service = SensorStreamService(
            0x0004,
            "Gyroscope",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_1)

        # Locator
        attributes = [
            SensorStreamAttribute("X", StreamingDataSizesEnum.int_32_min, StreamingDataSizesEnum.int_32_max),
            SensorStreamAttribute("Y", StreamingDataSizesEnum.int_32_min, StreamingDataSizesEnum.int_32_max)
        ]
        streaming_service = SensorStreamService(
            0x0006,
            "Locator",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_2)

        # Velocity
        attributes = [
            SensorStreamAttribute("X", StreamingDataSizesEnum.int_32_min, StreamingDataSizesEnum.int_32_max),
            SensorStreamAttribute("Y", StreamingDataSizesEnum.int_32_min, StreamingDataSizesEnum.int_32_max)
        ]
        streaming_service = SensorStreamService(
            0x0007,
            "Velocity",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_2)

        # Speed
        attributes = [
            SensorStreamAttribute("Speed", 0.0, 2.0068307),
        ]
        streaming_service = SensorStreamService(
            0x0008,
            "Speed",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_2)

        # Core Time
        attributes = [
            SensorStreamAttribute("TimeUpper", 0, StreamingDataSizesEnum.int_64_max),
            SensorStreamAttribute("TimeLower", 0, StreamingDataSizesEnum.int_64_max)
        ]
        streaming_service = SensorStreamService(
            0x0009,
            "CoreTime",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.NORDIC_TARGET, Processors.ST_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_3)

        # Ambient Light
        attributes = [
            SensorStreamAttribute("Light", 0.0, 120000.0),
        ]
        streaming_service = SensorStreamService(
            0x000A,
            "AmbientLight",
            StreamingDataSizesEnum.thirty_two_bit,
            attributes,
            [Processors.NORDIC_TARGET]
        )
        self.__add_service_to_slot(streaming_service, self.SLOT_TOKEN_2)

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
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.SLOT_TOKEN_1, Processors.NORDIC_TARGET)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.SLOT_TOKEN_2, Processors.NORDIC_TARGET)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.SLOT_TOKEN_3, Processors.NORDIC_TARGET)
        self.__init_service_slot(self.__nordic_service_slots_by_token, self.SLOT_TOKEN_4, Processors.NORDIC_TARGET)

        self.__st_service_slots_by_token.clear()
        self.__init_service_slot(self.__st_service_slots_by_token, self.SLOT_TOKEN_1, Processors.ST_TARGET)
        self.__init_service_slot(self.__st_service_slots_by_token, self.SLOT_TOKEN_2, Processors.ST_TARGET)
        self.__init_service_slot(self.__st_service_slots_by_token, self.SLOT_TOKEN_3, Processors.ST_TARGET)
        self.__init_service_slot(self.__st_service_slots_by_token, self.SLOT_TOKEN_4, Processors.ST_TARGET)

    def __get_processor_service_slots(self, processor):
        return self.__nordic_service_slots_by_token \
            if processor == Processors.NORDIC_TARGET \
            else self.__st_service_slots_by_token

    def __init_service_slot(self, processor_service_slots_by_token, token, processor):
        service_slot = SensorStreamSlot(token, processor)
        processor_service_slots_by_token[token] = service_slot

