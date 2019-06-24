from spherorvr.config.log_level import LogLevel


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
        'spherorvr.observer.dal.rvr_dal': {
            'propagate': True
        },
        'spherorvr.observer.dal.rvr_parser': {
            'propagate': True
        },
        'spherorvr.observer.dal.rvr_port': {
            'propagate': True
        },
        'spherorvr.observer.events.rvr_event_dispatcher': {
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
        'spherorvr.observer.dal.rvr_dal': {
            'propagate': True
        },
        'spherorvr.observer.dal.rvr_parser': {
            'propagate': True
        },
        'spherorvr.observer.dal.rvr_port': {
            'propagate': True
        },
        'spherorvr.observer.events.rvr_event_dispatcher': {
            'propagate': True
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['debug_handler']
    }
}
