import logging
from threading import Thread
from queue import Queue
from serial import Serial

logger = logging.getLogger(__name__)


class RvrSerialPort:
    def __init__(self, parser, port='/dev/ttyS0', baud=115200):
        self.__parser = parser
        self.__ser = Serial(port, baud)
        self.__running = True
        self.__write_queue = Queue()
        self.__serial_thread = Thread(name="serial_thread", target=self.__serial_rw)
        self.__serial_thread.start()

    def close(self):
        logger.info("read/write thread joining.")
        self.__running = False
        self.__serial_thread.join()
        logger.info("closing serial port.")
        self.__ser.close()

    def send(self, message):
        self.__write_queue.put(message.serialise())

    def __serial_rw(self):
        while self.__running:
            self.__write_bytes()
            self.__read_bytes()

    def __read_bytes(self):
        bytes_in_waiting = self.__ser.in_waiting
        if bytes_in_waiting > 0:
            data = self.__ser.read(bytes_in_waiting)
            logger.debug('read %s bytes: %s', bytes_in_waiting, data)
            self.__parser.feed(data)

    def __write_bytes(self):
        if not self.__write_queue.empty():
            data = self.__write_queue.get()
            logger.debug('writing bytes: %s', data)
            self.__ser.write(data)
