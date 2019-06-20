ERRORS = {
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


DEBUG_VERBOSE = {
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
