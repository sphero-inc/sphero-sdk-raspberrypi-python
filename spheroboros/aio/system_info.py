#! /usr/bin/env python3

import aiohttp
from ..common import exceptions
import time

path = '/system_info/'


async def get_main_app(self):
    try:
        url = ''.join((
            'http://',
            self.host,
            ':',
            str(self.port),
            path,
            'get_main_app'
        ))
        print('Sending to {}'.format(url))

        starttime = int(round(time.time() * 1000))
        print("Sent At: {}".format(starttime))
        resp = await self.session.get(
            url,
            timeout=3.0
        )
        endtime = int(round(time.time() * 1000))
        print("Received At: {}".format(endtime))
        print("Time Elapse: {}".format(endtime - starttime))

        resp.raise_for_status()

    except aiohttp.ClientResponseError:
        raise exceptions.BadResponse('Received Response: {}'.format(resp.status))
    except aiohttp.ServerTimeoutError:
        raise exceptions.BadConnection
    except:
        raise 

    try:
        resp_json = await resp.json()
    except aiohttp.ClientResponseError:
        raise exceptions.BadResponse

    return (resp_json['major'],
            resp_json['minor'],
            resp_json['build'])
