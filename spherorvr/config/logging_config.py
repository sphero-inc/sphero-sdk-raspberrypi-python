from spherorvr.config.log_level import LogLevel


def get_dict(log_level):
    if log_level == LogLevel.Errors:
        return errors
    elif log_level == LogLevel.Debug_Verbose:
        return debug_verbose


silent = {
    'version': 1,
    'handlers': {
        'null_handler': {
            'level': 'WARNING',
            'class': 'logging.NullHandler',
        }
    },
    'root': {
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
    'root': {
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
        'spherorvr.observer.dal.rvr_parser': {
            'level': 'DEBUG',
            'propagate': True
        },
        'spherorvr.observer.dal.rvr_port': {
            'level': 'DEBUG',
            'propagate': True
        }
    },
    'root': {
        'handlers': ['debug_handler']
    }
}
