#! /usr/bin/env python3

import logging
from threading import Thread
from queue import Queue
from serial import Serial

logger = logging.getLogger(__name__)


class SerialObserverPort:
    def __init__(self, parser, port_id, baud):
        """SerialObserverPort is responsible opening, writing, and reading bytes coming from the UART port.

        Args:
            parser (ObserverParser): Used to parse bytes read from the port.
            port_id (str): id for the serial port.
            baud (int): Baud rate.
        """
        self.__parser = parser
        self.__ser = Serial(port_id, baud)
        self.__running = True
        self.__write_queue = Queue()
        self.__serial_thread = Thread(name='serial_thread', target=self.__serial_rw)
        self.__serial_thread.start()

    def close(self):
        """Closes the port and joins the thread managing reading and writing.

        """
        logger.info('Read/Write thread joining.')
        self.__running = False
        self.__serial_thread.join()
        logger.info('Closing serial port.')
        self.__ser.close()

    def send(self, message):
        """Enqueues a Message instance which will be serialized and written to the port at a later time.

        Args:
            message (Message): Instance of a Message object

        """
        self.__write_queue.put(message.serialise())

    def __serial_rw(self):
        while self.__running:
            self.__write_bytes()
            self.__read_bytes()

    def __read_bytes(self):
        bytes_in_waiting = self.__ser.in_waiting
        if bytes_in_waiting > 0:
            data = self.__ser.read(bytes_in_waiting)
            logger.debug('Read {} bytes: [{}]'.format(bytes_in_waiting, ', '.join('0x{:02x}'.format(x) for x in data)))
            self.__parser.feed(data)

    def __write_bytes(self):
        if not self.__write_queue.empty():
            data = self.__write_queue.get()
            logger.debug('Writing bytes: [{}]'.format(', '.join('0x{:02x}'.format(x) for x in data)))
            self.__ser.write(data)
