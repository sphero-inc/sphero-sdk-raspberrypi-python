#! /usr/bin/env python3

import pytest
from spheroboros.aio.common.dal.mock_async_dal import MockAsyncDal
from spheroboros.common.parameter import Parameter
from spheroboros.aio.client.toys.async_sphero_rvr import AsyncSpheroRvr


@pytest.fixture(scope='session')
def mock_async_dal():
    dal = MockAsyncDal()
    yield dal


@pytest.fixture
def mock_input_parameters():
    parameters = [
        Parameter(
            name='input0',
            data_type='uint8_t',
            index=0,
            size=1,
            value=1
        ),
        Parameter(
            name='input1',
            data_type='int8_t',
            index=1,
            size=1,
            value=-1
        ),
        Parameter(
            name='input2',
            data_type='uint16_t',
            index=2,
            size=1,
            value=100000
        ),
        Parameter(
            name='input3',
            data_type='uint8_t',
            index=3,
            size=2,
            value=[10, 11]
        )
    ]

    yield parameters


@pytest.fixture
def mock_output_parameters():
    parameters = [
        Parameter(
            name='output0',
            data_type='uint8_t',
            index=0,
            size=1
        ),
        Parameter(
            name='output1',
            data_type='float',
            index=1,
            size=1
        ),
        Parameter(
            name='output2',
            data_type='uint16_t',
            index=2,
            size=2
        ),
        Parameter(
            name='output3',
            data_type='std::string',
            index=3,
            size=1
        )
    ]

    yield parameters


@pytest.fixture(scope='session')
def random_value():
    mock = MockAsyncDal()
    return mock.random_value


@pytest.fixture(scope='session')
def random_list():
    mock = MockAsyncDal()
    return mock.random_list


@pytest.fixture(scope='session')
def async_mock_sphero_rvr():
    rvr = AsyncSpheroRvr(
        dal=MockAsyncDal()
    )
    yield rvr
    # TODO rvr.cleanup()
