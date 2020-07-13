#! /usr/bin/env python3


class SpheroDalBase:
    def __init__(self):
        self.request_error_responses_only = False

    def close(self):
        raise NotImplementedError

    def send_command(self, did, cid, seq, target, timeout=None, inputs=[], outputs=[]):
        raise NotImplementedError

    def on_command(self, did, cid, target, handler, timeout=None, outputs=[]):
        raise NotImplementedError
