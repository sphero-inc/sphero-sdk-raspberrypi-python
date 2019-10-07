#!/usr/bin/env python3

import logging
from .sphero_header_base import SpheroHeaderBase
from .api_sphero_protocol import Flags, ErrorCode, Pack, Unpack


logger = logging.getLogger(__name__)


class Header(SpheroHeaderBase):
    __slots__ = ['__flags', '__did', '__cid', '__seq', '__target',
                 '__source', '__err', 'byte_length']
    def __init__(self, flags=None, did=None, cid=None, seq=None,
                 target=None, source=None, err=None, byte_length=None):
        self.__flags = flags if flags is not None else 0x00
        self.__did = did if did is not None else 0x00
        self.__cid = cid if cid is not None else 0x00
        self.__seq = seq if seq is not None else 0x00
        self.target = target
        self.source = source
        self.err = err

        self.byte_length = byte_length

    @property
    def is_response(self):
        return self.is_flag_set(Flags.packet_is_response)

    @is_response.setter
    def is_response(self, answer):
        if answer:
            self.set_flag(Flags.packet_is_response)
            self.clear_flag(Flags.packet_requests_response)
            self.clear_flag(Flags.packet_requests_response_if_error)
        else:
            self.clear_flag(Flags.packet_is_response)

    @property
    def requests_response(self):
        return self.is_flag_set(Flags.packet_requests_response)

    @requests_response.setter
    def requests_response(self, answer):
        if answer:
            self.set_flag(Flags.packet_requests_response)
        else:
            self.clear_flag(Flags.packet_requests_response)

    @property
    def requests_error_response(self):
        return (self.requests_response
                and self.is_flag_set(Flags.packet_requests_response_if_error))

    @requests_error_response.setter
    def requests_error_response(self, answer):
        if answer:
            self.set_flag(Flags.packet_requests_response)
            self.set_flag(Flags.packet_requests_response_if_error)
        else:
            self.clear_flag(Flags.packet_requests_response_if_error)

    @property
    def is_activity(self):
        return self.is_flag_set(Flags.packet_is_activity)

    @is_activity.setter
    def is_activity(self, answer):
        if answer:
            self.set_flag(Flags.packet_is_activity)
        else:
            self.clear_flag(Flags.packet_is_activity)

    @property
    def has_target(self):
        return self.is_flag_set(Flags.packet_has_target)

    @has_target.setter
    def has_target(self, answer):
        if answer:
            self.set_flag(Flags.packet_has_target)
        else:
            self.clear_flag(Flags.packet_has_target)
            self.target = None

    @property
    def has_source(self):
        return self.is_flag_set(Flags.packet_has_source)

    @has_source.setter
    def has_source(self, answer):
        if answer:
            self.set_flag(Flags.packet_has_source)
        else:
            self.clear_flag(Flags.packet_has_source)
            self.source = None

    @property
    def has_extended_flags(self):
        return self.is_flag_set(Flags.packet_has_more_flags)

    @has_extended_flags.setter
    def has_extended_flags(self, answer):
        raise NotImplementedError

    @property
    def did(self):
        return self.__did

    @did.setter
    def did(self, device):
        if device < 0x00:
            raise ValueError
        if device > 0xFF:
            raise ValueError
        self.__did = device

    @property
    def cid(self):
        return self.__cid

    @cid.setter
    def cid(self, command):
        if command < 0x00:
            raise ValueError
        if command > 0xFF:
            raise ValueError
        self.__cid = command

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, address):
        if address is None:
            self.__target = address
            return
        if address < 0x00:
            raise ValueError
        if address > 0xFF:
            raise ValueError
        self.has_target = True
        self.__target = address

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, address):
        if address is None:
            self.__source = address
            return
        if address < 0x00:
            raise ValueError
        if address > 0xFF:
            raise ValueError
        self.has_source = True
        self.__source = address

    @property
    def target_port(self):
        return self._get_port(self.target)

    @target_port.setter
    def target_port(self, port):
        self.target = self._set_port(self.target, port)

    @property
    def target_node(self):
        return self._get_node(self.target)

    @target_node.setter
    def target_node(self, node):
        self.target = self._set_node(self.target, node)

    @property
    def source_port(self):
        return self._get_port(self.source)

    @source_port.setter
    def source_port(self, port):
        self.source = self._set_port(self.source, port)

    @property
    def source_node(self):
        return self._get_node(self.source)

    @source_node.setter
    def source_node(self, node):
        self.source = self._set_node(self.source, node)

    @property
    def seq(self):
        return self.__seq

    @seq.setter
    def seq(self, sequence):
        if sequence < 0x00:
            raise ValueError
        if sequence > 0xFF:
            raise ValueError
        self.__seq = sequence

    @property
    def err(self):
        return self.__err

    @err.setter
    def err(self, value):
        if value is None:
            self.__err = value
            return
        if value < 0x00:
            raise ValueError
        if value > 0xFF:
            raise ValueError
        self.is_response = True
        self.__err = value

    @property
    def packet_type_string(self):
        if self.is_response:
            return 'RESPONSE'
        else:
            return 'COMMAND'

    @staticmethod
    def _get_port(address):
        return (address >> 4) & 0xF

    @staticmethod
    def _get_node(address):
        return address & 0xF

    @staticmethod
    def _set_port(address, port):
        if port < 0x0:
            raise ValueError
        if port > 0xF:
            raise ValueError
        if address is None:
            address = 0x00
        return (address & 0xF) | (port << 4)

    @staticmethod
    def _set_node(address, node):
        if node < 0x0:
            raise ValueError
        if node > 0xF:
            raise ValueError
        if address is None:
            address = 0x00
        return (address & 0xF0) | node

    def clear_flag(self, pos):
        self.__flags &= ~(pos) & 0xFF

    def set_flag(self, pos):
        self.__flags |= pos

    def is_flag_set(self, pos):
        return bool(self.__flags & pos)

    def serialise(self):
        try:
            buf = bytearray()
            buf += Pack.uint8(self.__flags)

            if self.has_extended_flags:
                logger.critical('MORE FLAGS UNSUPPORTED!')

            if self.has_target:
                buf += Pack.uint8(self.target)

            if self.has_source:
                buf += Pack.uint8(self.source)

            buf += Pack.uint8(self.did)
            buf += Pack.uint8(self.cid)
            buf += Pack.uint8(self.seq)

            if self.is_response:
                buf += Pack.uint8(self.err)

            return buf
        except Exception:
            raise AttributeError

    @staticmethod
    def from_buffer(buf):
        '''Pass an unescaped buffer to this method
        Returns a Header Class instance
        '''
        bit_index = 0
        flags = Unpack.uint8(buf[bit_index:])
        bit_index += 1
        header = Header(flags)
        logger.debug('FLAGS: {:x}'.format(flags))

        if header.has_extended_flags:
            header.more_flags = Unpack.uint8(buf[bit_index:])
            bit_index += 1
            logger.debug('MORE FLAGS: {}'.format(header.more_flags))
            logger.critical('Extra Flags NOT Supported!!!!')

        if header.has_target:
            header.target = Unpack.uint8(buf[bit_index:])
            bit_index += 1
            logger.debug('TARGET: {}'.format(header.target))

        if header.has_source:
            header.source = Unpack.uint8(buf[bit_index:])
            bit_index += 1
            logger.debug('SOURCE {}'.format(header.source))

        header.did = Unpack.uint8(buf[bit_index:])
        bit_index += 1
        logger.debug('DID {:x}'.format(header.did))

        header.cid = Unpack.uint8(buf[bit_index:])
        bit_index += 1
        logger.debug('CID {:x}'.format(header.cid))

        header.seq = Unpack.uint8(buf[bit_index:])
        bit_index += 1
        logger.debug('SEQ {:x}'.format(header.seq))

        err = None
        if header.is_response:
            header.err = ErrorCode(Unpack.uint8(buf[bit_index:]))
            bit_index += 1
            logger.debug('ERROR: {}'.format(err))

        header.byte_length = bit_index
        return header
