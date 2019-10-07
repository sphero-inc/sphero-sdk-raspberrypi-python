import asyncio
import logging
from sphero_sdk.common.processors import Processors
from sphero_sdk.common.sensors.sensor_streaming_control import SensorStreamingControl

logger = logging.getLogger(__name__)


class SensorControlAsync(SensorStreamingControl):

    def __init__(self, rvr):
        SensorStreamingControl.__init__(self, rvr)

    async def add_sensor_data_handler(self, handler):
        SensorStreamingControl.add_sensor_data_handler(self, handler)

    async def enable(self, *sensor_names):
        SensorStreamingControl.enable(self, *sensor_names)

    async def disable(self, *sensor_names):
        SensorStreamingControl.disable(self, *sensor_names)

    async def disable_all(self):
        SensorStreamingControl.disable_all(self)

    def _configure_streaming_service(self, token_id, configuration, processor):
        logger.info(
            'Configuring streaming service with data (token:{}, configuration:{}, target:{})'
            .format(token_id, configuration, processor)
        )

        asyncio.ensure_future(
            self._rvr.configure_streaming_service(
                token=token_id,
                configuration=configuration,
                target=processor
            )
        )

    def _add_streaming_service_data_notify_handler(self, processor):
        handler = self.__nordic_streaming_data_handler\
            if processor == Processors.NORDIC_TARGET\
            else self.__st_streaming_data_handler

        asyncio.ensure_future(
            self._rvr.on_streaming_service_data_notify(
                handler=handler,
                target=processor
            )
        )

    def _start_streaming_service(self, interval, processor):
        logger.info('Starting streaming service for at {}ms for processor {}'.format(interval, processor))
        asyncio.ensure_future(
            self._rvr.start_streaming_service(
                period=interval,
                target=processor
            )
        )

    def _stop_streaming_service(self, processor):
        logger.info('Stopping streaming service for processor {}'.format(processor))
        asyncio.ensure_future(
            self._rvr.stop_streaming_service(
                target=processor
            )
        )

    def _clear_streaming_service(self, processor):
        asyncio.ensure_future(
            self._rvr.clear_streaming_service(
                target=processor
            )
        )

    async def __nordic_streaming_data_handler(self, response):
        await self.__dispatch_user_callback(Processors.NORDIC_TARGET, response)

    async def __st_streaming_data_handler(self, response):
        await self.__dispatch_user_callback(Processors.ST_TARGET, response)

    async def __dispatch_user_callback(self, processor, response):
        streaming_data = SensorStreamingControl._process_streaming_data(self, processor, response)
        if streaming_data is None:
            logger.error('Streaming response dictionary processed from streaming data is null!')
            return

        for handler in self._handlers:
            await handler(streaming_data)
