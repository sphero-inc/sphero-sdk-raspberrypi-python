import logging
from sphero_sdk import SpheroRvrTargets
from sphero_sdk.common.sensors.sensor_streaming_control import SensorStreamingControl

logger = logging.getLogger(__name__)


class SensorControlObserver(SensorStreamingControl):
    def __init__(self, rvr):
        SensorStreamingControl.__init__(self, rvr)

    def _configure_streaming_service(self, token_id, configuration, processor):
        self._rvr.configure_streaming_service(
            token=token_id,
            configuration=configuration,
            target=processor
        )

    def _add_streaming_service_data_notify_handler(self, processor):
        handler = self.__nordic_streaming_data_handler \
            if processor == SpheroRvrTargets.primary.value \
            else self.__st_streaming_data_handler

        self._rvr.on_streaming_service_data_notify(
            handler=handler,
            target=processor
        )

    def _start_streaming_service(self, interval, processor):
        self._rvr.start_streaming_service(
            period=interval,
            target=processor
        )

    def _stop_streaming_service(self, processor):
        self._rvr.stop_streaming_service(
            target=processor
        )

    def _stop_and_clear_streaming_service(self, processor):
        self._rvr.clear_streaming_service(
            target=processor
        )

    def __nordic_streaming_data_handler(self, response):
        self.__dispatch_user_callback(SpheroRvrTargets.primary.value, response)

    def __st_streaming_data_handler(self, response):
        self.__dispatch_user_callback(SpheroRvrTargets.secondary.value, response)

    def __dispatch_user_callback(self, processor, response):
        response_dictionary = SensorStreamingControl._process_streaming_response(self, processor, response)
        if response_dictionary is None:
            logger.error('Streaming response dictionary processed from streaming data is null!')
            return

        sensors_in_response = response_dictionary.keys()
        for sensor_name in self.enabled_sensors:
            if sensor_name in sensors_in_response:
                handler = self._sensor_handlers[sensor_name]
                handler(response_dictionary)
