#!/usr/bin/env python3

import requests
from ..common import exceptions

path = '/system_info/'


def get_main_app(self):
    try:
        response = self.session.get(
            ''.join((
                'http://',
                self.host,
                ':',
                str(self.port),
                path,
                'get_main_app'
            )),
            timeout=1.0
        )

        response.raise_for_status()
    except requests.ConnectionError:
        raise exceptions.BadConnection
    except requests.HTTPError:
        raise exceptions.BadResponse(
            'Request returned: {}'.format(
                response.status_code
            )
        )
    except requests.Timeout:
        raise exceptions.BadConnection

    try:
        response_json = response.json()
    except ValueError:
        raise exceptions.BadResponse

    try:
        return (response_json['major'],
                response_json['minor'],
                response_json['build'])
    except KeyError:
        raise exceptions.BadResponse
