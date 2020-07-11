#!/usr/bin/env python3

import logging
from .sphero_message_base import SpheroMessageBase
from .api_sphero_header import Header
from .api_sphero_protocol import Pack, Unpack


logger = logging.getLogger(__name__)


class Message(SpheroMessageBase):
    __slots__ = ['_header', '_body']
    START_OF_PACKET = bytearray.fromhex('8d')
    END_OF_PACKET = bytearray.fromhex('d8')
    ESCAPE = bytearray.fromhex('ab')
    ESCAPED_START = bytearray.fromhex('05')
    ESCAPED_END = bytearray.fromhex('50')
    ESCAPED_ESCAPE = bytearray.fromhex('23')

    def __init__(self, header=None, body=None):
        SpheroMessageBase.__init__(self)
        self._header = header if header is not None else Header()
        self._body = body if body is not None else bytearray()

    def __repr__(self):
        return '{} DID: {} CID: {} Sequence: {} Payload: {} Error: {}'.format(
            self._header.packet_type_string,
            '0x{:02x}'.format(self._header.did),
            '0x{:02x}'.format(self._header.cid),
            '0x{:02x}'.format(self._header.seq),
            ','.join('0x{:02x}'.format(x) for x in self._body),
            '0x{:02x}'.format(self._header.err) if self._header.err is not None else None)

    @property
    def is_response(self):
        return self._header.is_response

    @is_response.setter
    def is_response(self, answer):
        self._header.is_response = answer

    @property
    def requests_response(self):
        return self._header.requests_response

    @requests_response.setter
    def requests_response(self, answer):
        self._header.requests_response = answer

    @property
    def requests_error_response(self):
        return self._header.requests_error_response

    @requests_error_response.setter
    def requests_error_response(self, answer):
        self._header.requests_error_response = answer

    @property
    def is_activity(self):
        return self._header.is_activity

    @is_activity.setter
    def is_activity(self, answer):
        self._header.is_activity = answer

    @property
    def has_target(self):
        return self._header.has_target

    @has_target.setter
    def has_target(self, answer):
        self._header.has_target = answer

    @property
    def has_source(self):
        return self._header.has_source

    @has_source.setter
    def has_source(self, answer):
        self._header.has_source = answer

    @property
    def has_extended_flags(self):
        return self._header.has_extended_flags

    @has_extended_flags.setter
    def has_extended_flags(self, answer):
        self._header.has_extended_flags = answer

    @property
    def did(self):
        return self._header.did

    @did.setter
    def did(self, device):
        self._header.did = device

    @property
    def cid(self):
        return self._header.cid

    @cid.setter
    def cid(self, command):
        self._header.cid = command

    @property
    def seq(self):
        return self._header.seq

    @seq.setter
    def seq(self, sequence):
        self._header.seq = sequence

    @property
    def target(self):
        return self._header.target

    @target.setter
    def target(self, address):
        self._header.target = address

    @property
    def target_port(self):
        return self._header.target_port

    @target_port.setter
    def target_port(self, port):
        self._header.target_port = port

    @property
    def target_node(self):
        return self._header.target_node

    @target_node.setter
    def target_node(self, node):
        self._header.target_node = node

    @property
    def source(self):
        return self._header.source

    @source.setter
    def source(self, address):
        self._header.source = address

    @property
    def source_port(self):
        return self._header.source_port

    @source_port.setter
    def source_port(self, port):
        self._header.source_port = port

    @property
    def source_node(self):
        return self._header.source_node

    @source_node.setter
    def source_node(self, node):
        self._header.source_node = node

    @property
    def err(self):
        return self._header.err

    @err.setter
    def err(self, errorCode):
        self._header.err = errorCode

    def serialise(self):
        buf = bytearray()
        buf += self._header.serialise()
        buf += self._body
        buf += bytes([Message.checksum(buf) ^ 0xFF])
        buf = Message.START_OF_PACKET + Message.escape_buffer(buf)
        buf += Message.END_OF_PACKET
        return buf

    def pack(self, type_string, value):
        if type_string == 'uint8_t':
            return self.pack_uint8(value)
        if type_string == 'uint16_t':
            return self.pack_uint16(value)
        if type_string == 'uint32_t':
            return self.pack_uint32(value)
        if type_string == 'uint64_t':
            return self.pack_uint64(value)
        if type_string == 'int8_t':
            return self.pack_int8(value)
        if type_string == 'int16_t':
            return self.pack_int16(value)
        if type_string == 'int32_t':
            return self.pack_int32(value)
        if type_string == 'int64_t':
            return self.pack_int32(value)
        if type_string == 'float':
            return self.pack_float(value)
        if type_string == 'double':
            return self.pack_double(value)
        if type_string == 'bool':
            return self.pack_bool(value)
        if type_string == 'std::string':
            return self.pack_string(value)

        raise AttributeError

    def pack_uint8(self, value):
        self._pack(Pack.uint8, value)

    def pack_int8(self, value):
        self._pack(Pack.int8, value)

    def pack_uint16(self, value):
        self._pack(Pack.uint16, value)

    def pack_int16(self, value):
        self._pack(Pack.int16, value)

    def pack_uint32(self, value):
        self._pack(Pack.uint32, value)

    def pack_int32(self, value):
        self._pack(Pack.int32, value)

    def pack_float(self, value):
        self._pack(Pack.float32, value)

    def pack_bytes(self, buf):
        self._body += buf

    def pack_array(self, buf, packer):
        for value in buf:
            packer(value)

    def pack_bool(self, value):
        self._pack(Pack.bool8, value)

    def pack_string(self, string):
        string += '\0'
        self._body += string.encode('ascii')

    def _pack(self, packer, value):
        if isinstance(value, list):
            for i in range(len(value)):
                self._body += packer(value.pop(0))
        else:
            self._body += packer(value)

    def unpack(self, type_string, count=1):
        if type_string == 'uint8_t':
            unpacker = Unpack.uint8
            size = 1
        elif type_string == 'uint16_t':
            unpacker = Unpack.uint16
            size = 2
        elif type_string == 'uint32_t':
            unpacker = Unpack.uint32
            size = 4
        elif type_string == 'uint64_t':
            unpacker = Unpack.uint64
            size = 8
        elif type_string == 'int8_t':
            unpacker = Unpack.int8
            size = 1
        elif type_string == 'int16_t':
            unpacker = Unpack.int16
            size = 2
        elif type_string == 'int32_t':
            unpacker = Unpack.int32
            size = 4
        elif type_string == 'int64_t':
            unpacker = Unpack.int64
            size = 8
        elif type_string == 'float':
            unpacker = Unpack.float32
            size = 4
        elif type_string == 'double':
            unpacker = Unpack.float64
            size = 8
        elif type_string == 'bool':
            unpacker = Unpack.bool8
            size = 1
        elif type_string == 'std::string':
            unpacker = Unpack.string
            # size of a variable length string is unknown.
            # setting size equal to length of self._body
            size = len(self._body)
        else:
            raise AttributeError

        if count == 1:
            return self._unpack(unpacker, size)

        return self.unpack_array(unpacker, size, count)

    def unpack_uint8(self):
        return self._unpack(Unpack.uint8, 1)

    def unpack_int8(self):
        return self._unpack(Unpack.int8, 1)

    def unpack_uint16(self):
        return self._unpack(Unpack.uint16, 2)

    def unpack_int16(self):
        return self._unpack(Unpack.int16, 2)

    def unpack_uint32(self):
        return self._unpack(Unpack.uint32, 4)

    def unpack_int32(self):
        return self._unpack(Unpack.int32, 4)

    def unpack_float(self):
        return self._unpack(Unpack.float32, 4)

    def unpack_bytes(self):
        buf = bytearray(self._body)
        self._body.clear()
        return buf

    def unpack_array(self, unpacker, size, count=None):
        array = []
        for x in range(int(min(len(self._body)/size, count))):
            array.append(self._unpack(unpacker, size))

        return array

    def _unpack(self, unpacker, size):
        buf = self._body[:size]
        self._body = self._body[size:]
        return unpacker(buf)

    @staticmethod
    def checksum(buf):
        chksum = 0
        for byte in buf:
            chksum += byte
        return chksum & 0xFF

    @staticmethod
    def escape_buffer(in_buf):
        out_buf = bytearray()
        for byte in in_buf:
            if (byte is Message.START_OF_PACKET[0]
                    or byte is Message.END_OF_PACKET[0]
                    or byte is Message.ESCAPE[0]):
                out_buf += bytes([Message.ESCAPE[0]])
                if byte is Message.START_OF_PACKET[0]:
                    byte = Message.ESCAPED_START[0]
                elif byte is Message.END_OF_PACKET[0]:
                    byte = Message.ESCAPED_END[0]
                else:
                    byte = Message.ESCAPED_ESCAPE[0]
            out_buf += bytes([byte])
        return out_buf

    @staticmethod
    def unescape_buffer(in_buf):
        out_buf = bytearray()
        i_in_buf = iter(in_buf)
        for byte in i_in_buf:
            if byte is Message.ESCAPE[0]:
                next_byte = i_in_buf.__next__()
                if next_byte is Message.ESCAPED_START[0]:
                    out_buf += Message.START_OF_PACKET
                elif next_byte is Message.ESCAPED_END[0]:
                    out_buf += Message.END_OF_PACKET
                elif next_byte is Message.ESCAPED_ESCAPE[0]:
                    out_buf += Message.ESCAPE
                else:
                    logger.warn('Character incorrectly Escaped')
                    raise AttributeError
                continue
            else:
                out_buf += bytes([byte])
        return out_buf

    @staticmethod
    def from_command_message(msg):
        '''Returns a Response Message given a Command Message
        '''
        response = Message()
        response.is_response = True
        response.did = msg.did
        response.cid = msg.cid
        response.target = msg.source
        response.source = msg.target

        return response

    @staticmethod
    def from_buffer(buf):
        '''Pass an *escaped* buffer to this helper
        Returns a Message Class instance
        '''
        try:
            # Find SOP
            start_index = buf.index(Message.START_OF_PACKET[0])
        except ValueError:
            raise
        try:
            # Find EOP
            end_index = buf.index(Message.END_OF_PACKET[0])
        except ValueError:
            raise

        # Strip SOP & EOP
        buf = buf[start_index+1:end_index]

        try:
            buf = Message.unescape_buffer(buf)
        except Exception:
            logger.error('Unescaping Failed!')
            raise

        # Validate packet
        chksum = Message.checksum(buf)
        if chksum != 0xFF:
            logger.warning('Bad Checksum: {}'.format(chksum))
            raise AttributeError

        try:
            header = Header.from_buffer(buf)
        except Exception:
            logger.warning('Bad Header: {}'.format(buf.hex()))
            raise AttributeError

        body = buf[header.byte_length:-1]
        return Message(header, body)
