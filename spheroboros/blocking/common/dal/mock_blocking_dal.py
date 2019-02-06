#! /usr/bin/env python3

import time
from spheroboros.blocking.common.dal.blocking_dal_base import BlockingDalBase
from threading import Timer
from queue import Queue


class MockBlockingDal(BlockingDalBase):
    def __init__(self):
        BlockingDalBase.__init__(self)

    def send_command(self, did, cid, target,
                     timeout=None, inputs=None, outputs=None):
        response_list = [None]*len(outputs)
        for param in outputs:
            if param.size == 1:
                response_list[param.index] = self.random_value(param.data_type)
            else:
                response_list[param.index] = self.random_list(
                        param.data_type, param.size
                )

        return tuple(response_list) if response_list is not {} else None

    def on_command(self, did, cid, target, handler,
                   timeout=None, outputs=None):

        q = Queue()

        def handler():
            q.put(True)

        t = Timer(timeout, handler)

        while True:
            json = {}
            for param in outputs:
                if len(param.size) == 1:
                    json[param.name] = self.random_value(param.data_type)
                else:
                    json[param.name] = self.random_list(
                        param.data_type,
                        param.size
                    )
            handler(**json)
            time.sleep(timeout/10)
            try:
                response = q.get(block=False)
                if response is True:
                    break
            except Exception:
                pass

        t.cancel()
