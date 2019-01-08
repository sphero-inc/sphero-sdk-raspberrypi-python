#!/usr/bin/env python3

from . import system_info
import requests


class SpheroRvr:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.session = requests.Session()

    def get_main_app(self):
        return system_info.get_main_app(self)
