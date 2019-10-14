import logging
from sphero_sdk.common.protocol.api_sphero_protocol import Pack

logger = logging.getLogger(__name__)


class SensorStreamSlot:
    def __init__(self, token, processor):
        self.__token = token
        self.__processor = processor
        self.__supported_streaming_services_by_name = {}
        self.__enabled_streaming_services_by_id = {}

    @property
    def token(self):
        return self.__token

    @property
    def processor(self):
        return self.__processor

    @property
    def supported_streaming_services_by_name(self):
        return self.__supported_streaming_services_by_name.copy()

    @property
    def enabled_streaming_services_by_id(self):
        return self.__enabled_streaming_services_by_id.copy()

    @property
    def has_enabled_streaming_services(self):
        return len(self.__enabled_streaming_services_by_id) > 0

    @property
    def streaming_services_configuration(self):
        if len(self.__enabled_streaming_services_by_id) == 0:
            return [0]

        data_array = []
        for streaming_service in self.__enabled_streaming_services_by_id.values():
            id_bytes = Pack.uint16(streaming_service.id)
            data_array.append(id_bytes[0])
            data_array.append(id_bytes[1])
            data_array.append(streaming_service.data_size.value)

        return data_array

    def add_streaming_service(self, streaming_service):
        if streaming_service in self.__supported_streaming_services_by_name.values():
            logger.error('Streaming service {} already added!'.format(streaming_service.name))
            return

        if len(self.__supported_streaming_services_by_name) > 5:
            logger.error('Streaming service count limit reached, cannot add {}'.format(streaming_service.name))
            return

        self.__supported_streaming_services_by_name[streaming_service.name] = streaming_service

    def remove_streaming_service(self, streaming_service):
        if streaming_service not in self.__supported_streaming_services_by_name.values():
            logger.error('Streaming service {} not present in this slot'.format(streaming_service.name))
            return

        self.__supported_streaming_services_by_name.pop(streaming_service.name)

    def enable_streaming_service(self, service_name):
        streaming_service = self.__supported_streaming_services_by_name.get(service_name)

        if streaming_service is None:
            raise Exception('Cannot enable Streaming service {} because it was not found in this slot!'.format(service_name))

        self.__enabled_streaming_services_by_id[streaming_service.id] = streaming_service

    def disable_streaming_service(self, service_name):
        streaming_service = self.__supported_streaming_services_by_name.get(service_name)

        if streaming_service is None:
            raise Exception('Cannot disable streaming service {} because it was not found in this slot!'.format(service_name))

        self.__enabled_streaming_services_by_id.pop(streaming_service.id)

    def disable_all_streaming_services(self):
        if len(self.__enabled_streaming_services_by_id) == 0:
            logger.error(
                'Attempted to disable all services for Slot (token:{}, processor:{}), but none are enabled.'
                .format(self.token, self.processor)
            )
            return

        self.__enabled_streaming_services_by_id.clear()
