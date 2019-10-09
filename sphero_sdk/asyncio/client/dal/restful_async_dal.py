#! /usr/bin/env python3

import aiohttp
import logging
from aiohttp import ClientSession
from sphero_sdk import __version__
from sphero_sdk.common.client.dal.sphero_dal_base import SpheroDalBase
from sphero_sdk.common.protocol.sphero_command_url import SpheroCommandUrl
from sphero_sdk.common.protocol.sphero_async_url import SpheroAsyncUrl
from sphero_sdk.common.devices import get_device_path_by_did, get_command_path_by_cid

logger = logging.getLogger(__name__)


class RestfulAsyncDal(SpheroDalBase):
    def __init__(self, prefix='RV', domain='localhost', port=8080, ssl=None):
        SpheroDalBase.__init__(self)
        self._session = ClientSession(raise_for_status=True)
        self._prefix = prefix
        self._scheme = 'http' if ssl is None else 'https'
        self._domain = domain
        self._port = port
        self._ssl = ssl
        self._web_socket = None
        self._web_socket_created = False
        self._async_callback_data = {}

    async def close(self):
        if self._web_socket_created:
            self._web_socket_created = False
            await self._web_socket.close()

    async def send_command(self, did, cid, seq, target, timeout=None, inputs=[], outputs=[]):
        url, json = self.__get_command_url_and_json(did, cid, target, inputs)
        try:
            logger.debug('Send Command URL: {} JSON:{}'.format(str(url), json))

            response = await self._session.request(
                        method='GET' if len(outputs) > 0 and len(inputs) == 0 else 'PUT',
                        url=str(url),
                        timeout=timeout,
                        ssl=self._ssl,
                        json=json if json is not {} else None
                    )

        except aiohttp.ClientResponseError:
            raise

        except Exception:
            raise

        if len(outputs) == 0:
            logger.info('Command has no expected outputs.')
            return

        try:
            response_json = await response.json()
            response_dictionary = self.__parse_command_json(outputs, response_json)
            return response_dictionary

        except Exception:
            raise

    async def on_command(self, did, cid, target, handler, timeout=None, outputs=[]):
        if handler is None:
            raise Exception('Cannot open async web socket with a null handler!')

        self._async_callback_data[(did, cid, target)] = {'outputs': outputs, 'handler': handler}

        # TODO - Would like a more elegant way of preventing double instantiation, but this works for now.
        if self._web_socket_created:
            logger.warning('Async web socket already exists!  Early exit.')
            return

        try:
            self._web_socket_created = True
            self._web_socket = await self._session.ws_connect(
                url=str(self.__get_async_url()),
                timeout=timeout,
                ssl=self._ssl
            )

        except aiohttp.ClientResponseError:
            raise

        except Exception:
            raise

        while not self._web_socket.closed:
            try:
                response_json = await self._web_socket.receive_json()
                handler, response_dictionary = self.__process_async_json(response_json)
                await handler(response_dictionary)

            except TypeError:
                await self._web_socket.close()
                raise

            except ValueError:
                await self._web_socket.close()
                raise

    def __get_command_url_and_json(self, did, cid, target, inputs):
        url = SpheroCommandUrl(
            self._scheme,
            self._domain,
            self._port,
            __version__,
            self._prefix,
            get_device_path_by_did(did),
            get_command_path_by_cid(did, cid),
            target
        )

        json = {}
        for param in inputs:
            json[param.name] = param.value

        return url, json

    def __get_async_url(self):
        return SpheroAsyncUrl(
            self._scheme,
            self._domain,
            self._port
        )

    def __parse_command_json(self, outputs, response_json):
        logger.info('Received Command JSON from web socket: {}'.format(response_json))

        response_dictionary = {}
        for param in outputs:
            response_dictionary[param.name] = response_json[param.name]

        return response_dictionary

    def __process_async_json(self, response_json):
        logger.info('Received Async JSON from web socket: {}'.format(response_json))

        did = response_json['_deviceId']
        cid = response_json['_commandId']
        source = response_json['_sourceId']
        data = response_json['_data']

        callback_dictionary = self._async_callback_data[(did, cid, source)]
        outputs = callback_dictionary['outputs']
        handler = callback_dictionary['handler']

        response_dictionary = {}
        for param in outputs:
            response_dictionary[param.name] = data[param.name]

        return handler, response_dictionary
