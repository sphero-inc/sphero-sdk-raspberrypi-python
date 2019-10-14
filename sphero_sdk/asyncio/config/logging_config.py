from sphero_sdk.common.log_level import LogLevel


def get_dict(log_level):
    if log_level == LogLevel.Silent:
        return silent
    elif log_level == LogLevel.Errors:
        return errors
    elif log_level == LogLevel.Debug_Verbose:
        return debug_verbose


silent = {
    'version': 1,
    'handlers': {
        'null_handler': {
            'level': 'NOTSET',
            'class': 'logging.NullHandler',
        }
    },
    'root': {
        'level': 'NOTSET',
        'handlers': ['null_handler']
    }
}

errors = {
    'version': 1,
    'handlers': {
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'sphero_sdk.asyncio.client.dal.serial_async_dal': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.handler.api_sphero_handler': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.parser.api_sphero_parser': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.port.serial_sphero_port': {
            'propagate': True
        },
        'sphero_sdk.asyncio.controls.sensor_control_async': {
            'propagate': True
        },
        'sphero_sdk.asyncio.client.firmware.rvr_fw_check_async': {
            'propagate': True
        },
        'sphero_sdk.asyncio.client.dal.restful_async_dal': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_streaming_control': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_stream_slot': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_stream_service': {
            'propagate': True
        }
    },
    'root': {
        'level': 'ERROR',
        'handlers': ['error_handler']
    }
}

debug_verbose = {
    'version': 1,
    'handlers': {
        'debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'sphero_sdk.asyncio.client.dal.serial_async_dal': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.handler.api_sphero_handler': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.parser.api_sphero_parser': {
            'propagate': True
        },
        'sphero_sdk.asyncio.server.port.serial_sphero_port': {
            'propagate': True
        },
        'sphero_sdk.asyncio.controls.sensor_control_async': {
            'propagate': True
        },
        'sphero_sdk.asyncio.client.firmware.rvr_fw_check_async': {
            'propagate': True
        },
        'sphero_sdk.asyncio.client.dal.restful_async_dal': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_streaming_control': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_stream_slot': {
            'propagate': True
        },
        'sphero_sdk.common.sensors.sensor_stream_service': {
            'propagate': True
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['debug_handler']
    }
}
