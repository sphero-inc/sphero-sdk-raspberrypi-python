import logging
from sphero_sdk.common.processors import Processors
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
            if processor == Processors.NORDIC_TARGET \
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

    def _clear_streaming_service(self, processor):
        self._rvr.clear_streaming_service(
            target=processor
        )

    def __nordic_streaming_data_handler(self, response):
        self.__dispatch_user_callback(response, Processors.NORDIC_TARGET)

    def __st_streaming_data_handler(self, response):
        self.__dispatch_user_callback(response, Processors.ST_TARGET)

    def __dispatch_user_callback(self, response, processor):
        streaming_data = self._process_streaming_data(processor, response)
        for handler in self._handlers:
            handler(streaming_data)
