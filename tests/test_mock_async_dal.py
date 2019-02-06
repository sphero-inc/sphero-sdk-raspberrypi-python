#! /usr/bin/env python3

import pytest


def test_random_value_uint8_t(mock_async_dal):
    value = mock_async_dal.random_value('uint8_t')
    assert value >= 0
    assert value < 256
    assert isinstance(value, int)


def test_random_value_uint16_t(mock_async_dal):
    value = mock_async_dal.random_value('uint16_t')
    assert value > 255
    assert value < 65536
    assert isinstance(value, int)


def test_random_value_uint32_t(mock_async_dal):
    value = mock_async_dal.random_value('uint32_t')
    assert value > 65535
    assert value < 4294967296
    assert isinstance(value, int)


def test_random_value_uint64_t(mock_async_dal):
    value = mock_async_dal.random_value('uint64_t')
    assert value > 4294967295
    assert isinstance(value, int)


def test_random_value_int8_t(mock_async_dal):
    value = mock_async_dal.random_value('int8_t')
    assert value > -129
    assert value < 0
    assert isinstance(value, int)


def test_random_value_int16_t(mock_async_dal):
    value = mock_async_dal.random_value('int16_t')
    assert value > -32769
    assert value < -129
    assert isinstance(value, int)


def test_random_value_int32_t(mock_async_dal):
    value = mock_async_dal.random_value('int32_t')
    assert value > -2147483648
    assert value < -32769
    assert isinstance(value, int)


def test_random_value_int64_t(mock_async_dal):
    value = mock_async_dal.random_value('int64_t')
    assert value < -21474836484
    assert isinstance(value, int)


def test_random_value_float(mock_async_dal):
    value = mock_async_dal.random_value('float')
    assert isinstance(value, float)


def test_random_value_double(mock_async_dal):
    value = mock_async_dal.random_value('double')
    assert isinstance(value, float)


def test_random_value_bool(mock_async_dal):
    value = mock_async_dal.random_value('bool')
    assert isinstance(value, bool)


def test_random_value_string(mock_async_dal):
    value = mock_async_dal.random_value('std::string')
    assert isinstance(value, str)


@pytest.mark.asyncio
async def test_send_command(
        mock_async_dal, mock_input_parameters, mock_output_parameters):
    response = await mock_async_dal.send_command(
        did=0x00,
        cid=0x00,
        target=0x00,
        timeout=0.0,
        inputs=mock_input_parameters,
        outputs=mock_output_parameters
    )

    assert isinstance(response[0], int)
    assert isinstance(response[1], float)
    assert isinstance(response[2], list)
    assert isinstance(response[3], str)
