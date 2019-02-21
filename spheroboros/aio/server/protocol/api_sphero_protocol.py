#!/usr/bin/env python3

from enum import IntEnum
import logging
import struct


logger = logging.getLogger(__name__)


class Flags(IntEnum):
    PACKET_IS_RESPONSE = 1
    PACKET_REQUESTS_RESPONSE = 2
    PACKET_REQUESTS_RESPONSE_IF_ERROR = 4
    PACKET_IS_ACTIVITY = 8
    PACKET_HAS_TARGET = 16
    PACKET_HAS_SOURCE = 32
    PACKET_UNUSED_FLAG_BIT = 64
    PACKET_HAS_MORE_FLAGS = 128


class ErrorCode(IntEnum):
    SUCCESS = 0x00
    BAD_DID = 0x01
    BAD_CID = 0x02
    NOT_YET_IMPLEMENTED = 0x03
    RESTRICTED = 0x04
    BAD_DATA_LENGTH = 0x05
    FAILED = 0x06
    BAD_DATA_VALUE = 0x07
    BUSY = 0x08
    BAD_TID = 0x09
    TARGET_UNAVAILABLE = 0x0A


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
