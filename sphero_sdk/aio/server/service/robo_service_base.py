#!/usr/bin/env python3


class RoboServiceBase:
    def __init__(self):
        return

    def register_as_node(self):
        raise NotImplementedError

    def unregister_node(self, node_id):
        raise NotImplementedError

    def register_port(self):
        raise NotImplementedError

    def unregister_port(self):
        raise NotImplementedError
