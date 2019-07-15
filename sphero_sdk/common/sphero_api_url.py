#!/usr/bin/env python3

from spheroboros.common.sphero_url_base import SpheroUrlBase


class SpheroApiUrl(SpheroUrlBase):
    def __init__(self, scheme, domain, port,
                 version, toy, device_name, command_name, target):
        '''A SpheroApiUrl takes the form:
            scheme://domain:port/api/version/toy/device_name/command_name/target

        '''
        SpheroUrlBase.__init__(
            self,
            scheme,
            domain,
            port,
            ('api', 'v1.0', device_name, command_name, str(target))
        )
