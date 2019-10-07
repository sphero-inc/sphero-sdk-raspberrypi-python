#!/usr/bin/env python3

from sphero_sdk.common.protocol.sphero_url_base import SpheroUrlBase


class SpheroAsyncUrl(SpheroUrlBase):
    def __init__(self, scheme, domain, port):
        """A SpheroAsyncUrl takes the form:
            scheme://domain:port/stream

        """
        SpheroUrlBase.__init__(
            self,
            scheme,
            domain,
            port,
            'stream'
        )
