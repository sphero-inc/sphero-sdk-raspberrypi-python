#!/usr/bin/env python3

from protocol.api_sphero_header import Header
from protocol.api_sphero_message import Message


def test_serialize_header():
    header = Header()
    header.requests_response = True
    header.target = 10
    header.source = 20
    header.did = 30
    header.cid = 40
    header.seq = 50

    buf = header.serialise()
    expected = bytes.fromhex('320a141e2832')
    assert buf == expected


def test_serialize_message():
    message = Message()
    message.requests_response = True
    message.target = 10
    message.source = 20
    message.did = 30
    message.cid = 40
    message.seq = 50
    message.pack_bytes(bytearray.fromhex('ABCDEF'))

    buf = message.serialise()
    expected = bytes.fromhex('8d320a141e2832ab23cdefd0d8')
    assert buf == expected


def test_packers_unpackers():
    message = Message()
    message.requests_response = True
    message.target = 10
    message.source = 20
    message.did = 30
    message.cid = 40
    message.seq = 50

    message.pack_uint8(0)
    message.pack_uint16(1)
    message.pack_uint32(2)
    message.pack_float(3.14)
    message.pack_bytes(b'abc')
    message.pack_string('whut')

    print("Body: {}".format(message._body.hex()))
    assert message._body == bytearray.fromhex(
            '00010002000000c3f548406162637768757400')

    assert message.unpack_uint8() == 0
    assert message.unpack_uint16() == 1
    assert message.unpack_uint32() == 2
    assert message.unpack_float() == 3.140000104904175


def test_prop_getters_setters():
    message = Message()
    message.target = 0x01
    assert message.has_target

    message.source = 0x02
    assert message.has_source

    message.has_target = False
    assert message.target is None

    message.has_source = False
    assert message.source is None


def test_from_buffer():
    message = Message()
    message.requests_response = True
    message.target = 10
    message.source = 20
    message.did = 30
    message.cid = 40
    message.seq = 50

    buf = message.serialise()

    new_message = Message.from_buffer(buf)

    assert new_message.requests_response
    assert new_message.has_target
    assert new_message.has_source
    assert new_message.target == 10
    assert new_message.source == 20
    assert new_message.did == 30
    assert new_message.cid == 40
    assert new_message.seq == 50
