#!/usr/bin/env python3


class SpheroUrlBase:
    def __init__(self, scheme, domain, port, *paths):
        '''A Base URL takes form:
            scheme://domain:port/path

            Example:
                http://localhost:8080/api/v0.6.2/rvr/system_info/get_main_application_version/1
        '''
        self.__scheme = scheme
        self.__domain = domain
        self.__port = port
        self.__paths = paths

    def __str__(self):
        url_string = '://'.join((
            self.__scheme,
            '/'.join((
                ':'.join((
                    self.__domain,
                    str(self.__port)
                )),
                '/'.join(path for path in self.__paths)
            ))
        ))
        return url_string
