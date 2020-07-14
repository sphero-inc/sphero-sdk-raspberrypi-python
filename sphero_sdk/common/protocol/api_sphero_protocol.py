#!/usr/bin/env python3

from enum import IntEnum
import logging
import struct


logger = logging.getLogger(__name__)


class Flags(IntEnum):
    packet_is_response = 1
    packet_requests_response = 2
    packet_requests_response_if_error = 4
    packet_is_activity = 8
    packet_has_target = 16
    packet_has_source = 32
    packet_unused_flag_bit = 64
    packet_has_more_flags = 128


class ErrorCode(IntEnum):
    success = 0x00
    bad_did = 0x01
    bad_cid = 0x02
    not_yet_implemented = 0x03
    restricted = 0x04
    bad_data_length = 0x05
    failed = 0x06
    bad_data_value = 0x07
    busy = 0x08
    bad_tid = 0x09
    target_unavailable = 0x0A


class Pack:
    @staticmethod
    def int8(value):
        return struct.pack('b', value)

    @staticmethod
    def uint8(value):
        return struct.pack('B', value)

    @staticmethod
    def uint16(value):
        return struct.pack('>H', value)

    @staticmethod
    def int16(value):
        return struct.pack('>h', value)

    @staticmethod
    def int32(value):
        return struct.pack('>i', value)

    @staticmethod
    def uint32(value):
        return struct.pack('>I', value)

    @staticmethod
    def float32(value):
        return struct.pack('>f', value)

    @staticmethod
    def bool8(value):
        return struct.pack('>?', value)


class Unpack:
    @staticmethod
    def int8(buf):
        return struct.unpack('b', buf[:1])[0]

    @staticmethod
    def uint8(buf):
        return struct.unpack('B', buf[:1])[0]

    @staticmethod
    def uint16(buf):
        return struct.unpack('>H', buf[:2])[0]

    @staticmethod
    def int16(buf):
        return struct.unpack('>h', buf[:2])[0]

    @staticmethod
    def int32(buf):
        return struct.unpack('>i', buf[:4])[0]

    @staticmethod
    def uint32(buf):
        return struct.unpack('>I', buf[:4])[0]

    @staticmethod
    def float32(buf):
        return struct.unpack('>f', buf[:4])[0]

    @staticmethod
    def bool8(buf):
        return struct.unpack('>?', buf[:1])[0]

    @staticmethod
    def string(buf):
        size = len(buf)
        fmt = '{}s'.format(size)
        string_bytes = struct.unpack(fmt, buf[:size])[0]
        return string_bytes.decode('utf-8')