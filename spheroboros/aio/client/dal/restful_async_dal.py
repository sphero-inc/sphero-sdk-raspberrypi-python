#! /usr/bin/env python3

import aiohttp
from aiohttp import ClientSession
from spheroboros.aio.common.dal.async_dal_base import AsyncDalBase
from spheroboros import __version__
from spheroboros.common.sphero_api_url import SpheroApiUrl
from spheroboros.common import exceptions
from spheroboros.common.devices import get_device_path_by_did,\
                                       get_command_path_by_cid


class RestfulAsyncDal(AsyncDalBase):
    def __init__(self, prefix, domain='localhost', port=8080, ssl=None):
        AsyncDalBase.__init__(self)
        self._session = ClientSession(raise_for_status=True)
        self._prefix = prefix
        self._scheme = 'http' if ssl is None else 'https'
        self._domain = domain
        self._port = port
        self._ssl = ssl

    async def send_command(self, did, cid, target,
                           timeout=None, inputs=[], outputs=[]):
        try:
            url = SpheroApiUrl(
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

            print('URL: {}'.format(str(url)))
            response = await self._session.request(
                method='GET' if len(outputs) > 0 and len(inputs) == 0 else 'PUT',
                url=str(url),
                timeout=timeout,
                ssl=self._ssl,
                json=json if json is not {} else None
            )

        except aiohttp.ClientResponseError:
            raise exceptions.BadResponse
        except Exception:
            raise exceptions.BadConnection

        try:
            response_json = await response.json()
        except Exception:
            return

        try:
            response_list = [None]*len(outputs)
            for param in outputs:
                response_list[param.index] = response_json[param.name]
        except Exception:
            raise

        if len(response_list) > 1:
            return tuple(response_list)

        if len(response_list) == 1:
            return response_list[0]

        return None

    async def on_command(self, did, cid, target, handler=None,
                         timeout=None, outputs=[]):
        try:
            await self._web_sockets[get_command_path_by_cid(did, cid)].close()
            self._web_sockets.pop(get_command_path_by_cid(did, cid))
        except KeyError:
            pass

        if handler is None:
            return

        try:
            url = SpheroApiUrl(
                self._scheme,
                self._domain,
                self._port,
                __version__,
                self._prefix,
                target,
                get_device_path_by_did(did),
                get_command_path_by_cid(did, cid)
            )

            socket = await self._session.ws_connect(
                url=str(url),
                timeout=timeout,
                ssl=self._ssl,
            )

            self._web_sockets[get_command_path_by_cid(did, cid)] = socket

        except aiohttp.ClientResponseError:
            raise exceptions.BadResponse
        except Exception:
            raise exceptions.BadConnection

        while not socket.closed:
            try:
                json = await socket.receive_json()
                await handler(**json)  # TODO MJC Investigate ws.close() effect
            except TypeError:
                socket.close()
            except ValueError:
                socket.close()
