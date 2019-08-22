#! /usr/bin/env python333

class SpheroToyBase:
    def __init__(self, port, node_id):
        self._port = port
        self._node_id = node_id

    @property
    def port(self):
        return self._port

    @property
    def node_id(self):
        return self._node_id
