#!/usr/bin/env python3

from ..api_sphero_handler import Handler


class Port:
    def __init__(self):
        pass

    def send(self, msg):
        pass


def command_handler(msg):
    pass


def test_add_worker():
    port = Port()
    handler = Handler(port)
    handler.add_command_worker(17, 0, 0x1, command_handler)
    assert (17, 0, 0x1) in handler.command_workers
    assert handler.command_workers[(17, 0, 0x1)] == command_handler
