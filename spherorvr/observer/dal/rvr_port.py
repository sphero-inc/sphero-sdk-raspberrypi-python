import asyncio
from serial import Serial


class RvrSerialPort:
    def __init__(self, parser, port='/dev/ttyS0', baud=115200):
        self._parser = parser
        self._loop = asyncio.get_event_loop()
        self._ser = Serial(port, baud)
        self._loop.run_in_executor(None, self._read_bytes)

    def close(self):
        pass

    def _read_bytes(self):
        while True:
            bytes_in_waiting = self._ser.in_waiting
            if bytes_in_waiting > 0:
                data = self._ser.read(bytes_in_waiting)
                self._parser.feed(data)

    def send(self, message):
        msg = message.serialise()
        self._ser.write(msg)

