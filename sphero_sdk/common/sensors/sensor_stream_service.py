import logging
from sphero_sdk.common.protocol.api_sphero_protocol import Unpack
from sphero_sdk.common.helpers import normalize
from sphero_sdk.common.enums.sensor_enums import StreamingDataSizesEnum
from sphero_sdk.common.enums.number_bounds_enums import UintBounds

logger = logging.getLogger(__name__)


class SensorStreamService:

    __slots__ = ['__id', '__name', '__data_size', '__byte_count', '__attributes', '__processors']

    def __init__(self, id, name, data_size, attributes, processors):
        self.__id = id
        self.__name = name
        self.__data_size = data_size
        self.__byte_count = pow(2, data_size.value)
        self.__attributes = attributes
        self.__processors = processors

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def data_size(self):
        return self.__data_size

    @property
    def byte_count(self):
        return self.__byte_count

    @property
    def attributes(self):
        return self.__attributes.copy()

    @property
    def processors(self):
        return self.__processors.copy()

    def parse_attribute_bytes_to_floats(self, sensor_data_bytes):
        sensor_data_index = 0
        attribute_values = {}

        for attribute in self.attributes:
            attribute_bytes = []

            for i in range(self.byte_count):
                attribute_bytes.append(sensor_data_bytes[sensor_data_index])
                sensor_data_index += 1

            integer_value, maximum_value = self.__get_values_from_bytes(bytes(attribute_bytes))
            normalized_value = normalize(integer_value, 0, maximum_value, attribute.minimum_value, attribute.maximum_value)
            # Cast attribute value to the intended type
            attribute_values[attribute.name] = attribute.number_type(normalized_value)
            logger.debug(
                'Sensor: {} Attribute: {} Bytes: [{}], Int Value: {}, Normalized Value: {}'.format(
                    self.name,
                    attribute.name,
                    ', '.join('0x{:02x}'.format(x) for x in attribute_bytes),
                    integer_value,
                    normalized_value
                )
            )

        return attribute_values

    def __get_values_from_bytes(self, bytes_buffer):
        if self.data_size == StreamingDataSizesEnum.eight_bit:
            return Unpack.uint8(bytes_buffer), UintBounds.uint_8_max
        elif self.data_size == StreamingDataSizesEnum.sixteen_bit:
            return Unpack.uint16(bytes_buffer), UintBounds.uint_16_max
        elif self.data_size == StreamingDataSizesEnum.thirty_two_bit:
            return Unpack.uint32(bytes_buffer), UintBounds.uint_32_max
        else:
            raise ValueError('Unsupported data size.  Make sure you assign a supported data size value!')
