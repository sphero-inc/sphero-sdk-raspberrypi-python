#! /usr/bin/env python3

import json
import requests
import websocket
from requests import Session
from spheroboros.blocking.common.dal.blocking_dal_base import BlockingDalBase
from spheroboros import __version__
from spheroboros.common.sphero_api_url import SpheroApiUrl
from spheroboros.common import exceptions
from spheroboros.common.devices import get_device_path_by_did,\
                                       get_command_path_by_cid


class RestfulBlockingDal(BlockingDalBase, Session):
    def __init__(self, prefix, domain='localhost', port=8080, ssl=None):
        BlockingDalBase.__init__(self)
        Session.__init__(self)
        self._prefix = prefix
        self._scheme = 'http' if ssl is None else 'https'
        self._domain = domain
        self._port = port
        self._ssl = ssl

    def send_command(self, did, cid, target,
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

            input_dict = {}
            for param in inputs:
                input_dict[param.name] = param.value

            # TODO MJC Investigate SSL
            response = self.request(
                method='GET' if len(outputs) > 0 and len(inputs) == 0 else 'PUT',
                url=str(url),
                timeout=timeout,
                json=input_dict if input_dict is not {} else None
            )

            response.raise_for_status()

        except requests.HTTPError:
            raise exceptions.BadResponse
        except Exception:
            raise exceptions.BadConnection

        try:
            response_json = response.json()
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

    def on_command(self, did, cid, target, handler=None,
                   timeout=None, outputs=[]):
        # TODO MJC Figure out what to do with handler=None
        try:
            url = SpheroApiUrl(
                'ws' if self._scheme is 'http' else 'wss',
                self._domain,
                self._port,
                __version__,
                self._prefix,
                target,
                get_device_path_by_did(did),
                get_command_path_by_cid(did, cid)
            )

            # TODO MJC investigate SSL
            socket = websocket.WebSocket()
            socket.connect(str(url))

        except Exception:
            return

        while True:
            try:
                response_string = socket.recv()
                response_json = json.loads(response_string)
                handler(**response_json)
            except json.JSONDecodeError:
                socket.close()
                break
            except Exception:
                socket.close()
                break
