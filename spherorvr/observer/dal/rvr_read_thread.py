from threading import Thread
from threading import Lock
import time

class RvrReadThread(Thread):
    def __init__(self, name, port):
        Thread.__init__(name=name)
        self._port = port

    def run(self):

        print("running", self.name)
        time.sleep(2)


