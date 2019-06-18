from threading import Thread
from queue import Queue
from serial import Serial


class RvrSerialPort:
    def __init__(self, parser, port='/dev/ttyS0', baud=115200):
        self._parser = parser
        self._ser = Serial(port, baud)
        self._running = True
        self._write_queue = Queue()
        self._serial_thread = Thread(name="serial_thread", target=self._serial_rw)
        self._serial_thread.start()

    def close(self):
        self._running = False
        self._serial_thread.join()
        self._ser.close()

    def send(self, message):
        self._write_queue.put(message.serialise())

    def _serial_rw(self):
        while self._running:
            self._write_bytes()
            self._read_bytes()

    def _read_bytes(self):
        bytes_in_waiting = self._ser.in_waiting
        if bytes_in_waiting > 0:
            data = self._ser.read(bytes_in_waiting)
            self._parser.feed(data)

    def _write_bytes(self):
        if not self._write_queue.empty():
            self._ser.write(self._write_queue.get())






