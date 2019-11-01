from serial import Serial
from .constants import SBUSConsts


class SerialParser:
    def __init__(self, tty, baud):
        self._ser = None
        self._tty = tty
        self._baud = baud
        self._parse_state = 0
        self._prev_byte = b'\x00'
        self._cur_byte = b'\x00'

    def begin(self):
        # initialize parse state
        self._parse_state = 0

        # begin serial port for SBUS
        self._ser = Serial(self._tty)
        self._ser.baudrate = self._baud

    def close(self):
        self._ser.flush()
        self._ser.close()

    def parse_raw(self):
        return self._ser.read(1)

    def parse(self, payload):
        header = SBUSConsts.SBUS_HEADER[0]
        footer = SBUSConsts.SBUS_FOOTER[0]
        self._cur_byte = b'\x00'
        self._prev_byte = b'\x00'

        # see if serial data is available
        while self._ser.readable():
            self._cur_byte = self._ser.read(1)
            #print(self._cur_byte)

            if len(self._cur_byte) == 0:
                break

            cur_byte = self._cur_byte[0]
            prev_byte = self._prev_byte[0]

            # find the header
            if self._parse_state == 0:
                #print("_parser_state = 0")
                if cur_byte == header and prev_byte == footer:
                    #print("header")
                    payload[self._parse_state] = cur_byte
                    self._parse_state += 1
                else:
                    self._parse_state = 0
            else:
                # strip off the data
                if self._parse_state < SBUSConsts.PAYLOAD_SIZE:
                    payload[self._parse_state] = cur_byte
                    self._parse_state += 1

                # check the end byte
                if self._parse_state == SBUSConsts.PAYLOAD_SIZE:
                    #print("_parser_state = 25")
                    if cur_byte == footer:
                        #print("footer")
                        self._parse_state = 0
                        return True
                    else:
                        #print("no footer")
                        self._parse_state = 0
                        return False

            self._prev_byte = self._cur_byte

        # return false if partial packet
        return False



